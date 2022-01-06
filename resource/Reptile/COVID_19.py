'''
Name：新冠疫情（COVID - 19）国内数据爬虫
Writer：山客
date：2021.10.9
Using：新冠疫情（COVID - 19）国内数据爬虫
Input： url # <class 'str'> 域名
Output： pro_data # <class 'dict'> 处理后的各地疫情最新数据 / today.json # json文件
'''


import json  # 轻量级数据交换格式
import re  # 正则表达式
import requests  # 简易 HTTP 库
import datetime


# 抓取网页
def get_html(url: str):
    response = requests.get(url)  # 发送 GET 请求

    # CHECK
    print('新冠疫情爬虫网页响应码：', response.status_code)  # 返回响应码，200为正常并有数据返回

    try:
        url_text = response.content.decode()  # 获取响应的 html 页面

        # 匹配字符串
        # re.S：逐行匹配，这一行匹配结束，自动匹配下一行
        url_content = re.search(r'window.getAreaStat = (.*?)}]}catch',
                                url_text, re.S)
        texts = url_content.group()  # 获取匹配后整体结果

        # 整理结果，去掉多余字符
        content = texts.replace('window.getAreaStat = ', '').replace('}catch', '')

        json_data = json.loads(content)  # 转换数据格式
        # CHECK
        print('Json loads Successfully!')

        return json_data  # <class 'list'>
    except:
        print('<Response: %s >' % response.status_code)


# 数据处理
def data_process(json_datas: list):
    pro_data = dict()

    if not json_datas:
        print('Failed to process data!')
        return None

    for json_data in json_datas:
        pro_data[json_data['provinceName']] = {
            "地点编号"  : json_data['locationId'],
            "目前确诊数": json_data['currentConfirmedCount'],
            "总确诊数"  : json_data['confirmedCount'],
            "疑似病例数": json_data['suspectedCount'],
            "治愈病例数": json_data['curedCount'],
            "死亡病例数": json_data['deadCount']
        }

    return pro_data


def COVID_Main():
    today = datetime.date.today().strftime('%Y%m%d')  # 实时保存

    json_data = get_html('https://ncov.dxy.cn/ncovh5/view/pneumonia')  # 原始数据
    pro_data = data_process(json_data)  # 处理数据

    # 打开一个文件并且保证该文件会被关闭。
    # 创建一个Gold文件夹，该文件夹下生成一个 当天Gold的json文件
    with open('Covid19&' + today + '.json', 'w', encoding='utf-8') as file:
        json.dump(pro_data, file, ensure_ascii=False)
    # CHECK
    print('Writing in the COVID json file succeeded!')     # 标识已经将疫情数据写入json文件


if __name__ == '__main__':
    COVID_Main()
