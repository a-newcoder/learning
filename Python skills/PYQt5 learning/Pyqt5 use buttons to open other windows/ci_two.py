from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow


class Ui_MainWindow(QMainWindow):  # 本来class Ui_MainWindow的实例是不能随意使用的，但因为继承了，就可以使用了
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        # super().__init__()
        self.setupUi(self)
        print(type(self))

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(550, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)  # 给Qwidget设置父窗口
        self.centralwidget.setObjectName("centralwidget")

        self.pushButton1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton1.setGeometry(QtCore.QRect(120, 80, 93, 28))  # 前两个参数是位置，后两个参数是按钮大小
        self.pushButton1.setObjectName("pushButton")

        self.pushButton2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton2.setGeometry(QtCore.QRect(120, 130, 93, 28))
        self.pushButton2.setObjectName("pushButton")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 550, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.pushButton2.clicked.connect(MainWindow.close)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow2"))
        self.pushButton1.setText(_translate("MainWindow", "ci-2"))
        self.pushButton2.setText(_translate("MainWindow", "退出"))