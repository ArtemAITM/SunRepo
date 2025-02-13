import os
import random
from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt

model = YOLO('modelYOLO.pt')
test_dir = 'E:/SunData/Data/train/images'
image_extensions = ('.jpg', '.jpeg', '.png', '.bmp')
image_files = [os.path.join(test_dir, f) for f in os.listdir(test_dir) if f.lower().endswith(image_extensions)]
num_images = 10 if len(image_files) >= 10 else len(image_files)
selected_images = random.sample(image_files, num_images)

for img_path in selected_images:
    results = model.predict(source=img_path, conf=0.25, imgsz=2048)
    #imgsize определяет точность работы модели - меньше размер, меньше пятен найдётся
    result = results[0]
    annotated_img = result.plot()
    print(len(result))
    plt.figure(figsize=(10, 10))
    plt.imshow(cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB))
    plt.title(f"Результат детекции для {os.path.basename(img_path)}")
    plt.axis('off')
    plt.show()