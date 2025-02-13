import re
import os
import time
from datetime import datetime, timedelta

import cloudscraper
from requests.exceptions import RequestException

MAX_RETRIES = 5000
RETRY_DELAY = 0.05
scraper = cloudscraper.create_scraper()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}


def access_site(link):
    retries_left = MAX_RETRIES
    while retries_left > 0:
        try:
            response = scraper.get(link, headers=headers)
            if response.status_code == 200:
                print("Успех! Доступ к сайту получен.")
                return response.text
            else:
                print(f"Неудача. Статус-код: {response.status_code}")
                retries_left -= 1
                time.sleep(RETRY_DELAY)
        except RequestException as e:
            print(f"Произошла ошибка: {e}")
            retries_left -= 1
            time.sleep(RETRY_DELAY)
    print("Максимальное количество попыток исчерпано.")
    return None


def download_images(html_content, day, month, year):
    image_urls = re.findall(r'src="(/[^"]+HMIIF\.jpg)"', html_content)
    if not image_urls:
        print("Изображения с 'HMIIF.jpg' в имени не найдены.")
        return

    base_url = 'https://www.spaceweatherlive.com'
    save_dir = f"../images/{day}_{month}_{year}"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for i, relative_url in enumerate(image_urls):
        image_url = base_url + relative_url
        image_name = os.path.basename(relative_url)
        image_path = os.path.join(save_dir, image_name)

        try:
            response = scraper.get(image_url, stream=True)
            if response.status_code == 200:
                with open(image_path, 'wb') as f:
                    f.write(response.content)
                print(f"{i + 1}/{len(image_urls)}: {image_name} сохранено.")
            else:
                print(f"Не удалось скачать {image_name}. Статус-код: {response.status_code}")
        except RequestException as e:
            print(f"Произошла ошибка при скачивании {image_name}: {e}")



start_date = datetime(2024, 12, 1)
end_date = datetime(2025, 1, 15)

now = start_date
while now <= end_date:
    print(f"Скачиваем изображения для {now.strftime('%Y-%m-%d')}")
    url = f'https://www.spaceweatherlive.com/ru/arhiv/{now.year}/{str(now.month).zfill(2)}/{str(now.day).zfill(2)}/dayobs.html'
    html_content = access_site(url)
    if html_content is not None:
        download_images(html_content, now.year, str(now.month).zfill(2), str(now.day).zfill(2))
    now += timedelta(days=1)

print("Скачивание завершено.")


