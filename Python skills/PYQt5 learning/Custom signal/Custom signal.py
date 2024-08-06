# 文件名称:E:\python Project\py skill files\PYQt5 learning\Custom signal\Custom signal.py(中文意思为:源代码查询)
# 注释添加日期:2022-08-03 15:55:12.040039
# 编写工具:PyChame
# 编写目的:自定义按钮
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtCore import pyqtSignal                             # 1
from PyQt5.QtWidgets import QApplication, QWidget, QLabel


class Demo(QWidget):
    my_signal = pyqtSignal()                                    # 2

    def __init__(self):
        super(Demo, self).__init__()
        self.label = QLabel('Hello World', self)
        self.my_signal.connect(self.change_text)                # 3

    def change_text(self):
        if self.label.text() == 'Hello World':
            self.label.setText('Hello PyQt5')
        else:
            self.label.setText('Hello World')

    def mousePressEvent(self, QMouseEvent):                     # 4
        self.my_signal.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())
'''1. 需要先导入pyqtSignal；

2. 实例化一个自定义的信号；

3. 将自定义的信号连接到自定义的槽函数上；

4. mousePressEvent()方法是许多控件自带的，这里来自于QWidget。该方法用来监测鼠标是否有按下。现在鼠标若被按下，则会发出自定义的信号.'''