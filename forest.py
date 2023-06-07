# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import gspread



link = []
name = []
price = []

gc = gspread.service_account(filename='ultimate-result-371107-04a8a2effdde.json') # подключаем файл с ключами и пр.
sheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/1rrACEEX1ZUq8z0YRicwFvMHO1Ro6SbKwb75prGDVZK0') # подключаем таблицу по ID
worksheet = sheet.worksheet("Forest")
worksheet.batch_clear(["A2:C100"])

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

def num_of_pages(url):
    try:
        response = requests.get(url).text
        soup = BeautifulSoup(response, 'lxml')
        max_page = soup.find('div', class_='module-pagination')
        obl = int(max_page.find_all('a')[-1].text)
        return obl
    except IndexError:
        return 1

def get_content(html):
    """сбор контента со страницы"""
    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find_all('div', {'class': 'catalog_item_wrapp item'})

    for item in items:
        link.append('https://www.for-est.ru' + item.find('a', class_='dark_link').get('href'))
        name.append(item.find('div', class_='item-title').get_text(strip=True)),
        price.append(item.find('span', class_='price_value').get_text(strip=True).replace(' ',''))


def f(lst, n):
    return [lst[i:i + n] for i in range(0, len(lst), n)]

def parser(url):
    """основная функция"""
    print(f"Парсим данные с: '{url}'")
    html = get_html(url)
    s = num_of_pages(url)
    if html.status_code == 200:
        pages = get_pages(html)
        for page in range(1, pages + s):
            print(f'Парсинг страницы: {page}')
            html = get_html(url, params={'PAGEN_1': page})
            get_content(html)
        worksheet.update('A2', f(link, 1))
        worksheet.update('B2', f(name, 1))
        worksheet.update('C2', f(price, 1))
    else:
        print(f'Ответ сервера:{html.status_code}. Парсинг невозможен!')




if __name__ == "__main__":
    parser('https://www.for-est.ru/catalog/krepezh/gvozd/barabannye_gvozdi/index.php?display=block')



    #     s = 2
    #     b = 2
    #     c = 2
    # for i in link:
    #     worksheet.update(f'A{s}', i)
    #     time.sleep(1)
    #     s+=1
    # for i2 in name:
    #     worksheet.update(f'B{b}', i2)
    #     time.sleep(1)
    #     b+=1
    # for i3 in price:
    #     worksheet.update(f'C{c}', i3)
    #     time.sleep(1)
    #     c+=1
