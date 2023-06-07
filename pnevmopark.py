# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import gspread

URLS = ['https://pnevmopark.ru/catalog/krepezh/gvozdi/gvozdi_barabannye_ne_otsinkovannye/?display=list&PAGEN_1=1',
        'https://pnevmopark.ru/catalog/krepezh/gvozdi/gvozdi_barabannye_ne_otsinkovannye/?display=list&PAGEN_1=2',
        'https://pnevmopark.ru/catalog/krepezh/gvozdi/gvozdi_barabannye_ne_otsinkovannye/?display=list&PAGEN_1=3',
        'https://pnevmopark.ru/catalog/krepezh/gvozdi/gvozdi_barabannye_ne_otsinkovannye/?display=list&PAGEN_1=4',
        'https://pnevmopark.ru/catalog/krepezh/gvozdi/gvozdi_barabannye_otsinkovannye/?display=list',
        ]

link = []
name = []
price = []
nal = []

gc = gspread.service_account(filename='ultimate-result-371107-04a8a2effdde.json')
sheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/1rrACEEX1ZUq8z0YRicwFvMHO1Ro6SbKwb75prGDVZK0')
worksheet = sheet.worksheet("Pnevmopark")
worksheet.batch_clear(["A2:C150"])


def get_html(url, params=None):
    """html код страницы"""
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
    }
    html = requests.get(url, headers=headers, params=params)
    return html

def get_pages(html):
    """получение количества страниц"""
    soup = BeautifulSoup(html.text, 'lxml')
    try:
        good_count = soup.find('div', class_='pagination').get_text(strip=True)
        pages = int(good_count) // 100 + 1
    except:
        pages = 1
    return pages

def get_content(html):
    """сбор контента со страницы"""
    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find_all('div', {'class': 'list_item_wrapp item_wrap item'})
    for item in items:
        link.append('https://pnevmopark.ru' + str(item.find('div', class_='desc_name').a.get('href')))
        name.append(item.find('div', class_='desc_name').span.get_text(strip=True)),
        price.append(item.find('div', class_='cost prices clearfix').get_text(strip=True).replace(' ', '').replace('руб.', '').replace('.', ''))
        nal.append(item.find('div', class_='wrapp_stockers').get_text(strip=True))

def f(lst, n):
    return [lst[i:i + n] for i in range(0, len(lst), n)]

def parser(url):
    """основная функция"""
    print(f'Парсим данные с: "{url}"')
    html = get_html(url)
    if html.status_code == 200:
        print(f'Парсинг страницы: 1')
        html = get_html(url)
        get_content(html)
    else:
        print(f'Ответ сервера:{html.status_code}. Парсинг невозможен!')


def upd():
    worksheet.update('A2', f(link, 1))
    worksheet.update('B2', f(name, 1))
    worksheet.update('C2', f(price, 1))
    worksheet.update('D2', f(nal, 1))

if __name__ == "__main__":
    for i in URLS:
        parser(i)

    worksheet.update('A2', f(link, 1))
    worksheet.update('B2', f(name, 1))
    worksheet.update('C2', f(price, 1))
    worksheet.update('D2', f(nal, 1))


