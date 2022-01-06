'''
Name：订阅显式消息中心服务端
Writer：山客
date：2021.10.31
Using：消息队列服务端，将服务端爬虫数据发送到 Exchange 上
Input： all message
Output： all message into Exchange by direct
Tips： 指定的queue才能收到消息
'''

# -*- coding:utf-8 -*-
__author__ = "MuT6 Sch01aR"

import pika  # rabbitMQ 消息队列

import json
import datetime
import time


class MQServer:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))  # localhost

        # 根据关键字绑定接收信息
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='MessCenter', exchange_type='direct')

    def SendExchange(self, severity, message):
        self.channel.basic_publish(
            exchange='MessCenter',
            routing_key=severity,
            body=message
        )

        # 添加服务日志
        # print('级别 [%s] 发送数据 [%s]' % (severity, message))


if __name__ == '__main__':
    TestServer = MQServer()  # 实例化消息队列服务端

    today = datetime.date.today().strftime('%Y%m%d')  # 实时日期
    # 导入数据
    File_Gold = open(r'../OUTPUT/Gold/Gold&' + today + '.json', 'rb')
    Data_Gold = json.load(File_Gold)

    File_Oil = open(r'../OUTPUT/Oil/Oil&' + today + '.json', 'rb')
    Data_Oil = json.load(File_Oil)
    '''
    File_Covid = open(r'../OUTPUT/Covid19/Covid&' + today + '.json', 'rb')
    Data_Covid = json.load(File_Covid)

    File_LoverPrattle = open(r'../OUTPUT/LoverPrattle/Love&' + today + '.json', 'rb')
    Data_LoverPrattle = json.load(File_LoverPrattle)

    File_News = open(r'../OUTPUT/News/News&' + today + '.json', 'rb')
    Data_News = json.load(File_News)

    File_Weather = open(r'../OUTPUT/Weather/Weather&' + today + '.json', 'rb')
    Data_Weather = json.load(File_Weather)
    '''

    # 服务端发送数据到 Exchange
    TestServer.SendToExchange('Gold', str(Data_Gold))
    TestServer.SendToExchange('Oil', str(Data_Oil))

    time.sleep(15)
