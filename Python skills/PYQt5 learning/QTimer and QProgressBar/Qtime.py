import sys
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout


class Demo(QWidget):
    def __init__(self):
        super(Demo, self).__init__()
        self.label = QLabel('0', self)  # 1
        self.label.setAlignment(Qt.AlignCenter)

        self.step = 0  # 2

        self.timer = QTimer(self)  # 3
        self.timer.timeout.connect(self.update_func)

        self.ss_button = QPushButton('Start', self)  # 4
        self.ss_button.clicked.connect(self.start_stop_func)

        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.label)
        self.v_layout.addWidget(self.ss_button)

        self.setLayout(self.v_layout)

    def start_stop_func(self):
        if not self.timer.isActive():
            self.ss_button.setText('Stop')
            self.timer.start(100)
        else:
            self.ss_button.setText('Start')
            self.timer.stop()

    def update_func(self):
        self.step += 1
        self.label.setText(str(self.step))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())

''' 1.
    首先实例化一个QLabel，并将文本设为0。setAlignment(Qt.AlignCenter)
    可以让QLabel控件在窗口中居中显示，而之前我们是通过addStretch(int)
    方法来让一个控件在布局中居中的，显然通过setAlignment(Qt.AlignCenter)
    方法更加方便：

    self.h_layout.addStretch(1)
    self.h_layout.addWidget(self.label)
    self.h_layout.addStretch(1)
    2.
    step变量用于计数，QLabel控件显示的就是这里的step，程序会通过QTimer来不断增加step的值；

    3.
    其次实例化一个QTimer，并将timeout信号连接到自定义的槽函数update_func()
    上：

    def update_func(self):
        self.step += 1
        self.label.setText(str(self.step))


    每次调用该槽函数就会将step值加1，并且用QLabel显示当前值；

    4.
    最后我们实例化一个QPushButton按钮来控制定时器的启动的停止，连接的自定义的槽函数如下：

    def start_stop_func(self):
        if not self.timer.isActive():
            self.ss_button.setText('Stop')
            self.timer.start(100)
        else:
            self.ss_button.setText('Start')
            self.timer.stop()


    在槽函数中通过isActive()
    方法来判断定时器是否处于激活状态，若没有激活，则将按钮文字变成Stop并通过start(100)
    方法来启动定时器，100
    表示100毫秒，也就是说每过0
    .1
    秒，定时器就会触发timeout信号，并执行update_func()
    槽函数；若已经处于激活状态，则将按钮文字变回Start并通过stop()
    方法停止定时器。



    有些小伙伴可能想在触发timeout信号后只调用一次update_func()，那么我们可以通过setSingleShot(True)
    方法来设置。


'''
