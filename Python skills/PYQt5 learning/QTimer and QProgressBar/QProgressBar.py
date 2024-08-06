import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QProgressBar, QPushButton, QHBoxLayout, QVBoxLayout


class Demo(QWidget):
    def __init__(self):
        super(Demo, self).__init__()
        self.progressbar = QProgressBar(self)  # 1
        # self.progressbar.setOrientation(Qt.Vertical)
        self.progressbar.setMinimum(0)  # 2
        self.progressbar.setMaximum(100)
        # self.progressbar.setRange(0, 100)

        self.step = 0  # 3

        self.timer = QTimer(self)  # 4
        self.timer.timeout.connect(self.update_func)

        self.ss_button = QPushButton('Start', self)  # 5
        self.ss_button.clicked.connect(self.start_stop_func)
        self.reset_button = QPushButton('Reset', self)  # 6
        self.reset_button.clicked.connect(self.reset_func)

        self.h_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()

        self.h_layout.addWidget(self.ss_button)
        self.h_layout.addWidget(self.reset_button)
        self.v_layout.addWidget(self.progressbar)
        self.v_layout.addLayout(self.h_layout)

        self.setLayout(self.v_layout)

    def start_stop_func(self):
        if self.ss_button.text() == 'Start':
            self.ss_button.setText('Stop')
            self.timer.start(100)
        else:
            self.ss_button.setText('Start')
            self.timer.stop()

    def update_func(self):
        self.step += 1
        self.progressbar.setValue(self.step)

        if self.step >= 100:
            self.ss_button.setText('Start')
            self.timer.stop()
            self.step = 0

    def reset_func(self):
        self.progressbar.reset()
        self.ss_button.setText('Start')
        self.timer.stop()
        self.step = 0


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())
'''1. 实例化一个QProgressBar，默认是水平的，但是我们可以通过setOrientation(Qt.Vertical)方法来让进度条垂直显示；

2. 通过setMinimum()和setMaximum()方法来设置范围，也可以单单用setRange()方法来实现，这里我们将范围设为0-100；

3. 这里的step变量用于计数，之后QProgressBar会将值设为step；

4. 实例化一个QTimer，并将timeout信号连接到update_func()槽函数上：

def update_func(self):
    self.step += 1
    self.progressbar.setValue(self.step)

    if self.step >= 100:
        self.ss_button.setText('Start')
        self.timer.stop()
        self.step = 0
每次触发timeout都会调用该槽函数，在这里我们将step值加1，并将progressbar的值设为step，当step值达到pregress的最大值时(也就是说进度条达到100%)，将按钮文本重新设为Start，停止定时器并将step值重设为0；

5. 实例化一个QPushButton按钮来控制QTimer的启动与停止，这里将它的clicked信号和start_stop_func()槽函数连接起来：

def start_stop_func(self):
    if self.ss_button.text() == 'Start':
        self.ss_button.setText('Stop')
        self.timer.start(100)
    else:
        self.ss_button.setText('Start')
        self.timer.stop()
在槽函数中，我们通过按钮文字来进行判断，若为Start，则说明定时器没有启动，所以将按钮文字设为Stop，并且通过start(100)方法来启动，100表示100毫秒，即0.1秒。也就是说之后每隔0.1秒就会触发timeout信号并调用update_func()槽函数；若按钮文字为Stop，则将其设为Start并停止定时器(我们在10.1章节中时通过定时器isActive()方法来的，当然这里也可以使用)；

6. 该实例化的按钮用于重置进度条：

def reset_func(self):
    self.progressbar.reset()
    self.ss_button.setText('Start')
    self.timer.stop()
    self.step = 0
其所连接的槽函数中通过reset()方法来进行重置，还有将按钮文字设为Start，停止定时器以及将step值设为0。

'''