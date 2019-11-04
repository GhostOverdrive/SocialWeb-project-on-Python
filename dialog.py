# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow_dialog(object):
    def setupUi(self, MainWindow_dialog):
        MainWindow_dialog.setObjectName("MainWindow_dialog")
        MainWindow_dialog.resize(440, 496)
        self.centralWidget = QtWidgets.QWidget(MainWindow_dialog)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.dialog_plainTextEdit = QtWidgets.QPlainTextEdit(self.centralWidget)
        self.dialog_plainTextEdit.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.dialog_plainTextEdit.setFont(font)
        self.dialog_plainTextEdit.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.dialog_plainTextEdit.setPlainText("")
        self.dialog_plainTextEdit.setObjectName("dialog_plainTextEdit")
        self.gridLayout.addWidget(self.dialog_plainTextEdit, 1, 0, 1, 2)
        self.label = QtWidgets.QLabel(self.centralWidget)
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.user = QtWidgets.QLabel(self.centralWidget)
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.user.setFont(font)
        self.user.setObjectName("user")
        self.gridLayout.addWidget(self.user, 0, 1, 1, 1)
        self.msg_lineEdit = QtWidgets.QLineEdit(self.centralWidget)
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.msg_lineEdit.setFont(font)
        self.msg_lineEdit.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.msg_lineEdit.setObjectName("msg_lineEdit")
        self.gridLayout.addWidget(self.msg_lineEdit, 2, 0, 1, 1)
        self.send_btn = QtWidgets.QPushButton(self.centralWidget)
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.send_btn.setFont(font)
        self.send_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.send_btn.setObjectName("send_btn")
        self.gridLayout.addWidget(self.send_btn, 2, 1, 1, 1)
        MainWindow_dialog.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow_dialog)
        QtCore.QMetaObject.connectSlotsByName(MainWindow_dialog)

    def retranslateUi(self, MainWindow_dialog):
        _translate = QtCore.QCoreApplication.translate
        MainWindow_dialog.setWindowTitle(_translate("MainWindow_dialog", "MainWindow"))
        self.label.setText(_translate("MainWindow_dialog", "Диалог с:"))
        self.user.setText(_translate("MainWindow_dialog", "user"))
        self.send_btn.setText(_translate("MainWindow_dialog", "Отправить"))
