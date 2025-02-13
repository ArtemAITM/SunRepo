import os
from datetime import datetime, timedelta

start_date = datetime(2011, 1, 1)
end_date = datetime(2024, 11, 25)

current_date = start_date
while current_date <= end_date:
    day, month, year = str(current_date.day).zfill(2), str(current_date.month).zfill(2), str(current_date.year)
    if os.path.exists(f"E:/SunData/images/{year}/{month}/{day}"):
        files = os.listdir(f"E:/SunData/images/{year}/{month}/{day}")
        files.sort()
        for i in files:
            if i != files[0]:
                os.remove(f"E:/SunData/images/{year}/{month}/{day}/{i}")
                print("Del")
            print(i)
    else:
        print("Skipped")
    current_date += timedelta(days=1)