import json
from socket import gethostname, gethostbyname
from PyQt5.QtNetwork import *
from PyQt5.QtMultimedia import *
from PyQt5.QtWidgets import *

'''from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QVBoxLayout, \
    QTextBrowser, QTextEdit, QComboBox, QLabel, QTabWidget, QHBoxLayout, QMessageBox, \
    QInputDialog
'''


# -*- coding: utf-8 -*-

class main(QTabWidget):

    def __init__(self):
        super(main, self).__init__()
        try:
            with open("contacts.json", "r+", encoding="utf-8") as file:  # 这里曾经出现问题：把打开模式设置为了a+，导致文件从最后面读取，以至于无法读取到任何数据
                self.contacts = json.load(file)
        except json.decoder.JSONDecodeError or IOError:
            with open("contacts.json", "w", encoding="utf-8") as file:
                self.contacts = {}
                json.dump({}, file)
        try:
            with open("people.json", "r+", encoding="utf-8") as file:  # 这里曾经出现问题：把打开模式设置为了a+，导致文件从最后面读取，以至于无法读取到任何数据
                self.people = json.load(file)
        except json.decoder.JSONDecodeError or IOError:
            with open("people.json", "w", encoding="utf-8") as file:
                self.people = {}
                json.dump({}, file)

        self.setGeometry(550, 340, 400, 400)
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        self.tab1_init()
        self.tab2_init()
        self.tab3_init()

        self.addTab(self.tab1, '通讯')
        self.addTab(self.tab2, '通讯录')
        self.addTab(self.tab3, '使用说明')

    def tab1_init(self):
        self.sock = QUdpSocket(self)
        self.sock.bind(QHostAddress.Any, 6666)
        self.sock.readyRead.connect(self.read_data_slot)

        self.sock1 = QUdpSocket(self)

        self.choce = QComboBox()
        self.choce.addItems(self.contacts)

        self.btn = QPushButton('发送', self)
        self.btn.clicked.connect(self.send_data_slot)

        self.mes = QTextEdit()
        self.mes.setPlaceholderText("输入你要发送的消息")

        self.browser = QTextBrowser(self)

        layouts = QVBoxLayout()
        layouts.addWidget(self.choce)
        layouts.addWidget(self.browser)
        layouts.addWidget(self.mes)
        layouts.addWidget(self.btn)

        self.tab1.setLayout(layouts)

    def tab2_init(self):

        self.my_IP = QLabel()
        self.my_IP.setStyleSheet("color:blue")
        self.my_IP.setStyleSheet("background-color:grey")
        self.my_IP.setText("你的IP地址" + gethostbyname(gethostname()))

        self.name = QTextEdit()

        self.IP = QTextEdit()

        self.add = QPushButton("添加")
        self.del_ = QPushButton("删除")
        self.name.setPlaceholderText("请输入联系人名字")
        self.IP.setPlaceholderText("请输入联系人ID地址")
        self.add.released.connect(self.add_people)
        self.del_.released.connect(self.del_people)

        layouts = QVBoxLayout()
        a = QHBoxLayout()

        layouts.addWidget(self.my_IP)
        layouts.addWidget(self.name)
        layouts.addWidget(self.IP)

        a.addWidget(self.add)
        a.addWidget(self.del_)

        layouts.addLayout(a)

        self.tab2.setLayout(layouts)

    def tab3_init(self):
        self.help = QTextEdit()
        self.help.setText('''                       使用说明\n
输入联系人名-->添加ID地址-->切换到
1.收发信息需要双方都打开此应用，不然用不了\n
2.在发送消息之前先添加对方好友，不然会闪退\n
3.发的第一个消息必须是验证消息即表明自己身份的消息\n
4.会同时接收到不同人的信息，统一在通讯界面接收\n
5.ID地址相当于账号\n
6.在通讯前记得切换到想发的人的名字，每次开启本软件，联系人都会显示最先加的那一个，请看清楚再发。发错人本软件不负责。\n
7.如果想删除一个给你发过信息的，你又通过了的人，请打开文件夹中的people文件，删除某两逗号之间的信息，例如{"::ffff:127.0.0.1": "123", "::ffff:192.168.0.107": "\u674e\u56db"}，例如你想删除123这个人，请删除"::ffff:127.0.0.1": "123"。输入中文名字会变成一堆编码例如\\u674e\\u56db,暂时无法解决\n
8.删除好友只需要输入名字（当然，你把ID输入了也没事）\n
9.如果按删除输入名字的那个框没有清空、通讯人没有变化，请检查名字是否正确''')
        a = QHBoxLayout()
        a.addWidget(self.help)
        self.tab3.setLayout(a)

    def resizeEvent(self, *args, **kwargs) -> None:
        x = self.width()
        y = self.height()

    def send_data_slot(self):
        message = self.mes.toPlainText()
        datagram = message.encode()
        try:

            self.sock1.writeDatagram(datagram, QHostAddress(self.contacts[self.choce.currentText()]), 6666)
            self.browser.append("你发送给" + self.choce.currentText() + "一条信息:" + message)
        except:
            QMessageBox.warning(self, '警告', '此用户不存在')

    def add_people(self):
        self.contacts[self.name.toPlainText()] = self.IP.toPlainText()
        self.choce.clear()
        self.choce.addItems(self.contacts)
        with open("contacts.json", "w", encoding="utf-8") as file:
            json.dump(self.contacts, file)
        self.IP.clear()
        self.name.clear()

    def del_people(self):
        if self.name.toPlainText() not in self.contacts:
            return
        del self.contacts[self.name.toPlainText()]
        self.choce.clear()
        self.choce.addItems(self.contacts)
        self.name.clear()
        with open('contacts.json', 'w', encoding="utf-8") as file:
            json.dump(self.contacts, file)

    def read_data_slot(self):
        while self.sock.hasPendingDatagrams():
            sound = QSound("sounds.wav", self)

            datagram, host, port = self.sock.readDatagram(self.sock.pendingDatagramSize())
            if self.is_not(host.toString(), datagram.decode()):
                message = '\n发送人: {}\n{}'.format(self.people[host.toString()], datagram.decode())
                self.browser.append(message)
                sound.play()

    def is_not(self, host, datagram):
        if host in self.people:
            return True
        else:
            confirm = QMessageBox.question(self, "安全验证", "有一个陌生信息,是否通过？验证消息为{}".format(datagram),
                                           QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                name = QInputDialog.getText(self, "询问", "请输入他的名或者填写‘陌生’")
                with open("people.json", "r", encoding="utf-8") as file:
                    self.people = json.load(file)
                self.people[host] = name[0]

                with open("people.json", "w", encoding="utf-8") as file:
                    json.dump(self.people, file)
                return True
            if confirm == QMessageBox.No:
                return False


if __name__ == '__main__':
    from sys import argv, exit

    app = QApplication(argv)
    main = main()
    main.show()
    exit(app.exec_())
