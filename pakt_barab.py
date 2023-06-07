# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials
import gspread

credentials_file = 'ultimate-result-371107-04a8a2effdde.json'

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
gc = gspread.authorize(credentials)
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1rrACEEX1ZUq8z0YRicwFvMHO1Ro6SbKwb75prGDVZK0'
worksheet = gc.open_by_url(spreadsheet_url).worksheet("Pakt-group")


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
    pager = soup.find('div', class_='pager pager2 buttons-switcher')
    if pager is None:
        return 1
    else:
        pages = int(pager.find('a', class_='item pnav-shownext')['data-num-all']) // 20 + 1
        return pages

def get_content(html):
    """сбор контента со страницы"""
    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find_all('li', {'class': 'lta-item position- image-position- catalog-group-list73'})
    link = []
    art = []
    name = []
    fas = []
    price = []
    in_stock = []
    for item in items:
        link.append('https://www.pakt-group.ru' + item.find('div', class_='catalog-model-name catalog-list-tile-name').a.get('href'))
        art.append(item.find('div', class_='catalog-item-code-list').get_text(strip=True))
        name.append(item.find('div', class_='catalog-model-name catalog-list-tile-name').a.get_text(strip=True))
        fas.append(item.div.find('ul', class_='catalog-list-base-params').get_text(strip=True).replace(' ', '').replace('штуквупаковке', ''))

        price_elem = item.find('div', class_='price model-price')
        price_text = price_elem.find('span', class_='price-propria').text.strip() if price_elem else ''
        price_value = ''.join(filter(str.isdigit, price_text))
        price.append(price_value)

        in_stock_elem = item.find('span', class_='catalog-status-d')
        in_stock_text = in_stock_elem.text.strip() if in_stock_elem else ''
        in_stock.append(in_stock_text)
    return link, art, name, fas, price, in_stock



def parser(url):
    """парсер"""
    html = get_html(url)
    if html.status_code == 200:
        pages = get_pages(html)
        print(f'Всего страниц: {pages}')
        data = []
        for page in range(1, pages + 1):
            print(f'Парсинг страницы: {page}')
            html = get_html(url, params={'page': page})
            content = get_content(html)
            data.extend(list(zip(*content)))
        data = [[str(value) if value is not None else '' for value in row] for row in data]
        cell_range = f"A2:F{len(data)+1}"
        cell_list = worksheet.range(cell_range)
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                cell_list[i * len(row) + j].value = value
        worksheet.update_cells(cell_list, value_input_option='USER_ENTERED')
        print(f'Всего: {len(data)} позиций')
    else:
        print(f'Ответ сервера: {html.status_code}. Парсинг невозможен!')




if __name__ == "__main__":
    parser('https://www.pakt-group.ru/catalog/barabannie-gvozdi/c1690/')

