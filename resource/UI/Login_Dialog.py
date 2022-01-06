'''
Name：订阅显式消息中心登录界面
Writer：山客
date：2021.10.22
Using：登录消息中心
Input： user_account, user_password
Output： successfully login, and turn to the main interface
'''

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from UI_SignUp import Ui_Dialog

import pymysql
# import hashlib  # md5加密
import sys


# 登录对话框
class LoginDialog(QDialog, Ui_Dialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 设置界面属性
        self.setupUi(self)
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)  # 固定窗口大小

        # 绑定事件
        self.Button_SignUp.clicked.connect(self.Check_Login)
        # self.Button_SignIn.clicked.connect(self.To_Register)

        # 连接数据库
        host = 'localhost'  # 本地连接
        port = 3306  # 端口
        database = 'users'  # 数据库名
        user = 'root'  # mysql用户名
        password = 'aa321123'  # mysql密码

        self.database = pymysql.connect(host=host, port=port, db=database, user=user, password=password)
        self.cursor = self.database.cursor()  # 创建游标
        # self.md5 = hashlib.md5() md5加密技术

        # 其他状态
        self.isSignUp = False  # 登录状态
        self.UID = None  # 用户ID
        self.UName = None  # 用户名

    # 登录查询
    def Check_Login(self):
        user_account = self.Text_Account.toPlainText()
        user_password = self.Text_Password.toPlainText()

        if not user_account or not user_password:
            self.Label_Tip.setText('请输入正确的账号密码！')
            return

        # sql查询
        sql = 'select user_id, user_account, user_password, user_name from user where user_account = "{}"'.format(user_account)
        self.cursor.execute(sql)

        # 处理账号
        if not self.cursor.rowcount:
            self.Label_Tip.setText('用户不存在！')
            return

        # 处理密码
        # md5加密技术
        # self.md5.update(user_password.encode('utf-8'))
        # pro_password = self.md5.hexdigest()

        user_message = self.cursor.fetchone()
        if user_message[-2] != user_password:  # [1]会有bug，采用[-1]避免bug
            self.Label_Tip.setText('请输入正确的密码！')
            return

        # 登录检查完成，关闭登录框，返回主界面
        # print('成功登录！')  # test
        self.isSignUp = True  # 登录状态切换
        self.UID = user_message[-4]
        self.UName = user_message[-1]
        self.Text_Account.clear()
        self.Text_Password.clear()

        self.close()  # 登录框关闭


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 必须在QWidget前构造QApplication

    # 实例化窗口类
    login_window = LoginDialog()
    # register_dialog = RegisterDialog()

    login_window.show()

    sys.exit(app.exec_())  # 控制界面退出


