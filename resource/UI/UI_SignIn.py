# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_SignIn.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(450, 383)
        self.Button_SignIn = QtWidgets.QPushButton(Dialog)
        self.Button_SignIn.setGeometry(QtCore.QRect(170, 320, 93, 28))
        self.Button_SignIn.setObjectName("Button_SignIn")
        self.Label_Tip = QtWidgets.QLabel(Dialog)
        self.Label_Tip.setGeometry(QtCore.QRect(100, 280, 261, 21))
        self.Label_Tip.setText("")
        self.Label_Tip.setObjectName("Label_Tip")
        self.Lable_Account = QtWidgets.QLabel(Dialog)
        self.Lable_Account.setGeometry(QtCore.QRect(90, 90, 72, 15))
        self.Lable_Account.setObjectName("Lable_Account")
        self.Lable_Password = QtWidgets.QLabel(Dialog)
        self.Lable_Password.setGeometry(QtCore.QRect(90, 140, 41, 16))
        self.Lable_Password.setObjectName("Lable_Password")
        self.Text_Account = QtWidgets.QTextEdit(Dialog)
        self.Text_Account.setGeometry(QtCore.QRect(150, 80, 191, 31))
        self.Text_Account.setObjectName("Text_Account")
        self.Text_Password = QtWidgets.QTextEdit(Dialog)
        self.Text_Password.setGeometry(QtCore.QRect(150, 130, 191, 31))
        self.Text_Password.setObjectName("Text_Password")
        self.Lable_Ensure = QtWidgets.QLabel(Dialog)
        self.Lable_Ensure.setGeometry(QtCore.QRect(50, 190, 91, 20))
        self.Lable_Ensure.setObjectName("Lable_Ensure")
        self.Text_Ensure = QtWidgets.QTextEdit(Dialog)
        self.Text_Ensure.setGeometry(QtCore.QRect(150, 180, 191, 31))
        self.Text_Ensure.setObjectName("Text_Ensure")
        self.Lable_Name = QtWidgets.QLabel(Dialog)
        self.Lable_Name.setGeometry(QtCore.QRect(80, 240, 61, 20))
        self.Lable_Name.setObjectName("Lable_Name")
        self.Text_Name = QtWidgets.QTextEdit(Dialog)
        self.Text_Name.setGeometry(QtCore.QRect(150, 230, 191, 31))
        self.Text_Name.setObjectName("Text_Name")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "??????"))
        self.Button_SignIn.setText(_translate("Dialog", "??????"))
        self.Lable_Account.setText(_translate("Dialog", "?????????"))
        self.Lable_Password.setText(_translate("Dialog", "?????????"))
        self.Lable_Ensure.setText(_translate("Dialog", "??????????????????"))
        self.Lable_Name.setText(_translate("Dialog", "????????????"))
