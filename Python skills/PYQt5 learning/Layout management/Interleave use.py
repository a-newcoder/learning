# 文件名称:E:\python Project\py skill files\PYQt5 learning\Layout management\Interleave use.py(中文意思为:源代码查询)
# 注释添加日期:2022-08-03 15:55:57.709960
# 编写工具:PyChame
# 编写目的:混合使用QHBoxLayout与QVBoxLayout
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, \
    QHBoxLayout, QVBoxLayout


class Demo(QWidget):

    def __init__(self):
        super(Demo, self).__init__()

        self.user_label = QLabel('Username:', self)
        self.pwd_label = QLabel('Password:', self)
        self.user_line = QLineEdit(self)
        self.pwd_line = QLineEdit(self)
        self.login_button = QPushButton('Log in', self)
        self.signin_button = QPushButton('Sign in', self)

        self.user_h_layout = QHBoxLayout()
        self.pwd_h_layout = QHBoxLayout()
        self.button_h_layout = QHBoxLayout()
        self.all_v_layout = QVBoxLayout()

        self.user_h_layout.addWidget(self.user_label)
        self.user_h_layout.addWidget(self.user_line)
        self.pwd_h_layout.addWidget(self.pwd_label)
        self.pwd_h_layout.addWidget(self.pwd_line)
        self.button_h_layout.addWidget(self.login_button)
        self.button_h_layout.addWidget(self.signin_button)
        self.all_v_layout.addLayout(self.user_h_layout)
        self.all_v_layout.addLayout(self.pwd_h_layout)
        self.all_v_layout.addLayout(self.button_h_layout)

        self.setLayout(self.all_v_layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())