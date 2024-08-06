import json
from socket import gethostname,gethostbyname
from sys import argv
from os import system
import matplotlib.pyplot as py
import numpy as nu
import pandas
from PyQt5.QtGui import QPixmap
from PyQt5.QtNetwork import QUdpSocket, QHostAddress
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QHBoxLayout, QVBoxLayout, \
    QProgressBar, QFileDialog, QMessageBox, QInputDialog, QTextBrowser, QTextEdit, QComboBox, QLabel


class Server(QWidget):
    try:
        with open("people.json", "r+", encoding="utf-8") as file:#这里曾经出现问题：把打开模式设置为了a+，导致文件从最后面读取，以至于无法读取到任何数据
            lis=json.load(file)
    except json.decoder.JSONDecodeError or IOError:
        with open("people.json","w",encoding="utf-8") as file:
            lis={}
            json.dump({},file)

    def __init__(self):
        super(Server, self).__init__()

        self.setGeometry(550, 340, 400, 400)

        self.lab = QLabel(self)
        self.lab.setPixmap(QPixmap("onefile.jpg"))
        self.lab.setScaledContents(True)
        self.lab.lower()

        self.sock = QUdpSocket(self)
        self.sock.bind(QHostAddress.Any, 6666)
        self.sock.readyRead.connect(self.read_data_slot)

        self.Chat_record=QPushButton()
        self.Chat_record.setText("打开聊天记录")
        self.Chat_record.clicked.connect(self.open_Chat_record)

        self.browser = QTextBrowser(self)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.browser)
        self.layout.addWidget(self.Chat_record)
        self.setLayout(self.layout)

    def open_Chat_record(self):
        system("\"E:\\python Project\\contest\\Chat_record.txt\"")

    def read_data_slot(self):
        while self.sock.hasPendingDatagrams():
            datagram, host, port = self.sock.readDatagram(self.sock.pendingDatagramSize())

            if self.is_not(host.toString()):
                messgae = 'message: {}\nHost: {}\n'.format(datagram.decode(), self.lis[host.toString()],
                                                           port)
                with open("Chat_record.txt","a",encoding="utf-8") as file:
                    file.write("{}:{}\n".format(self.lis[host.toString()],datagram.decode()))
                self.browser.append(messgae)

    def is_not(self, host):
        if host in self.lis:
            return True
        else:
            confirm = QMessageBox.question(self, "安全验证", "有一个陌生信息,是否通过？",
                                           QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                name = QInputDialog.getText(self, "询问", "请输入他的名或者填写‘陌生’")
                with open("people.json", "r", encoding="utf-8") as file:
                    self.lis = json.load(file)
                self.lis[host] = name[0]
                with open("people.json", "w", encoding="utf-8") as file:
                    json.dump(self.lis, file)
                return True
            if confirm == QMessageBox.No:
                return False

    def resizeEvent(self, *args, **kwargs) -> None:
        x = self.width()
        y = self.height()
        self.lab.resize(x, y)



class Client(QWidget):
    def __init__(self):
        super(Client, self).__init__()
        try:

             with open("contacts.json", "r+", encoding="utf-8") as file:   #这里曾经出现问题：把打开模式设置为了a+，导致文件从最后面读取，以至于无法读取到任何数据
                    self.lis=json.load(file)


        except json.decoder.JSONDecodeError or IOError :
            with open("contacts.json","w",encoding="utf-8") as file:
                self.lis={}
                json.dump({},file)

        self.setGeometry(970, 340, 400, 400)

        self.sock = QUdpSocket(self)

        self.lab = QLabel(self)
        self.lab.setPixmap(QPixmap("onefile.jpg"))
        self.lab.setScaledContents(True)
        self.lab.lower()

        self.my_IP=QLabel()
        self.my_IP.setStyleSheet("color:blue")
        self.my_IP.setStyleSheet("background-color:grey")
        self.my_IP.setText("你的IP地址"+gethostbyname(gethostname()))

        self.choce = QComboBox()

        self.name = QTextEdit()


        self.IP = QTextEdit()

        self.add = QPushButton("添加")
        self.del_ = QPushButton("删除")
        self.name.setPlaceholderText("请输入联系人名字")
        self.IP.setPlaceholderText("请输入联系人ID地址")
        self.add.released.connect(self.add_people)
        self.del_.released.connect(self.del_people)
        self.choce.addItems(self.lis)

        self.btn = QPushButton('Start Server', self)
        self.btn.clicked.connect(self.send_data_slot)
        self.mes = QTextEdit()
        self.mes.setPlaceholderText("输入你要发送的消息")

        self.bottom = QHBoxLayout()
        self.v_layout = QVBoxLayout()
        self.left = QVBoxLayout()
        self.h_layout = QHBoxLayout()

        self.bottom.addWidget(self.add)
        self.bottom.addWidget(self.del_)
        self.v_layout.addWidget(self.my_IP)
        self.v_layout.addWidget(self.mes)
        self.v_layout.addWidget(self.btn)
        self.left.addWidget(self.choce)
        self.left.addWidget(self.name)
        self.left.addWidget(self.IP)
        self.left.addLayout(self.bottom)
        self.h_layout.addLayout(self.left)
        self.h_layout.addLayout(self.v_layout)

        self.setLayout(self.h_layout)

    def send_data_slot(self):
        message = self.mes.toPlainText()

        datagram = message.encode()
        print(self.lis[self.choce.currentText()])
        self.sock.writeDatagram(datagram, QHostAddress(self.lis[self.choce.currentText()]), 6666)

    def add_people(self):
        self.lis[self.name.toPlainText()] = self.IP.toPlainText()
        self.choce.clear()
        self.choce.addItems(self.lis)

        with open("contacts.json", "w", encoding="utf-8") as file:
            print(self.lis)
            json.dump(self.lis, file)

        self.IP.clear()
        self.name.clear()

    def del_people(self):
        del self.lis[self.name.toPlainText()]
        self.choce.clear()
        self.choce.addItems(self.lis)

        with open("contacts.json", "w", encoding="utf-8") as file:
            json.dump(self.lis, file)
        self.IP.clear()

    def resizeEvent(self, *args, **kwargs) -> None:
        x = self.width()
        y = self.height()
        self.lab.resize(x, y)


class Main(QWidget):
    def __init__(self):
        super(Main, self).__init__()
        self.setGeometry(540, 330, 1000, 500)
        self.resize(1000, 500)

        self.lab = QLabel(self)
        self.lab.setPixmap(QPixmap("onefile.jpg"))
        self.lab.setScaledContents(True)
        self.lab.lower()

        self.filename = QLabel()
        self.filename.setText("                                                                             hallo world")
        self.sizeHint().setWidth(100)
        self.filename.setMaximumHeight(25)

        self.product = QPushButton()
        self.product.setText("生成成绩图像")
        self.product.clicked.connect(self.produc)
        self.product.released.connect(self.change_bottom_test)

        self.check = QPushButton()
        self.check.setText("查询成绩")
        self.check.clicked.connect(self.chec)

        self.net = QPushButton()
        self.net.setText("打开通讯")
        self.net.clicked.connect(self.open_net)

        self.progress = QProgressBar()
        self.progress.setValue(0)

        self.step = 0
        self.confirm = [False]
        self.file_way = [""]

        self.bottom = QHBoxLayout()
        self.bottom.addWidget(self.product)
        self.bottom.addWidget(self.check)
        self.bottom.addWidget(self.net)
        # self.progress.setStyleSheet("QProgressBar::chunk "
        # "{"
        # "background-color: turquoise;"
        # "}")
        self.all_ = QVBoxLayout()
        self.all_.addWidget(self.filename)
        self.all_.addWidget(self.progress)
        self.all_.addLayout(self.bottom)

        self.setLayout(self.all_)

    def change_progress(self, step, number):
        cha = step / number * 100
        self.progress.setValue(int(cha))
        if self.step == number:
            self.product.setText("生成成绩图像")
            self.step = 0

    def change_bottom_test(self):
        if self.product.text() == "生成成绩图像":
            self.product.setText("正在生成成绩图像")

    def produc(self):
        if not self.confirm[0]:  # 如果文件未打开
            self.file_way[0] = self.open_file()  # string
            if self.file_way[0]:  # 如果文件已打开
                pass
            elif not self.file_way[0]:
                return

        Excel = pandas.read_excel(self.file_way[0])
        subject, score, number = nu.array(Excel.columns.values), nu.array(Excel.values), Excel.shape[0]
        py.figure(num='score', figsize=(5, 6))
        dig = QFileDialog()
        # 设置可以打开任何文件
        dig.setFileMode(QFileDialog.Directory)
        dig.exec_()
        way = dig.selectedFiles()
        for j in range(number):
            py.clf()
            py.ylim(0, 100)
            py.xlim(0, 9)
            py.ylabel('Score')
            py.xlabel('subject')
            py.bar(subject, score[j], color='red', width=1.5, align='edge')
            py.savefig(way[0] + '/' + str(j + 1) + '.jpg')
            self.step += 1
            self.change_progress(self.step, number)

    def chec(self):
        if not self.confirm[0]:  # 如果文件未打开

            self.file_way[0] = self.open_file()  # string
            if self.file_way[0]:  # 如果文件已打开
                pass
            elif not self.file_way[0]:
                return
        Excel = pandas.read_excel(self.file_way[0])
        subject = nu.array(Excel.columns.values)
        score = nu.array(Excel.values)
        number = QInputDialog.getInt(self, '学号', '请输入你的学号', min=0, max=57)
        py.figure(num='score', figsize=(5, 6))
        py.ylim(0, 100)
        py.xlim(0, 9)
        py.ylabel('Score')
        py.xlabel('subject')
        py.bar(subject, score[number[0]], color='red', width=0.7, align='edge')
        py.show()

    def open_file(self):
        get = QFileDialog.getOpenFileName()
        if get[0]:
            self.filename.setText("                                                              "+get[0])
            self.confirm[0] = True
            return get[0]
        else:
            QMessageBox.warning(self, 'warning', '请选择正确的文件')
            return False

    def open_net(self):
        self.cli = Client()
        self.sev = Server()
        self.cli.show()
        self.sev.show()

    def resizeEvent(self, *args, **kwargs) -> None:
        x = self.width()
        y = self.height()
        self.lab.resize(x, y)


if __name__ == "__main__":

    app = QApplication(argv)
    window = Main()
    window.show()
    app.exec_()
