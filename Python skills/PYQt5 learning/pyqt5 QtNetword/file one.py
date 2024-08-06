# 文件名称:E:\python Project\py skill files\PYQt5 learning\pyqt5 QtNetword\file one.py(中文意思为:源代码查询)
# 注释添加日期:2022-08-03 15:58:10.760742
# 编写工具:PyChame
# 编写目的:pyqt5 网络编程
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtNetwork import QUdpSocket, QHostAddress
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout


class Server(QWidget):

    def __init__(self):
        super(Server, self).__init__()

        # 1
        self.sock = QUdpSocket(self)

        # 2
        self.label = QLabel('0', self)
        self.label.setAlignment(Qt.AlignCenter)
        self.btn = QPushButton('Start Server', self)
        self.btn.clicked.connect(self.start_stop_slot)

        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.label)
        self.v_layout.addWidget(self.btn)
        self.setLayout(self.v_layout)

        # 3
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.send_data_slot)

    def start_stop_slot(self):
        if not self.timer.isActive():
            self.btn.setText('Stop Server')
            self.timer.start(1000)
        else:
            self.btn.setText('Start Server')
            self.timer.stop()

    def send_data_slot(self):
        message = QDateTime.currentDateTime().toString()
        self.label.setText(message)
        datagram = message.encode()
        self.sock.writeDatagram(datagram, QHostAddress.LocalHost, 6666)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Server()
    demo.show()
    sys.exit(app.exec_())
'''    1.
    实例化一个QUdpSocket对象；

    2.
    实例化QLabel和QPushButton控件并布局，按钮所连接的槽函数用来控制定时器QTimer的启动与停止。当定时器启动后，服务器每过一秒就会向客户端发送数据；

    3.
    实例化一个QTimer对象，并将timeout信号和槽函数连接起来。在槽函数中，笔者首先获取到当前的系统时间并存储到message变量中，然后将QLabel控件的值设为message显示在窗口中。接着调用encode()
    方法对message进行编码以用于传输。最后调用QUdpSocket对象的writedatagram()
    方法将编码后的字节数据发送到本地主机地址，目标端口为6666；'''