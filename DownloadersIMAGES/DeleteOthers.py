import sys
from datetime import datetime, timedelta
import os

start_date = datetime(2014, 1, 1)
end_date = datetime(2024, 11, 25)

current_date = start_date
while current_date <= end_date:
    day, month, year = str(current_date.day).zfill(2), str(current_date.month).zfill(2), str(current_date.year)
    print(os.path.exists(f"E:/SunData/sectrs/{year}_{month}_{day}"), f"E:/SunData/sectrs/{year}_{month}_{day}")
    if os.path.exists(f"E:/SunData/sectrs/{year}_{month}_{day}"):
        files = os.listdir(f"E:/SunData/sectrs/{year}_{month}_{day}")
        for i in files:
            if len(i) > 15:
                os.remove(f"E:/SunData/sectrs/{year}_{month}_{day}/{i}")
                print("Del")
            print(i)
    else:
        print("Skipped")
    current_date += timedelta(days=1)