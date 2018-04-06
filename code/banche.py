from numpy import *
from matplotlib.pyplot import *
import matplotlib as plt
import pandas as pd
import seaborn as sns
import re
import os

sns.set()


# path = 'C:\\Users\\D\\Desktop\\banche\\'
# for name in os.listdir(path):
#     os.rename(path+name, path + name[1:])
#
# def df_add_time(df):
#     df = df[['UID', 'rectime', 'year', 'date1', 'time', 'time1', 'speed','longitude', 'latitude', 'location', 'LID']]
#     # 处理日期
#     def f(x):
#         sp = x.split('/')
#         y = sp[-1]
#         m = sp[0]
#         d = sp[1]
#         if len(m)==1:
#             m = '0'+ m
#         if len(d)==1:
#             d = '0' + d
#         return int(y+m+d)
#     df['rdate'] = df.rectime.apply(f)
#     # 处理时间
#     def f(x):
#         sp = re.split(':| ',x)
#         h = sp[0]
#         m = sp[1]
#         s = sp[2]
#         if sp[3] == 'PM':
#             if not int(h) == 12:
#                 h = str(int(h) + 12)
#         else :
#             if int(h) == 12:
#                 h = str(int(h) - 12)
#         return int(h + m+ s)
#     df['rtime'] = df.time.apply(f)
#     df = df.drop(labels=['time1','date1','UID'],axis=1)
#     return df


def find_path(df, name):
    Dic = {'start_index': [], 'end_index': [], 'date': [], 'start_time': [], 'start_lid': [], 'end_time': [],
           'end_lid': [], 'caoyang': []}
    dates = df.rdate.unique()
    for date in dates:
        m = df[df.rdate == date]
        m = m.reset_index()
        lid = array(m.LID.tolist())
        trip = np.where(lid == 0)[0]

        # 得到一天的出行次数
        from itertools import groupby
        dic = {}
        last_index = -1000
        fun = lambda x: x[1] - x[0]
        for key, group in groupby(enumerate(trip), fun):
            lst = [v for i, v in group]
            if len(lst) > 60:
                if lst[0] - last_index < 30:
                    dic[last_key].extend(lst)
                else:
                    dic[key] = lst
                    last_key = key
                    last_index = lst[-1]

        # 画图为了后续检验比较纠错有几条明显折线就有几次出行
        figure(figsize=(6, 6))
        axis('off')
        plot(trip)
        savefig('F:\\xiaochefig\\{}-{}-{}.jpg'.format(name[0:-4], date, len(dic)))

        # 找到对应起终点路径
        # 出发到达时间 出发到达位置 是否经过曹阳
        for key in dic.keys():
            start_index = dic[key][0]
            end_index = dic[key][-1]
            while 1:
                if m.loc[start_index].speed == 0 and m.loc[start_index].LID in [1, 2, 3]:
                    start_time = m.loc[start_index].rtime
                    start_lid = m.loc[start_index].LID
                    break
                else:
                    start_index = start_index - 1
                    if start_index <= 0:
                        start_time = NaN
                        start_lid = NaN
                        print("_________something wrong in start!______")
                        print(m.loc[dic[key][0]])
                        print("________________________________________")
                        break
            while 1:
                if m.loc[end_index].speed == 0 and m.loc[end_index].LID in [1, 2, 3]:
                    end_time = m.loc[end_index].rtime
                    end_lid = m.loc[end_index].LID
                    break
                else:
                    end_index = end_index + 1
                    if end_index >= len(m):
                        end_time = NaN
                        end_lid = NaN
                        print("_________something wrong in end!______")
                        print(m.loc[dic[key][0]])
                        print("______________________________________")
                        break
            caoyang = 1 if 4 in m.loc[start_index:end_index].LID.unique() else 0
            Dic['start_index'].append(start_index)
            Dic['end_index'].append(end_index)
            Dic['date'].append(date)
            Dic['start_time'].append(start_time)
            Dic['start_lid'].append(start_lid)
            Dic['end_time'].append(end_time)
            Dic['end_lid'].append(end_lid)
            Dic['caoyang'].append(caoyang)
    return Dic


new_path = 'C:\\Users\\D\\Desktop\\banche1\\'
for name in os.listdir(new_path):
    df = pd.read_csv(new_path + name, encoding='gbk')
    Dic = find_path(df, name)
    info = pd.DataFrame(Dic)
    info['id'] = name[0:-4]
    info = info[
        ['id', 'date', 'start_index', 'end_index', 'start_time', 'start_lid', 'end_time', 'end_lid', 'caoyang']]
    info.to_csv('F:\\info\\{}.csv'.format(name), index=False)
