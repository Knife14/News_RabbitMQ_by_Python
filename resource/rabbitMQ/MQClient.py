'''
Name：订阅显式消息中心客户端
Writer：山客
date：2021.10.31
Using：从Exchange中，通过选择截取（订阅）方式，部分接收数据，并且传输到Main_Window上
Input： some choices
Output： some message matching the choices by direct
Tips： 指定的queue才能收到消息
'''

# -*- coding:utf-8 -*-
__author__ = "MuT6 Sch01aR"

import pika

import json

Message = dict()  # 具体信息内容


class MQClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))  # 创建连接，且不会自动关闭连接

        # 绑定 Exchange
        self.channel = self.connection.channel()  # 创建信道
        self.channel.exchange_declare(exchange='MessCenter', exchange_type='direct')
        # self.channel.basic_qos(prefetch_count=1)  # 设置当前消息未处理完，即不会进行新消费

        # 随机生成消息队列，一个客户端绑定一个消息队列（唯一性）
        self.result = self.channel.queue_declare('', exclusive=True)
        self.queue_name = self.result.method.queue  # 获取队列名

        self.message_json = dict()

        # 其他状态
        self.isRunning = True


# 客户端从消息队列中消费信息
def GetFromExchange(cli: 'MQClient', severity: set):
    for se in severity:
        cli.channel.queue_bind(
            exchange='MessCenter',
            queue=cli.queue_name,
            routing_key=se
        )

    # ch - channel（频道）信息，如连接ip、端口号；
    # method - 消费者标签、发送者标签、exchange、重交付设置、routing_key
    # propertioes - 基础属性
    # body - queue中的具体内容
    def CallBack(ch, method, propertioes, body):
        Message[method.routing_key] = json.loads(
            bytes.decode(body, encoding='utf-8').replace('\'', '\"')
        )  # load - 从文件加载， loads - 从内存加载
    cli.channel.basic_consume(cli.queue_name, CallBack, auto_ack=False)  # 设置手动签收，重回消息队列

    # 开始消费信息
    cli.channel.start_consuming()


if __name__ == '__main__':
    Key = input()  # test, 输入关键字 routing_key
    # print(type(Key), Key)

    # 实例化消息队列客户端
    TestClient = MQClient()

    TestClient.GetFromExchange(Key)

    if TestClient.message_json != None:
        print(TestClient.message_json)
    else:
        print('None')

