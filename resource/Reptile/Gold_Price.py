'''
Name：黄金API接口获取au9999 / agTplusD数据
Writer：wjl
date：2021.10.11
Using：黄金API接口获取数据，黄金类别有：au9999 与 agTplusD
Input： url # <class 'str'> 域名
Output： pro_data # <class 'dict'> 黄金最新数据 / today.json # json文件
'''

import json
import re
import requests
import datetime


# 抓取网页
def get_html(url: str):
    response = requests.get(url)  # 发送GET请求,得到响应数据response
    # CHECK
    print('今日黄金价格响应码：', response.status_code)  # 返回响应码，200为正常，有数据返回

    try:
        response.raise_for_status()   # 判断response返回值是否为200
        response.encoding = 'utf-8'

        json_data=json.loads(response.text)
        # CHECK
        print('Json loads Successfully!')

        return json_data   # <class 'list'>
    except:
        print('<Response: %s >' % response.status_code)  # 如果发生错误，则返回响应码


# 处理数据
def data_process(json_data: dict):
    pro_data = dict()  # 创建list型数据结构

    if not json_data:
        print('Failed to process data!')
        return None

    # 遍历黄金型号
    for i in range(16):
        pro_data[json_data['result'][0][str(i + 1)]['variety']] = {
            '最新价格': json_data['result'][0][str(i + 1)]['latestpri'],
            '开盘价格': json_data['result'][0][str(i + 1)]['openpri'],
            '最高价格': json_data['result'][0][str(i + 1)]['maxpri'],
            '最低价格': json_data['result'][0][str(i + 1)]['minpri'],
            '涨跌幅度': json_data['result'][0][str(i + 1)]['limit'],
            '昨日收盘价': json_data['result'][0][str(i + 1)]['yespri'],
            '总成交量': json_data['result'][0][str(i + 1)]['totalvol'],
            '更新时间': json_data['result'][0][str(i + 1)]['time']
        }

    return pro_data


def Gold_Main():
    today = datetime.date.today().strftime('%Y%m%d')  # 实时保存
    # %Y 四位数的年份表示（000-9999）
    # %m 月份（01-12）
    # %d 月内中的一天（0-31）

    # 原始数据网页API
    json_data = get_html('http://web.juhe.cn/finance/gold/shgold?key=f450d3f3ce7a40cade056c1623b9b4b7')   # &prov=au999,agTplusD
    pro_data = data_process(json_data)

    # 打开一个文件并且保证该文件会被关闭。
    # 创建一个Gold文件夹，该文件夹下生成一个 当天Gold的json文件
    with open('../OUTPUT/Gold/Gold&' + today + '.json', 'w', encoding='utf-8') as file:
        json.dump(pro_data, file, ensure_ascii=False)
    # CHECK
    print('Writing in the Gold json file succeeded!')     # 标识已经将黄金数据写入json文件


if __name__ == '__main__':
    Gold_Main()







