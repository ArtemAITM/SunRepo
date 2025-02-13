import sys
import cv2
import os
import subprocess
from datetime import datetime, timedelta
import numpy as np


def prepare_sun(dir):
    f = cv2.imread(dir)
    c = cv2.inRange(f, (0, 20, 50), (255, 255, 255))
    cnt, _ = cv2.findContours(c, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    img = np.zeros_like(c)
    cnt = sorted(cnt, key=lambda x: -cv2.contourArea(x))
    moments = cv2.moments(cnt[0])
    if moments["m00"] != 0:
        cx = moments["m10"] / moments["m00"]
        cy = moments["m01"] / moments["m00"]
    else:
        cx, cy = 0, 0

    cnew = []
    for point in cnt[0]:
        x, y = point[0]
        x_new = cx + (x - cx) * (1 - 50 / cv2.arcLength(cnt[0], True))
        y_new = cy + (y - cy) * (1 - 50 / cv2.arcLength(cnt[0], True))
        cnew.append([[int(x_new), int(y_new)]])

    cv2.drawContours(img, [np.array(cnew)], -1, (255, 255, 255), cv2.FILLED)
    res = cv2.bitwise_and(f, f, mask=img)
    res[img < 5] = [255, 255, 255]
    cv2.imwrite(dir, res)


start_date = datetime(2011, 1, 1)
end_date = datetime(2024, 11, 25)

current_date = start_date
while current_date <= end_date:
    print(current_date)
    day, month, year = current_date.day, current_date.month, current_date.year
    files = os.listdir(f"../images/{year}/{str(month).zfill(2)}/{str(day).zfill(2)}")
    files.sort()
    DIR = os.path.join(f"../images/{year}/{str(month).zfill(2)}/{str(day).zfill(2)}", files[0])
    image = cv2.imread(os.path.join(f"../images/{year}/{str(month).zfill(2)}/{str(day).zfill(2)}", files[0]))

    rows, cols = 64, 64
    height, width, _ = image.shape
    sector_height = height // rows
    sector_width = width // cols
    scale = 8
    sectors = []
    os.chdir("../sectors/")
    os.makedirs(f'{str(year) + str(month).zfill(2) + str(day).zfill(2)}')
    for i in range(rows):
        for j in range(cols):
            start_y = i * sector_height
            start_x = j * sector_width
            end_y = start_y + sector_height
            end_x = start_x + sector_width
            sector = image[start_y:end_y, start_x:end_x]
            new_size = (sector_width * scale, sector_height * scale)
            resized_sector = cv2.resize(sector, new_size, interpolation=cv2.INTER_LANCZOS4)
            sectors.append(resized_sector)
            cv2.imwrite(f'{str(year)+str(month).zfill(2)+str(day).zfill(2)}/sector_{i}_{j}.jpg', resized_sector)
    current_date += timedelta(days=1)
