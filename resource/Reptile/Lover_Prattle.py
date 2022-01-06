'''
Name：情话API接口获取数据
Writer：wjl
date：2021.10.10
Using：情话API接口获取数据
Input： url # <class 'str'> 域名
Output： pro_data # <class 'dict'> 情话最新数据 / today.json # json文件
'''

import json
import re
import requests
import datetime


# 爬取网页
def get_html(url: str):
    response = requests.get(url)         # 发送GET请求,得到响应数据response

    # CHECK
    # print('今日情话响应码：', response.status_code)          # 返回响应码，200为正常，有数据返回
    try:
        # 够判断返回的Response类型状态是不是200。
        # 如果是200，他将表示返回的内容是正确的，如果不是200，他就会产生一个HttpError的异常。
        response.raise_for_status()
        response.encoding = 'utf-8'  # 设置编码格式utf-8

        json_data = json.loads(response.text)  # 将统一编码转化为python类型,作用对象是字符串。
        # CHECK
        # print('Json loads Successfully!')

        return json_data   # <class 'list'>
    except:
        print('<Response: %s >' % response.status_code)     # 如果发生错误，则返回响应码


def data_process(json_data: dict, pro_data: list):
    if not json_data:
        print('Failed to process data!')
        return None

    pro_data.append(json_data['newslist'][0]['content'])


def LoverPrattle_Main():
    today = datetime.date.today().strftime('%Y%m%d')  # 实时保存
    # %Y 四位数的年份表示（000-9999）
    # %m 月份（01-12）
    # %d 月内中的一天（0-31）

    pro_data = list()
    # 原始数据网页API
    for i in range(100):
        json_data = get_html('http://api.tianapi.com/txapi/saylove/index?key=68cbbcecad11235224ded74b30d15927')
        data_process(json_data, pro_data)   # 调用定义的数据处理函数

    # 打开一个文件并且保证该文件会被关闭。
    # 创建一个Gold文件夹，该文件夹下生成一个 当天Gold的json文件
    with open('../OUTPUT/LoverPrattle/Love&' + today + '.json', 'w', encoding='utf-8') as file:
        json.dump(pro_data, file, ensure_ascii=False)
    # CHECK
    print('Writing in the Lover Prattle json file succeeded!')     # 标识已经将情话数据写入json文件


if __name__ == '__main__':
    LoverPrattle_Main()

