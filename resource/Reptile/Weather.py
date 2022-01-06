'''
Name：天气预报数据爬虫（中国天气网）34省份
Writer：山客
date：2021.10.10
Using：爬取全国31省份天气概况，如最高温度、最低温度、天气现象、风向等
Input： url # <class 'str'> 域名
Output： pro_data # <class 'dict'> 处理后的各地天气最新数据 / today.json # json文件
Tips：因技术原因，港澳台的数据尚未处理成功
'''


import requests  # 简易 HTTP 库
import datetime
from bs4 import BeautifulSoup
from lxml import html
import json
import re


# 爬取网页
def get_html(url: str, cnt: int):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
    }  # 'Referer': 'http://www.weather.com.cn/textFC/hb.shtml'

    response = requests.get(url=url, headers=headers)
    # CHECK
    print('天气预报爬虫网页响应码：', response.status_code)  # 返回响应码，200为正常并有数据返回

    try:
        url_text = response.content.decode('utf-8')  # 获取响应的 html 页面，格式为 utf-8

        # 解析网页
        url_soup = BeautifulSoup(url_text, 'lxml')   # <class 'bs4.BeautifulSoup'>
        # 每一个 table 是一个省份，里面还有若干城市
        # 获取的是当天的天气信息
        if cnt == 1:
            url_tables = url_soup.find_all('table')[:5]  # <class 'list'>
        elif cnt == 2:
            url_tables = url_soup.find_all('table')[:3]
        elif cnt == 3:
            url_tables = url_soup.find_all('table')[:7]
        elif cnt == 4:
            url_tables = url_soup.find_all('table')[:3]
        elif cnt == 5:
            url_tables = url_soup.find_all('table')[:3]
        elif cnt == 6:
            url_tables = url_soup.find_all('table')[:5]
        elif cnt == 7:
            url_tables = url_soup.find_all('table')[:5]

        return url_tables
    except:
        print('<Response: %s >' % response.status_code)


# 处理数据
def data_process(url_tables: list, cnt: int):
    pro_data = list()  # 处理后的数据

    isProvince = True  # 省份标识

    try:
        # 遍历每个省份
        for url_table in url_tables:
            trs = url_table.find_all('tr')[2:]  # 省份中的每个地区, tr 为 html 的格式块

            # 遍历每个地区
            for tr in trs:
                tds = tr.find_all('td')  # 城市地区信息，包括地名、天气

                if isProvince:
                    # 获取城市名：如北京、天津、佛山、广州等
                    city_td = tds[1]  # 提取第二个td，一般是地区名
                    city_name = list(city_td.stripped_strings)[0]  # stripped_strings这个方法可以对文本中的空格行进行删除只提取出其中的文字信息

                    # 获取天气现象
                    weather_td = tds[2]
                    weather_phenomenon = list(weather_td.stripped_strings)[0]
                else:
                    # 获取城市名
                    city_td = tds[0]
                    city_name = list(city_td.stripped_strings)[0]

                    # 获取天气现象
                    weather_td = tds[1]
                    weather_phenomenon = list(weather_td.stripped_strings)[0]

                # 获取最高温度
                temp_max_td = tds[-5]
                temp_max = list(temp_max_td.stripped_strings)[0]

                # 获取最低温度
                temp_min_td = tds[-2]
                temp_min = list(temp_min_td.stripped_strings)[0]

                # 获取城市编号：
                city_id_a = tr.find_all('a')
                if isProvince:
                    city_id = str(list(city_id_a)[2])[44:52]
                    isProvince = False
                else:
                    city_id = str(list(city_id_a)[1])[44:52]

                # 整合数据
                pro_data.append({
                    city_name: {
                        '城市编号': city_id,
                        '天气现象': weather_phenomenon,
                        '最高温度': temp_max,
                        '最低温度': temp_min
                    }
                })

            isProvince = True

        return pro_data
    except:
        print('<Process: 400 >')


def Weather_Main():
    today = datetime.date.today().strftime('%Y%m%d')  # 实时保存

    # 七大地区：华北、东北、华东、华中、华南、西北、西南
    urls = [
        'http://www.weather.com.cn/textFC/hb.shtml',
        'http://www.weather.com.cn/textFC/db.shtml',
        'http://www.weather.com.cn/textFC/hd.shtml',
        'http://www.weather.com.cn/textFC/hz.shtml',
        'http://www.weather.com.cn/textFC/hn.shtml',
        'http://www.weather.com.cn/textFC/xb.shtml',
        'http://www.weather.com.cn/textFC/xn.shtml',
    ]
    pro_data = list()

    cnt = 0
    for url in urls:
        cnt += 1

        url_tables = get_html(url, cnt)
        try:
            pro_data += data_process(url_tables, cnt)
        except:
            pass

        if cnt == 8:
            cnt = 0

    # 打开一个文件并且保证该文件会被关闭。
    # 创建一个Gold文件夹，该文件夹下生成一个 当天Gold的json文件
    with open('../OUTPUT/Weather/Weather&' + today + '.json', 'w', encoding='utf-8') as file:
        json.dump(pro_data, file, ensure_ascii=False)
    # CHECK
    print('Writing in the Weather json file succeeded!')     # 标识已经将天气数据写入json文件


if __name__ == '__main__':
    Weather_Main()
