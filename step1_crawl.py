import requests
import bs4
import os
import re


def download_titles(url, fn):
    print(url, '->', fn)
    html = requests.get(url).content.decode()
    soup = bs4.BeautifulSoup(html, 'html.parser')

    with open(fn, 'a', encoding='utf8') as f:
        titles = soup.find_all('dt')
        if len(titles) > 0:
            print(len(titles))
            for title in titles:
                print(title.get_text(), file=f)
        else:
            days = soup.find_all(text=re.compile(r"^Day \d: "))
            for day in days:
                sub_url = 'https://openaccess.thecvf.com/' + day.parent['href']
                download_titles(sub_url, fn)


def read_urls_from_home_page():
    url = 'https://openaccess.thecvf.com/menu'
    html = requests.get(url).content.decode()
    soup = bs4.BeautifulSoup(html, 'html.parser')
    for mc in soup.find_all(text='Main Conference'):
        href = mc.parent['href']
        yield 'https://openaccess.thecvf.com/' + href


for url in read_urls_from_home_page():
    fn = os.path.splitext(os.path.basename(url))[0] + '.txt'
    download_titles(url, fn)
