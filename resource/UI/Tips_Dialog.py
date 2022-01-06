'''
Name：订阅显式消息中心提示对话框
Writer：山客
date：2021.11.26
Using：登录消息中心
Input：
Output：
'''


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from UI_Tips import Ui_Tips


class TipsDialog(QDialog, Ui_Tips):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 设置界面属性
        self.setupUi(self)
