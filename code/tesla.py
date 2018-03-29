# reference ： https://github.com/sdroadie/supercharger-distance
from bs4 import BeautifulSoup
import requests
import time
import re


def _str(s):
    if s is None:
        return ''
    else:
        return str(s)


response = requests.get('https://www.teslamotors.com/findus/list/superchargers/United+States')
supercharger_html = response.text
soup = BeautifulSoup(supercharger_html, 'html.parser')
superchargers_markup = soup.select('.vcard')
superchargers = []

l = len(superchargers_markup)
for i, s in enumerate(superchargers_markup):
    address = ', '.join(
        filter(lambda s: len(s) > 0,
               map(_str,
                   [s.select_one('.street-address').string,
                    s.select_one('.extended-address').string])))
    locality = s.select_one('.locality').string
    url = s.findAll('a')
    url = url[0]['href']
    son_url = "https://www.tesla.com/" + url

    full_address = ', '.join([address, locality])
    print(full_address)
    son_response = requests.get(son_url)
    son_superchargers_html = son_response.text
    son_soup = BeautifulSoup(son_superchargers_html, 'html.parser')
    s1 = son_soup.find_all('img')
    print(str(s1))
    try:
        q = re.findall(r'er=(.+?).+zoom', str(s1))[0]
        lat = str(q[0])
        long = str(q[1])
    except IndexError:
        lat = str(0)
        long = str(0)

    try:
        son_superchargers_markup = son_soup.select('.vcard')
        son_s = son_superchargers_markup[0]
        chargers_num = re.findall(r'\d.+kW', str(son_s))[0]
        num = re.findall(r'(\d).+kW', str(son_s))[0]
    except IndexError:
        chargers_num = 'coming soon'
        num = ''
    time.sleep(0.1)
    if i % 100 == 0:
        time.sleep(10)

    location_map = {'address': address, 'locality': locality, 'lat': lat, 'long': long,
                    'chargers_num': num, 'detail': chargers_num}
    print('%s : %s' % (i, l))
    print(location_map)
    superchargers.append(location_map)

with open('C:\\Users\\D\\Desktop\\full_superchargers.csv', 'w') as csv_file:
    # Write legend row.
    csv_file.write('address,locality,lat,long,chargers_num,detail\n')
    for s in superchargers:
        csv_file.write(','.join([
            s['address'],
            s['locality'],
            s['lat'],
            s['long'],
            s['chargers_num'],
            s['detail']]) + '\n')


