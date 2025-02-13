import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import transforms
from TorchModel import SunspotDataset, SunspotCounter

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
criterion = nn.MSELoss()
def test_model(model, test_loader):
    model.eval()
    total_loss = 0.0
    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)
            total_loss += loss.item()
            print("Ошибка на данном тесте:", loss.item())

    print(f"Средняя потеря на тесте: {total_loss / len(test_loader):.4f}")

if __name__ == "__main__":
    transform = transforms.Compose([
        transforms.Resize((512, 512)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.28155156, 0.28155156, 0.28155156], std=[0.24071367, 0.24071367, 0.24071367]),
    ])

    test_dataset = SunspotDataset(image_dir='Data/test/images',
                                  labels_file='Data/test/res2.csv',
                                  transform=transform)

    test_loader = DataLoader(test_dataset, batch_size=6, shuffle=False)
    model = SunspotCounter()
    model.load_state_dict(torch.load("best_model4.pth"))
    model = model.to(device)
    test_model(model, test_loader)
