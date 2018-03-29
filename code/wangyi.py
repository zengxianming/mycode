# coding=utf8
# Benjamin

import pandas as pd
import requests
from bs4 import BeautifulSoup

response = requests.get('http://music.163.com/#/user/home?id=108192250',)
soup = BeautifulSoup(response.text, 'lxml')
print(soup)
# titles = soup.select(r'#\34 458674071521982596614 > div.song > div.tt > div > span > a > b')
# for i in titles:
#     print(i)

# \34 458674071521982596614 > div.song > div.tt > div > span > a > b
