import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime, timedelta

base_url = "https://sdo.gsfc.nasa.gov/assets/img/browse/"

download_root = "images"


def create_directory_structure(year, month, day):
    dir_path = os.path.join(download_root, str(year), str(month).zfill(2), str(day).zfill(2))
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path


def download_images_for_date(year, month, day):
    try:
        date_str = f"{year}/{month:02d}/{day:02d}/"
        url = urljoin(base_url, date_str)
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Ошибка при запросе для {url}: {response.status_code}")
            return
        soup = BeautifulSoup(response.text, 'html.parser')

        a_tags = soup.find_all('a', href=True)
        k = 0
        dir_path = create_directory_structure(year, month, day)
        for a in a_tags:
            img_url = a.get('href')

            if "2024_HMIIС.jpg" in img_url and img_url.endswith('.jpg') and k < 10:
                img_url = urljoin(url, img_url)
                img_name = os.path.join(dir_path, img_url.split("/")[-1])

                try:
                    img_response = requests.get(img_url)
                    img_response.raise_for_status()
                    with open(img_name, 'wb') as f:
                        f.write(img_response.content)
                    print(f"Изображение {img_name} скачано.")
                    k += 1
                except requests.exceptions.RequestException as e:
                    print(f"Ошибка при скачивании {img_url}: {e}")
    except Exception as e:
        print("Skipped,", e)

start_date = datetime(2024, 11, 26)
end_date = datetime(2025, 1, 20)

current_date = start_date
while current_date <= end_date:
    print(f"Скачиваем изображения для {current_date.strftime('%Y-%m-%d')}")
    download_images_for_date(current_date.year, current_date.month, current_date.day)
    current_date += timedelta(days=1)

print("Скачивание завершено.")
