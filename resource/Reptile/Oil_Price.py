'''
Name：油价API接口获取数据
Writer：wjl
date：2021.10.10
Using：油价API接口获取数据
Input： url # <class 'str'> 域名
Output： pro_data # <class 'dict'> 油价最新数据 / today.json # json文件
'''

import json
import re
import requests
import datetime


# 抓取网页
def get_html(url: str):
    response = requests.get(url)  # 发送GET请求,得到响应数据response
    # CHECK
    print('今日油价响应码：', response.status_code)  # 返回响应码，200为正常，有数据返回

    try:
        response.raise_for_status()
        response.encoding='utf-8'
        json_data=json.loads(response.text)
        print('Json loads Successfully!')
        return json_data   # <class 'list'>
    except:
        print('<Response: %s >' % response.status_code)  # 如果发生错误，则返回响应码


# 处理数据
def data_process(json_data: dict):

    if not json_data:
        print('Failed to process data!')
        return None

    # 处理后的数据
    pro_data = [
        json_data['newslist'][0]['p0'],  # 0号汽油
        json_data['newslist'][0]['p89'],  # 89号汽油
        json_data['newslist'][0]['p92'],  # 92号汽油
        json_data['newslist'][0]['p95'],  # 95号汽油
        json_data['newslist'][0]['p98']  # 98号汽油
    ]

    return pro_data


def Oil_Main():
    today = datetime.date.today().strftime('%Y%m%d')  # 实时保存
    # %Y 四位数的年份表示（000-9999）
    # %m 月份（01-12）
    # %d 月内中的一天（0-31）

    # 原始数据网页API
    json_data = get_html('http://api.tianapi.com/txapi/oilprice/index?key=68cbbcecad11235224ded74b30d15927&prov=%E9%87%8D%E5%BA%86') # &prov=%E9%87%8D%E5%BA%86
    pro_data = data_process(json_data)   # 调用定义的数据处理函数

    # 打开一个文件并且保证该文件会被关闭。
    # 创建一个Gold文件夹，该文件夹下生成一个 当天Gold的json文件
    with open('../OUTPUT/Oil/Oil&' + today + '.json', 'w', encoding='utf-8') as file:
        json.dump(pro_data, file, ensure_ascii=False)
    # CHECK
    print('Writing in the Oil json file succeeded!')     # 标识已经将石油数据写入json文件


if __name__ == '__main__':
    Oil_Main()




