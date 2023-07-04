
import requests
from bs4 import BeautifulSoup


headers = {'Accept':
               'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
           'User-Agent':
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
           }

url = 'https://alpari-online.com/ru/markets/cbr/kurs-kzt-kazahskij-tenge/'


def find_price(url):
    req = requests.get(url=url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    euro_price = soup.find('span',
                           class_="-rdsn-markets-cbr-course-day__main -rdsn-markets-cbr-course-day__main_size-big")
    euro = euro_price.text
    euro = euro.replace(' ', '')
    euro = euro.replace('\n', '')
    euro = float(euro)
    return euro
