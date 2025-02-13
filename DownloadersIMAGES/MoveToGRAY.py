import sys
from datetime import datetime, timedelta
import os
import cv2

start_date = datetime(2014, 1, 1)
end_date = datetime(2024, 11, 25)

current_date = start_date
while current_date <= end_date:
    day, month, year = str(current_date.day).zfill(2), str(current_date.month).zfill(2), str(current_date.year)
    path = f"E:/SunData/sectrs/{year}_{month}_{day}"
    if os.path.exists(path):
        files = os.listdir(path)
        for i in files:
            img = cv2.imread(os.path.join(path, i))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(os.path.join(path, i), gray)
    else:
        print("Skipped")
    path2 = f"E:/SunData/images/{year}/{month}/{day}"
    if os.path.exists(path2):
        files = os.listdir(path2)
        for i in files:
            if i == files[0]:
                print("YES", path2)
                img = cv2.imread(os.path.join(path2, i))
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                cv2.imwrite(os.path.join(path2, i), gray)
            else:
                print("DELETED")
                os.remove(os.path.join(path2, i))
    else:
        print("Skipped")

    current_date += timedelta(days=1)