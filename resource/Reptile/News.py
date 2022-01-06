'''
Name：新闻API接口获取数据
Writer：山客
date：2021.10.9
Using：新闻API接口获取数据
Input： url # <class 'str'> 域名
Output： pro_data # <class 'dict'> 新闻最新数据 / today.json # json文件
Tips：部分注释参照 COVID19.py
'''

import json  # 轻量级数据交换格式
import re  # 正则表达式
import requests  # 简易 HTTP 库
import datetime


# 爬取网页
def get_html(url: str):
    response = requests.get(url)

    # CHECK
    print('新闻API接口网页响应码：', response.status_code)

    try:
        response.raise_for_status()
        response.encoding = 'utf-8'

        json_data = json.loads(response.text)
        # CHECK
        print('Json loads Successfully!')

        return json_data
    except:
        print('<Response: %s >' % response.status_code)


# 处理数据
def data_process(json_data: dict):
    pro_data = list()
    cnt = 1

    if not json_data:
        print('Failed to process data!')
        return None

    tmps = json_data['newslist']
    for tmp in tmps:
        pro_data.append({
            '新闻编号': cnt,
            '新闻标题': tmp['title'],
            '新闻内容': tmp['description']
        })
        cnt += 1

    return pro_data


def News_Main():
    today = datetime.date.today().strftime('%Y%m%d')  # 实时保存
    # %Y 四位数的年份表示（000-9999）
    # %m 月份（01-12）
    # %d 月内中的一天（0-31）

    json_data = get_html('http://api.tianapi.com/topnews/index?key=68cbbcecad11235224ded74b30d15927')
    pro_data = data_process(json_data)

    # 打开一个文件并且保证该文件会被关闭。
    # 创建一个Gold文件夹，该文件夹下生成一个 当天Gold的json文件
    with open('../OUTPUT/News/News&' + today + '.json', 'w', encoding='utf-8') as file:
        json.dump(pro_data, file, ensure_ascii=False)
    # CHECK
    print('Writing in the News json file succeeded!')     # 标识已经将新闻数据写入json文件


if __name__ == '__main__':
    News_Main()
