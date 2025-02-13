import os
import random
import cv2
import torch
from ultralytics import YOLO

model = YOLO("runs/detect/train2/weights/best.pt")


def detect_objects(image):
    results = model(image)
    return results


def draw_bboxes(image, results):
    for result in results:
        boxes = result.boxes
        if boxes is not None:
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                confidence = box.conf.cpu().numpy()
                class_id = int(box.cls.cpu().numpy())
                if confidence >= 0.01:
                    label = model.names[class_id]
                    color = (0, 255, 0)
                    cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
                    cv2.putText(image, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
    return image



image_folder = 'images'
all_files = os.listdir(image_folder)
image_files = [f for f in all_files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
if len(image_files) < 10:
    raise ValueError("В папке недостаточно изображений для выбора 10 случайных файлов.")
random_images = random.sample(image_files, 10)
for idx, image_name in enumerate(random_images):
    image_path = os.path.join(image_folder, image_name)
    original_image = cv2.imread(image_path)

    if original_image is None:
        print(f"Не удалось загрузить изображение {image_path}. Пропуск.")
        continue
    results = detect_objects(original_image)
    image_with_bboxes = original_image.copy()
    image_with_bboxes = draw_bboxes(image_with_bboxes, results)
    cv2.imshow(f'Original Image {idx + 1}', original_image)
    cv2.waitKey(0)
    cv2.imshow(f'Image with BBoxes {idx + 1}', image_with_bboxes)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
