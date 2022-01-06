'''
Name：订阅显式消息中心主界面
Writer：山客
date：2021.11.20
Using：消息中心主界面，数据可视化
Input：user_account, user_password, reptile_data_json
Output：some pictures, some tables, some text
'''

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from UI_Main import Ui_MainWindow

import sys
import threading
import time
import random
import inspect
import ctypes

from Login_Dialog import *
from Register_Dialog import *
from Tips_Dialog import *
from resource.rabbitMQ.MQClient import *


# 关闭线程
def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""

    """引发异常，如果需要执行清理"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        """if it returns a number greater than one, you're in trouble,
        and you should call it again with exc=NULL to revert the effect"""

        """如果它返回一个大于1的数字，您就有麻烦了，
        您应该使用exc=NULL再次调用它来恢复效果"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


# 登录主界面
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 设置界面属性与控件
        self.setupUi(self)
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)  # 固定窗口大小

        # 绑定复选框状态改变事件
        self.MessList = set()  # routing_key
        self.Box_Gold.stateChanged.connect(self.BoxChanged)
        self.Box_COVID.stateChanged.connect(self.BoxChanged)
        self.Box_Weather.stateChanged.connect(self.BoxChanged)
        self.Box_News.stateChanged.connect(self.BoxChanged)
        self.Box_Oil.stateChanged.connect(self.BoxChanged)
        self.Box_Prattle.stateChanged.connect(self.BoxChanged)

        # 绑定按钮事件
        self.Button_SignUp.clicked.connect(self.To_SignUp)
        self.Button_SignIn.clicked.connect(self.To_SignIn)
        self.Button_Update.clicked.connect(self.GetAndProMessage)
        self.Button_SignOut.clicked.connect(self.Make_SignOut)

        # 实例化对话框类
        self.login_dialog = LoginDialog()
        self.register_dialog = RegisterDialog()
        self.tip_dialog = TipsDialog()

        # 实例化消息队列
        self.MQClient = MQClient()
        # self.Message = None

        # 其他状态在初始化时候进行修改
        self.Label_UID.hide()
        self.Button_SignOut.hide()
        self.isChangedUI = False

        # 在主线程下创建子线程
        self.Thread_GetMessList = []  # threading.Thread(target=GetFromExchange, args=(self.MQClient, self.MessList))
        self.Thread_ProMess = Data_Thread()

    # 跳转登录对话框
    def To_SignUp(self):
        if self.login_dialog.isSignUp == False:
            self.login_dialog.show()

    # 跳转注册对话框
    def To_SignIn(self):
        if self.login_dialog.isSignUp == False:
            self.register_dialog.show()

        self.register_dialog.Text_Account.clear()
        self.register_dialog.Text_Name.clear()
        self.register_dialog.Label_Tip.clear()

    # 退出登录
    def Make_SignOut(self):
        self.login_dialog.isSignUp = False  # 修改登录状态
        self.isChangedUI = False

        # 清空可视化内容，复选框选中
        self.Text_Data.clear()

        self.Box_Gold.setChecked(False)
        self.Box_News.setChecked(False)
        self.Box_Oil.setChecked(False)
        self.Box_Weather.setChecked(False)
        self.Box_Prattle.setChecked(False)
        self.Box_COVID.setChecked(False)

        # 显示登录注册按钮
        self.Button_SignUp.show()
        self.Button_SignIn.show()

        # 隐藏用户名与退出按钮
        self.Label_UID.hide()
        self.Button_SignOut.hide()

    # 监测复选框状态
    def BoxChanged(self):

        if self.Box_Gold.isChecked():
            self.Box_Gold.setCheckState(Qt.Checked)
            if 'Gold' not in self.MessList:
                self.MessList.add('Gold')
        elif not self.Box_Gold.isChecked():
            self.Box_Gold.setCheckState(Qt.Unchecked)
            if 'Gold' in self.MessList:
                self.MessList.remove('Gold')

        if self.Box_Oil.isChecked():
            self.Box_Oil.setCheckState(Qt.Checked)
            if 'Oil' not in self.MessList:
                self.MessList.add('Oil')
        elif not self.Box_Oil.isChecked():
            self.Box_Oil.setCheckState(Qt.Unchecked)
            if 'Oil' in self.MessList:
                self.MessList.remove('Oil')

        if self.Box_News.isChecked():
            self.Box_News.setCheckState(Qt.Checked)
            if 'News' not in self.MessList:
                self.MessList.add('News')
        elif not self.Box_News.isChecked():
            self.Box_News.setCheckState(Qt.Unchecked)
            if 'News' in self.MessList:
                self.MessList.remove('News')

        if self.Box_Weather.isChecked():
            self.Box_Weather.setCheckState(Qt.Checked)
            if 'Weather' not in self.MessList:
                self.MessList.add('Weather')
        elif not self.Box_Weather.isChecked():
            self.Box_Weather.setCheckState(Qt.Unchecked)
            if 'Weather' in self.MessList:
                self.MessList.remove('Weather')

        if self.Box_Prattle.isChecked():
            self.Box_Prattle.setCheckState(Qt.Checked)
            if 'Prattle' not in self.MessList:
                self.MessList.add('Prattle')
        elif not self.Box_Prattle.isChecked():
            self.Box_Prattle.setCheckState(Qt.Unchecked)
            if 'Prattle' in self.MessList:
                self.MessList.remove('Prattle')

        if self.Box_COVID.isChecked():
            self.Box_COVID.setCheckState(Qt.Checked)
            if 'COVID' not in self.MessList:
                self.MessList.add('COVID')
        elif not self.Box_COVID.isChecked():
            self.Box_COVID.setCheckState(Qt.Unchecked)
            if 'COVID' in self.MessList:
                self.MessList.remove('COVID')

    # 消费信息
    def GetAndProMessage(self):
        # 全局变量 Message
        global Message
        Message.clear()

        if self.login_dialog.isSignUp:
            # 实例化消息队列
            self.MQClient = MQClient()

            # 消息队列消费信息，避免消费冲突
            self.Thread_GetMessList.append(threading.Thread(target=GetFromExchange, args=(self.MQClient, self.MessList)))
            self.Thread_GetMessList.pop().start()

            # # 数据可视化，避免渲染冲突
            # self.Thread_ProMess.start()
            # self.Thread_ProMess.trigger.connect(self.Data_Description)
            # self.Thread_ProMess.wait()
        # 显示登录提示框，提示用户登录
        else:
            # 清空复选框选中
            self.Box_Gold.setChecked(False)
            self.Box_News.setChecked(False)
            self.Box_Oil.setChecked(False)
            self.Box_Weather.setChecked(False)
            self.Box_Prattle.setChecked(False)
            self.Box_COVID.setChecked(False)

            self.tip_dialog.show()

    def Data_Description(self):
        global Message

        if len(Message) > 0:
            for Key, Value in Message.items():
                # 黄金
                if Key == 'Gold' and Key in self.MessList:
                    self.Text_Data.append('<font size=\"5\" color=\"Brown\">黄金实时价格：</font>')
                    for G_name, G_pros in Value.items():
                        self.Text_Data.append('<font size=\"4\">' + G_name + '（单位：元/克）</font>')
                        self.Text_Data.insertPlainText('\n   最新价格： ' + G_pros['最新价格'])
                        self.Text_Data.insertPlainText('\n   开盘价格： ' + G_pros['开盘价格'])
                        self.Text_Data.insertPlainText('\n   最高价格： ' + G_pros['最高价格'])
                        self.Text_Data.insertPlainText('\n   最低价格： ' + G_pros['最低价格'])
                        self.Text_Data.insertPlainText('\n   涨跌幅度： ' + G_pros['涨跌幅度'])
                        self.Text_Data.insertPlainText('\n   昨日收盘价： ' + G_pros['昨日收盘价'])
                        self.Text_Data.insertPlainText('\n   总成交量： ' + G_pros['总成交量'])
                        self.Text_Data.insertPlainText('\n   更新时间： ' + G_pros['更新时间'])
                # 实时新闻
                elif Key == 'News' and Key in self.MessList:
                    self.Text_Data.append('<font size=\"5\" color=\"Brown\">今日头条：</font>')
                    for val in Value:
                        self.Text_Data.insertPlainText('\n  ' + str(list(val.values())[0]) + '、 ' + list(val.values())[1])
                # 土味情话
                elif Key == 'Prattle' and Key in self.MessList:
                    self.Text_Data.append('<font size=\"5\" color=\"Brown\">今日情话：</font>')
                    index = random.randint(0, 100)
                    self.Text_Data.insertPlainText('\n ' + Value[index])
                # 疫情数据
                elif Key == 'COVID' and Key in self.MessList:
                    self.Text_Data.append('<font size=\"5\" color=\"Brown\">疫情最新情况：</font>')
                    COVID_Area = self.Text_COVID19.toPlainText()
                    if len(COVID_Area) < 1:
                        COVID_Area = '重庆市'
                    self.Text_Data.append('<font size=\"4\">' + COVID_Area + '</font>')
                    self.Text_Data.insertPlainText('\n    地点编号：' + str(Value[COVID_Area]['地点编号']))
                    self.Text_Data.insertPlainText('\n    目前确诊数：' + str(Value[COVID_Area]['目前确诊数']))
                    self.Text_Data.insertPlainText('\n    总确诊数：' + str(Value[COVID_Area]['总确诊数']))
                    self.Text_Data.insertPlainText('\n    疑似病例数：' + str(Value[COVID_Area]['疑似病例数']))
                    self.Text_Data.insertPlainText('\n    治愈病例数：' + str(Value[COVID_Area]['治愈病例数']))
                    self.Text_Data.insertPlainText('\n    死亡病例数：' + str(Value[COVID_Area]['死亡病例数']))
                # 天气
                elif Key == 'Weather' and Key in self.MessList:
                    self.Text_Data.append('<font size=\"5\" color=\"Brown\">今日天气：</font>')
                    Weather_Area = self.Text_Weather.toPlainText()
                    if len(Weather_Area) < 1:
                        Weather_Area = '沙坪坝'
                    for val in Value:
                        if list(val.keys())[0] == Weather_Area:
                            self.Text_Data.append('<font size=\"4\">' + Weather_Area + '</font>')
                            self.Text_Data.insertPlainText('\n  城市编号：' + val[Weather_Area]['城市编号'])
                            self.Text_Data.insertPlainText('\n  天气现象：' + val[Weather_Area]['天气现象'])
                            self.Text_Data.insertPlainText('\n  最高温度：' + val[Weather_Area]['最高温度'] + ' ℃')
                            self.Text_Data.insertPlainText('\n  最低温度：' + val[Weather_Area]['最低温度'] + ' ℃')
                # 油价
                elif Key == 'Oil' and Key in self.MessList:
                    self.Text_Data.append('<font size=\"5\" color=\"Brown\">最新油价（元/升）：</font>')
                    self.Text_Data.insertPlainText('\n  0号汽油：' + Value[0])
                    self.Text_Data.insertPlainText('\n  89号汽油：' + Value[1])
                    self.Text_Data.insertPlainText('\n  92号汽油：' + Value[2])
                    self.Text_Data.insertPlainText('\n  95号汽油：' + Value[3])
                    self.Text_Data.insertPlainText('\n  98号汽油：' + Value[4])

        Message.clear()


