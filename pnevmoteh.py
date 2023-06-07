# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import gspread
import re

article = []
link = []
name = []
price = []

gc = gspread.service_account(filename='ultimate-result-371107-04a8a2effdde.json')
sheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/1rrACEEX1ZUq8z0YRicwFvMHO1Ro6SbKwb75prGDVZK0')
worksheet = sheet.worksheet("Pnevmoteh")
worksheet.batch_clear(["A2:D250"])


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
        good_count = soup.find('li', class_='pager-item').get_text(strip=True)
        pages = int(good_count) // 100 + 1
    except:
        pages = -1
    return pages

def get_content(html):
    """сбор контента со страницы"""
    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find_all('div', {'class': 'pr__card-inner in-stock'})
    try:
        for item in items:
            article.append(int(item.find('div', class_='pr__card-code').span.get_text(strip=True)))
            link.append(item.find('div', class_='pr__card-title').a.get('href'))
            name.append(item.find('div', class_='pr__card-title').a.get_text(strip=True)),
            price.append(item.find('div', class_='benefit-info').dd.get_text(strip=True).replace('\xa0', '').replace('RUB', '').replace(' ', ''))
    except AttributeError:
        for item in items:
            article.append(int(item.find('div', class_='pr__card-code').span.get_text(strip=True)))
            link.append(item.find('div', class_='pr__card-title').a.get('href'))
            name.append(item.find('div', class_='pr__card-title').a.get_text(strip=True)),
            price.append(item.find("div", class_='pr__card-price').span.get_text(strip=True).replace('\xa0', ''))



def f(lst, n):
    return [lst[i:i + n] for i in range(0, len(lst), n)]


def parser(url):
    """основная функция"""
    print(f'Парсим данные с: "{url}"')
    html = get_html(url)
    if html.status_code == 200:
        pages = get_pages(html)
        for page in range(0, pages + 8): #8
            print(f'Парсинг страницы: {page}')
            html = get_html(url, params={'page': page})
            get_content(html)
        worksheet.update('A2', f(article, 1))
        worksheet.update('B2', f(link, 1))
        worksheet.update('C2', f(name, 1))
        worksheet.update('D2', f(price, 1))
    else:
        print(f'Ответ сервера:{html.status_code}. Парсинг невозможен!')



if __name__ == "__main__":
    parser('https://www.pnevmoteh.ru/barabannye-gvozdi')








    # a = 2
    # s = 2
    # b = 2
    # c = 2
    # for i0 in article:
    #     worksheet.update(f'A{a}', i0)
    #     time.sleep(1)
    #     a += 1
    # for i in link:
    #     worksheet.update(f'B{s}', i)
    #     time.sleep(1)
    #     s += 1
    # for i2 in name:
    #     worksheet.update(f'C{b}', i2)
    #     time.sleep(1)
    #     b += 1
    # for i3 in price:
    #     worksheet.update(f'D{c}', i3)
    #     time.sleep(1)
    #     c += 1