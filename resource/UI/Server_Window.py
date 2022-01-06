'''
Name：订阅显式消息中心服务日志界面
Writer：山客
date：2021.11.6
Using：消息队列服务日志
Input：
Output： 更新日志、发送日志
'''


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from UI_Server import Ui_mainWindow

import sys
import time
import datetime
import threading
import json
import os

from resource.rabbitMQ.MQServer import *
from resource.Reptile import COVID_19, Gold_Price, Oil_Price, Lover_Prattle, News, Weather


class ServerWindow(QMainWindow, Ui_mainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 设置界面属性与控件
        self.setupUi(self)
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)  # 固定窗口大小

        # 实例化消息队列服务端
        self.MQServer = MQServer()
        self.MQMessage = dict()
        self.cnt = 0

    def SendToExchange(self):
        # 每次打开该服务端的时候，都会启动爬虫程序
        if self.cnt <= 0:
            self.RepliteData()

            for key, value in self.MQMessage.items():
                self.MQServer.SendExchange(key, str(value))
                self.Text_Log.insertPlainText(str(datetime.datetime.now()) + ': Send the latest ' + key + ' data succeeded!' + '\n')

            self.cnt = 1
        else:
            # 程序运行期间，每到每天9点钟，也会运行一次爬虫程序，用以更新
            if datetime.datetime.now().hour == 9:
                self.RepliteData()

                for key, value in self.MQMessage.items():
                    self.MQServer.SendToExchange(key, str(value))

                self.cnt += 1

    def RepliteData(self):
        # 日期
        today = datetime.date.today().strftime('%Y%m%d')  # 实时保存

        # 疫情数据
        if not os.path.isfile('../OUTPUT/Covid19/Covid19&' + today + '.json'):
            COVID_19.COVID_Main()
        with open('../OUTPUT/Covid19/Covid19&' + today + '.json', 'r', encoding='utf-8') as CovidFile:
            self.MQMessage['COVID'] = json.load(CovidFile)
        self.Text_Log.insertPlainText(str(datetime.datetime.now()) + ': Download the latest COVID data succeeded!' + '\n')

        # 黄金数据
        if not os.path.isfile('../OUTPUT/Gold/Gold&' + today + '.json'):
            Gold_Price.Gold_Main()
        with open('../OUTPUT/Gold/Gold&' + today + '.json', 'r', encoding='utf-8') as GoldFile:
            self.MQMessage['Gold'] = json.load(GoldFile)
        self.Text_Log.insertPlainText(str(datetime.datetime.now()) + ': Download the latest Gold data succeeded!' + '\n')

        # 情话数据
        if not os.path.isfile('../OUTPUT/News/News&' + today + '.json'):
            Lover_Prattle.LoverPrattle_Main()
        with open('../OUTPUT/LoverPrattle/Love&' + today + '.json', 'r', encoding='utf-8') as LoveFile:
            self.MQMessage['Prattle'] = json.load(LoveFile)
        self.Text_Log.insertPlainText(str(datetime.datetime.now()) + ': Download the latest Lover Prattle data succeeded!' + '\n')

        # 新闻数据
        if not os.path.isfile('../OUTPUT/News/News&' + today + '.json'):
            News.News_Main()
        with open('../OUTPUT/News/News&' + today + '.json', 'r', encoding='utf-8') as NewsFile:
            self.MQMessage['News'] = json.load(NewsFile)
        self.Text_Log.insertPlainText(str(datetime.datetime.now()) + ': Download the latest News data succeeded!' + '\n')

        # 石油数据
        if not os.path.isfile('../OUTPUT/Oil/Oil&' + today + '.json'):
            Oil_Price.Oil_Main()
        with open('../OUTPUT/Oil/Oil&' + today + '.json', 'r', encoding='utf-8') as OilFile:
            self.MQMessage['Oil'] = json.load(OilFile)
        self.Text_Log.insertPlainText(str(datetime.datetime.now()) + ': Download the latest Oil Price data succeeded!' + '\n')

        # 天气数据
        if not os.path.isfile('../OUTPUT/Weather/Weather&' + today + '.json'):
            Weather.Weather_Main()
        with open('../OUTPUT/Weather/Weather&' + today + '.json', 'r', encoding='utf-8') as WeatherFile:
            self.MQMessage['Weather'] = json.load(WeatherFile)
        self.Text_Log.insertPlainText(str(datetime.datetime.now()) + ': Download the latest Weather data succeeded!' + '\n')


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 必须在QWidget前构造QApplication

    TestWindow = ServerWindow()
    TestWindow.show()

    # TestWindow.SendToExchange()
    Thread_Window = threading.Thread(target=TestWindow.SendToExchange)
    Thread_Window.start()

    sys.exit(app.exec_())  # 控制界面退出
