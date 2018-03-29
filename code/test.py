# 爬取 标题 时间 回答数 关注数 网址
# find title time ans_num foc_num site


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

    titles = soup.select('div.QuestionItem-title')
    times = soup.find_all(text=re.compile(r"(\d{4}-\d{1,2}-\d{1,2})"))
    ans_nums = soup.find_all(text=re.compile("个回答"))
    foc_nums = soup.find_all(text=re.compile("个关注"))
    sites = soup.select('div.QuestionItem-title > a')

    for title, time, ans_num, foc_num, site in zip(titles, times, ans_nums, foc_nums, sites):
        ans = re.findall(r'\d+', ans_num)
        ans_num = 0
        for i in range(0, len(ans)):
            ans_num = pow(1000, len(ans) - i - 1) * int(ans[i]) + ans_num
        foc = re.findall(r'\d+', foc_num)
        foc_num = 0
        for i in range(0, len(foc)):
            foc_num = pow(1000, len(foc) - i - 1) * int(foc[i]) + foc_num
        data = {
            "title": title.get_text(),
            "time": time,
            "ans_num": ans_num,
            "foc_num": foc_num,
            "site": "https://www.zhihu.com/" + str(site.get('href'))
        }
        print(data)
    tm.sleep(4)

for url in urls:
    get_info(url)
