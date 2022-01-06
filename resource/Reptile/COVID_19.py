'''
Name：新冠疫情（COVID - 19）国内数据爬虫
Writer：山客
date：2022.1.5
Using：新冠疫情（COVID - 19）国内数据爬虫
Input： url # <class 'str'> 域名
Output： pro_data # <class 'dict'> 处理后的各地疫情最新数据 / today.json # json文件
'''


import json  # 轻量级数据交换格式
import re  # 正则表达式
from bs4 import BeautifulSoup
import requests  # 简易 HTTP 库
import datetime


# 抓取网页
def get_html(url: str):
    response = requests.get(url)  # 发送 GET 请求

    # CHECK
    print('新冠疫情爬虫网页响应码：', response.status_code)  # 返回响应码，200为正常并有数据返回

    try:
        url_text = response.content.decode('utf-8')  # 获取响应的 html 页面

        # 解析网页
        url_soup = BeautifulSoup(url_text, 'lxml')
        url_script = url_soup.find_all('script')[6]
        
        return url_script
    except:
        print('<Response: %s >' % response.status_code)


# 数据处理：仅提取需要的城市
def data_process(url_script: list, need_city: list):
    pro_data = list()

    # 匹配字符串
    # re.S：逐行匹配，这一行匹配结束，自动匹配下一行
    url_data = re.search(r'window.getAreaStat = (.*?)}]}catch',
        str(url_script), re.S)
    couple_text = url_data.group()  # 获取匹配后整体结果
    pro_text = couple_text.replace('window.getAreaStat = ', '').replace('}catch', '')

    pro_json = json.loads(pro_text)

    pro_cities = list()
    for province in pro_json:
        if province['provinceName'] in need_city:
            if province['provinceName'] == '广东省':
                pro_cities.append(province['cities'][0])
            else:
                pro_cities.append(province)

    for city in pro_cities:
    	tmp = dict()
    	
    	try: 
    		if city['cityName'] == '广州':
    			tmp['City'] = '广州'
    	except:
    		tmp['City'] = city['provinceName']

    	tmp['目前确认数'] = city['currentConfirmedCount']
    	tmp['累计确诊数'] = city['confirmedCount']
    	tmp['疑似病例数'] = city['suspectedCount']
    	tmp['累计治愈数'] = city['curedCount']
    	tmp['累计死亡数'] = city['deadCount']
    	tmp['高危险数']   = city['highDangerCount']
    	tmp['中危险数']   = city['midDangerCount']

    	pro_data.append(tmp)
    	

    return pro_data


def COVID_Main():
    today = datetime.date.today().strftime('%Y%m%d')  # 实时保存

    need_city = ['广东省', '香港', '澳门']

    url_script = get_html('https://ncov.dxy.cn/ncovh5/view/pneumonia')  # 原始数据
    pro_data = data_process(url_script, need_city)  # 处理数据

    # 打开一个文件并且保证该文件会被关闭。
    # 创建一个Gold文件夹，该文件夹下生成一个 当天Gold的json文件
    with open('Covid19&' + today + '.json', 'w', encoding='utf-8') as file:
        json.dump(pro_data, file, ensure_ascii=False)
    # CHECK
    print('Writing in the COVID json file succeeded!')     # 标识已经将疫情数据写入json文件


if __name__ == '__main__':
    COVID_Main()
