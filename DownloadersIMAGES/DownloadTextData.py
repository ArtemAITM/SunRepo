import re
import time
from datetime import datetime, timedelta
import cloudscraper
from bs4 import BeautifulSoup
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


def extract_spot_count(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    tables = soup.find_all('table', {'class': 'table table-sm table-bordered'})
    if tables:
        spot_counts = []
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['th', 'td'])
                for cell in cells:
                    match = re.search(r'(\d+)\s*<span', str(cell))
                    if match:
                        spot_counts.append(int(match.group(1)))
        return spot_counts
    else:
        print("Таблицы с указанным классом не найдены на странице.")
        return None


start_date = datetime(2011, 1, 1)
end_date = datetime(2024, 11, 26)

now = start_date
AllSpotCounts = []
while now <= end_date:
    print(f"Скачиваем данные для {now.strftime('%Y-%m-%d')}")
    url = f'https://www.spaceweatherlive.com/ru/arhiv/{now.year}/{str(now.month).zfill(2)}/{str(now.day).zfill(2)}/dayobs.html'
    html_content = access_site(url)
    if html_content is not None:
        spot_counts = extract_spot_count(html_content)
        if spot_counts is not None:
            AllSpotCounts.append({now.strftime('%Y-%m-%d'): spot_counts})
    now += timedelta(days=1)
print("Скачивание завершено.")

for item in AllSpotCounts:
    for key, value in item.items():
        print(f"{key}: {value}")
