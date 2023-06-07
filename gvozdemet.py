import time
import requests
from bs4 import BeautifulSoup
import gspread

cards = []
link = []
name = []
price = []

URLS = ['https://gvozdemet.ru/krepezh/stroitelnye-gvozdi-cid185/barabannye-gvozdi-cid72/']

gc = gspread.service_account(filename='ultimate-result-371107-04a8a2effdde.json')
sheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/1rrACEEX1ZUq8z0YRicwFvMHO1Ro6SbKwb75prGDVZK0')
worksheet = sheet.worksheet("Gvozdemet")
worksheet.batch_clear(["A2:C200"])

def get_html(url, params=None):
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
    }
    html = requests.get(url, headers=headers, params=params)
    return html

def get_content(html):
    soup = BeautifulSoup(html.text, 'html.parser')
    table_rows = soup.select('tr')
    for row in table_rows:
        name_elem = row.select_one('td > span.fw-500 > a')
        if name_elem:
            link.append("https://gvozdemet.ru/" + name_elem['href'])
            name.append(name_elem.text.strip())

        price_elem = row.select_one('td:nth-of-type(7)')
        if price_elem:
            price.append(price_elem.text.strip().replace('\xa0₽', '').replace('.', ','))

def get_total_pages(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find('ul', class_='_js-ajax-pagination')
    page_links = pagination.find_all('a')
    total_pages = len(page_links) - 2  # Exclude the "Previous" and "Next" links
    return total_pages

def parser(url):
    """основная функция"""
    print(f'Парсим данные с: "{url}"')
    html = get_html(url)
    if html.status_code == 200:
        total_pages = get_total_pages(html.text)
        print(f'Общее количество страниц: {total_pages}')
        for page in range(1, total_pages + 1):
            page_url = f'{url}?page={page}'
            print(f'Парсинг страницы: {page}')
            html = get_html(page_url)
            get_content(html)
            time.sleep(1)
        print(f'Всего: {len(link)} позиций')
    else:
        print(f'Ответ сервера:{html.status_code}. Парсинг невозможен!')

def upd_gvozdemet():
    worksheet.update('A2', list(map(lambda x: [x], link)))
    worksheet.update('B2', list(map(lambda x: [x], name)))
    worksheet.update('C2', list(map(lambda x: [x], price)))

if __name__ == "__main__":
    for i in URLS:
        parser(i)
    upd_gvozdemet()
