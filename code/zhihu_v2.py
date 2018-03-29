import json
import requests
import time
import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
    'Cookie': '_zap=e06beca8-088b-44db-b72e-80599bdaa80d; d_c0="AIAC9w0iuwyPTmO6yHiurlfWnI1UXdxtQSE=|1511496714"; __utma=51854390.2024113287.1519484755.1519484755.1519484755.1; __utmz=51854390.1519484755.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=51854390.110-1|2=registration_date=20150622=1^3=entry_date=20150622=1; capsion_ticket="2|1:0|10:1519487310|14:capsion_ticket|44:OGJkMzU1ZDFmNTAyNDZiNTlkZGQ0YTQ2YjUzZDIxOGE=|03fdd00dcefbbffda22e6a4f5aee11f0ee6e82f9aef287c3e543120caac67c7a"; z_c0="2|1:0|10:1519487367|4:z_c0|92:Mi4xcVFETUFRQUFBQUFBZ0FMM0RTSzdEQ1lBQUFCZ0FsVk5oOWQtV3dEdnJIZndIZjkzMjNRODRCRlpsMVluSC0yQ2NB|b8c4703d8fe6ea5165676bb28cbd13645c71a6481cedc7919c5b82990879886d"; q_c1=a88b6273b9ce48a783fbfe88c9a9f4f9|1519612729000|1511347384000; aliyungf_tc=AQAAABbMVhqvXAUAHOU3O+o8G1C9RnuT; _xsrf=ede75c90-aa47-4448-864b-e3ab40ed66f0'
}

form_data = {
    'include': 'data[*].created,answer_count,follower_count,author',
    'offset': 0,
    'limit': 20
}


def get_info(form_data):
    data = []
    url = 'https://www.zhihu.com/api/v4/members/yan-xi-5-31/following-questions'
    response = requests.get(url, headers=headers, data=form_data)
    json_dir = json.loads(response.text)
    for info in json_dir['data']:
        find = {
            'title': info['title'],
            'created': str(datetime.datetime.fromtimestamp(info['created'])),
            'updated_time': str(datetime.datetime.fromtimestamp(info['updated_time'])),
            'follower_count': str(info['follower_count']),
            'answer_count': str(info['answer_count']),
            'site': info['url']
        }
        data.append(find)
    time.sleep(2)
    return data


if __name__ == '__main__':
    all_data = []
    for offset in range(0, 420, 20):
        form_data['offset'] = offset
        all_data.extend(get_info(form_data))

    with open('C:\\Users\\D\\Desktop\\zhihu.csv', 'w') as csv_file:
        csv_file.write('title,created,updated_time,follower_count,answer_count,site\n')
        for zhihu in all_data:
            csv_file.write(','.join([
                                        zhihu['title'],
                                        zhihu['created'],
                                        zhihu['updated_time'],
                                        zhihu['follower_count'],
                                        zhihu['answer_count'],
                                        zhihu['site']]) + '\n'
                                    )


