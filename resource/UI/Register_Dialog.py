'''
Name：订阅显式消息中心注册界面
Writer：山客
date：2021.10.24
Using：注册消息中心用户
Input： user_account, user_password
Output： successfully register, and turn to login interface
'''


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from UI_SignIn import Ui_Dialog

import sys

import pymysql
import time


# 注册对话框
class RegisterDialog(QDialog, Ui_Dialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 设置界面属性与控件
        self.setupUi(self)
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)  # 固定窗口大小

        # 绑定事件
        self.Button_SignIn.clicked.connect(self.Check_Register)
        # self.Button_SignUp.clicked.connect(self.To_SignUp)

        # 连接数据库
        host = 'localhost'  # 本地连接
        port = 3306  # 端口
        database = 'users'  # 数据库名
        user = 'root'  # mysql用户名
        password = 'aa321123'  # mysql密码

        self.database = pymysql.connect(host=host, port=port, db=database, user=user, password=password)
        self.cursor = self.database.cursor()  # 创建游标

    def Check_Register(self):
        user_R_account = self.Text_Account.toPlainText()  # 待注册账号
        user_R_password = self.Text_Password.toPlainText()  # 待注册账号密码
        user_R_ensure = self.Text_Ensure.toPlainText()  # 确认密码
        user_R_name = self.Text_Name.toPlainText()  # 待注册用户名

        # print(user_R_account, user_R_password, user_R_name)

        if not user_R_account or not user_R_password:
            print('请输入正确的账号密码！')
            return

        # 查询是否有同样的账号已经注册
        sql_check = 'select user_id from user where user_account = "{}" and user_name = "{}"'.format(user_R_account, user_R_name)

        self.cursor.execute(sql_check)
        if self.cursor.rowcount:
            self.Label_Tip.setText('账号已存在，请换一个账号！')
            return
        # print('待注册账号不存在！')

        if user_R_password != user_R_ensure:
            self.Label_Tip.setText('请输入同样的密码进行注册！')
            return

        # print('可以正常注册！')

        sql_register = 'insert into user values(@user_id, "{}", "{}", "{}")'.format(user_R_name, user_R_account, user_R_password)

        self.cursor.execute(sql_register)
        self.database.commit()  # mysql 提交操作

        # 注册成功，界面刷新
        self.Label_Tip.setText('注册成功！')
        self.Text_Password.setText('')
        self.Text_Ensure.setText('')

        # time.sleep(1)

        # self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 必须在QWidget前构造QApplication

    register_window = RegisterDialog()
    register_window.show()

    sys.exit(app.exec_())  # 控制界面退出