# 数据可视化
# QThread，无法使用threading，会导致渲染失败从而程序崩溃
class Data_Thread(QThread):
    trigger = pyqtSignal(dict)  # 定义类属性，不能放进init方法中

    def __init__(self):
        super(Data_Thread, self).__init__()

    # 重写run()
    def run(self):
        self.trigger.emit(Message)


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 必须在QWidget前构造QApplication

    # 实例化对象类
    main_window = MainWindow()
    main_window.show()

    # 实时监测登录状态
    def ChangeSign():
        while True:
            if main_window.login_dialog.isSignUp:
                if not main_window.isChangedUI:
                    # 隐藏登录注册按钮
                    main_window.Button_SignUp.hide()
                    main_window.Button_SignIn.hide()

                    # 显示用户名与退出按钮
                    main_window.Label_UID.setText(str(main_window.login_dialog.UID) + ' ' + main_window.login_dialog.UName + '，欢迎你！')
                    main_window.Label_UID.show()
                    main_window.Button_SignOut.show()

                    main_window.isChangedUI = True

                # 数据可视化，避免渲染冲突
                main_window.Thread_ProMess.start()
                main_window.Thread_ProMess.trigger.connect(main_window.Data_Description)
                main_window.Thread_ProMess.wait()
    CheckLogin = threading.Thread(target=ChangeSign)
    CheckLogin.start()

    # 控制界面退出，并销毁所有线程
    app.exec_()

    for t in main_window.Thread_GetMessList:
        stop_thread(t)

    sys.exit()

