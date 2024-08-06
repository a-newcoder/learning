import sys
from PyQt5.QtNetwork import QUdpSocket, QHostAddress
from PyQt5.QtWidgets import QApplication, QWidget, QTextBrowser, QVBoxLayout


class Client(QWidget):

    def __init__(self):
        super(Client, self).__init__()

        # 1
        self.sock = QUdpSocket(self)
        self.sock.bind(QHostAddress.LocalHost, 6666)
        self.sock.readyRead.connect(self.read_data_slot)

        # 2
        self.browser = QTextBrowser(self)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.browser)
        self.setLayout(self.layout)

    def read_data_slot(self):
        while self.sock.hasPendingDatagrams():
            datagram, host, port = self.sock.readDatagram(
                self.sock.pendingDatagramSize()
            )

            messgae = 'Date time: {}\nHost: {}\nPort: {}\n\n'.format(datagram.decode(), host.toString(), port)
            self.browser.append(messgae)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Client()
    demo.show()
    sys.exit(app.exec_())
'''1. 实例化QUdpSocket对象并调用bind()方法绑定地址和端口。每次可以准备读取新数据时，readyRead信号就会发射，
我们在该信号所连接的槽函数中进行读取操作。首先调用hasPendingDatagrams()来判断是否还有要读取的数据，如果有的话就调用readDatagram()来读取数据，传入该方法的参数为要读取的数据大小
，我们可以用pendingDatagramSize()方法获取。

readDatagram()一共返回三个值，分别是数据(字节)，主机地址(QHostAddress对象)以及端口号(整型值)。之后我们用decode()将数据解码，用QHostAddress对象的toString()方法来获取到地址字符串。
最后调用append()方法将message值显示在QTextBrowser控件上；

2. 实例化一个QTextBrowser文本浏览框对象并进行布局。'''