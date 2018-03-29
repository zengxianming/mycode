import requests
from bs4 import BeautifulSoup

# 爬取课题组网址
def find_ktz():
    url = 'http://tjjt.tongji.edu.cn/index.php?classid=9394'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    ktz_links = soup.select('#announcement_roll > ul > li > a')

    with open('C:\\Users\\D\\Desktop\\同济交运课题组网站.csv', 'w') as csv:
        csv.write('name,link\n')
        for link in ktz_links:
            title = link.get_text()
            href = link.get('href')
            csv.write(
                ','.join(
                    [
                        title,
                        href
                    ]
                ) + '\n'
            )

# 爬取教师信息
def find_professor():
    url = 'http://tjjt.tongji.edu.cn/index.php?classid=9402'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')



