# title other text quote com_num rating_num
import requests
from bs4 import BeautifulSoup
import time
import re

urls = ['https://movie.douban.com/top250?start={}&filter='.format(str(i)) for i in range(0, 250, 25)]
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                  '64.0.3282.140 Safari/537.36',
    'Cookie': 'bid=XYklAs7eYB8; viewed="2075915"; gr_user_id=9890e3d8-5be2-4b51-b4a8-c8f6f23843d1; __'
              'utmz=30149280.1516200726.4.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _'
              'pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1519569105%2C%22http%3A%2F%2Flink.'
              'zhihu.com%2F%3Ftarget%3Dhttp%253A%2F%2Fmovie.douban.com%2Ftop250%22%5D; _pk_ses.100001.4cf6'
              '=*; __yadk_uid=C1gkhbJJK1vPlc6YxiVvGVT5mJDntixo; __utma=30149280.1751264912.1512616682.15162'
              '00726.1519569676.5; __utmb=30149280.0.10.1519569676; __utmc=30149280; __utma=223695111.174879'
              '2497.1519569676.1519569676.1519569676.1; __utmb=223695111.0.10.1519569676; __utmc=223695111; __'
              'utmz=223695111.1519569676.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _pk_id.100001.4cf'
              '6=72b54b746756a10b.1519569105.1.1519569716.1519569105.'

}


def get_movies_info(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    titles = soup.select('span.title')
    others = soup.select('span.other')
    texts = soup.select('div.bd > p.')
    quotes = soup.select('span.inq')
    com_nums = soup.find_all(text=re.compile(r"人评价"))
    rating_nums = soup.select('span.rating_num')

    all_data = []
    for title, other, text, quote, com_num, rating_num in zip(titles, others, texts, quotes, com_nums, rating_nums):
        data = {
            'title': ' '.join(title.get_text().split()),
            'other': ' '.join(other.get_text().split()),
            'text': ' '.join(text.get_text().split()),
            'quote': ' '.join(quote.get_text().split()),
            'com_num': re.findall(r'\d+', com_num)[0],
            'rating_num': rating_num.get_text()
        }
        all_data.append(data)
    return all_data
    time.sleep(2)


if __name__ == '__main__':
    movies = []
    for url in urls:
        movies.extend(get_movies_info(url))
        print('get '+ url)
    with open('C:\\Users\\D\\Desktop\\movies.csv', 'w', encoding='utf-8') as csv_file:
        csv_file.write('title,other,text,quote,com_num,rating_num\n')
        for movie in movies:
            csv_file.write(','.join([
                movie['title'],
                movie['other'],
                movie['text'],
                movie['quote'],
                movie['com_num'],
                movie['rating_num']
            ]) + '\n')