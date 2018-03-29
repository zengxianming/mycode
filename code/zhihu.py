# title time ans_num foc_num site

from bs4 import BeautifulSoup
import requests
import time as tm
import re

urls = ['https://www.zhihu.com/people/yan-xi-5-31/following/questions?page={}'.format(str(i)) for i in range(1, 22)]
headers = {
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'aliyungf_tc=AQAAALlHnAa9hwYAgxkFajTTLlmNTUws; d_c0="AEBthFTRMA2PTl_q8JcaDUEOWBCASvcN_Fo=|1519394399"; _xsrf=59a447e1-9a1f-4b04-b72a-46d1593e8b9c; q_c1=f20a23e1db6641b2af6c9ee3d1f65a8f|1519394399000|1519394399000; _zap=770526c5-761f-49c1-8d14-d04a42640566',
    'Host': 'www.zhihu.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
}


def get_info(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    titles = soup.select('div.QuestionItem-title > a')
    times = soup.find_all(text=re.compile(r'\d{4}-\d{2}-\d{2}'))
    ans_nums = soup.find_all(text=re.compile("个回答"))
    foc_nums = soup.find_all(text=re.compile("个关注"))
    sites = soup.select('div.QuestionItem-title > a')

    for title, time, ans_num, foc_num, site in zip(titles, times, ans_nums, foc_nums, sites):
        def f(all):
            sum = 0
            for i, a in enumerate(all):
                sum = sum + pow(1000, len(all) - i - 1) * int(a)
            return sum

        data = {
            'title': title.get_text(),
            'time': time,
            'ans_num': f(re.findall(r'\d+', ans_num)),
            'foc_num': f(re.findall(r'\d+', foc_num)),
            'site': 'https://www.zhihu.com' + site.get('href')
        }
        print(data)
    tm.sleep(4)

get_info('https://www.zhihu.com/people/yan-xi-5-31/following/questions?page=1')
