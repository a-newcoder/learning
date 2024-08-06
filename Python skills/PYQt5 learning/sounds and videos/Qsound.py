import sys
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton


class Demo(QWidget):
    def __init__(self):
        super(Demo, self).__init__()
        self.sound = QSound('sounds.wav', self)              # 1

        self.play_btn = QPushButton('Play Sound', self)
        self.play_btn.clicked.connect(self.sound.play)      # 2


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())