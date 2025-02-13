import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import torchvision.transforms as transforms
from PIL import Image
import os
import torch.nn.functional as F

class SunspotDataset(Dataset):
    def __init__(self, image_dir, labels_file, transform=None):
        self.image_dir = image_dir
        self.labels = self.load_labels(labels_file)
        self.transform = transform

    def load_labels(self, labels_file):
        labels = {}
        with open(labels_file, 'r') as file:
            for line in file:
                img_name, spots, groups = line.strip().split(',')
                if groups == "":
                    groups = 0
                labels[img_name] = (int(spots), int(groups))
        return labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        img_name = list(self.labels.keys())[idx]
        spots, groups = self.labels[img_name]
        img_path = os.path.join(self.image_dir, img_name)
        image = Image.open(img_path).convert("RGB")

        if self.transform:
            image = self.transform(image)

        return image, torch.tensor([spots, groups], dtype=torch.float32)

class SunspotCounter(nn.Module):
    def __init__(self):
        super(SunspotCounter, self).__init__()
        def conv_block(in_channels, out_channels, kernel_size=3, stride=1, padding=1, dilation=1):
            return nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding, dilation),
                nn.BatchNorm2d(out_channels),
                nn.ReLU()
            )
        class ResidualBlock(nn.Module):
            def __init__(self, in_channels, out_channels, stride=1):
                super(ResidualBlock, self).__init__()
                self.conv1 = conv_block(in_channels, out_channels, kernel_size=3, stride=stride, padding=1)
                self.conv2 = conv_block(out_channels, out_channels, kernel_size=3, stride=1, padding=1)
                self.skip = nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=stride)

            def forward(self, x):
                identity = self.skip(x)
                x = self.conv1(x)
                x = self.conv2(x)
                return x + identity

        self.conv_layers = nn.Sequential(
            conv_block(3, 32, kernel_size=3, stride=1, padding=1),
            conv_block(32, 64, kernel_size=3, stride=1, padding=1),
            nn.MaxPool2d(2),
            ResidualBlock(64, 128, stride=2),
            ResidualBlock(128, 128),
            ResidualBlock(128, 256, stride=2),
            ResidualBlock(256, 256),
            ResidualBlock(256, 256),
            ResidualBlock(256, 512, stride=2),
            conv_block(512, 512),
            conv_block(512, 512),
            conv_block(512, 512),
            conv_block(512, 512, kernel_size=3, stride=1, padding=2, dilation=2),
            conv_block(512, 512, kernel_size=3, stride=1, padding=2, dilation=2),
            conv_block(512, 512, kernel_size=3, stride=1, padding=4, dilation=4),
            ResidualBlock(512, 512),
            ResidualBlock(512, 512),
            ResidualBlock(512, 512),
            conv_block(512, 1024),
            conv_block(1024, 1024),
            nn.MaxPool2d(2)
        )

        self.fc_layers = nn.Sequential(
            nn.Flatten(),
            nn.Linear(1024 * (512 // 32) * (512 // 32), 2048),
            nn.ReLU(),
            nn.Linear(2048, 1024),
            nn.ReLU(),
            nn.Linear(1024, 256),
            nn.ReLU(),
            nn.Linear(256, 2)
        )

    def forward(self, x):
        x = self.conv_layers(x)
        x = self.fc_layers(x)
        return x
