# form https://blog.csdn.net/weixin_69832035/article/details/125611039

import sys

from PyQt5.QtCore import Qt, QEvent, QChildEvent, QTimerEvent, QObject
from PyQt5.QtGui import QMouseEvent, QWheelEvent, QDropEvent, QFocusEvent, QDragMoveEvent, \
    QDragEnterEvent, QDragLeaveEvent, QTabletEvent, QCloseEvent, QShowEvent, QHideEvent, QMoveEvent, QResizeEvent, \
    QPaintEvent
from PyQt5.QtWidgets import QApplication, QWidget, QLabel


# 把上边 PyQt5 替换成 PySide2 也可以正常运行!
class QmyWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.resize(400, 400)
        self.setWindowTitle('事件委托')
        self.laba = QLabel(self)
        self.laba.setText('I am Label A')
        font = self.laba.font()
        font.setPointSize(10)
        font.setBold(True)
        self.laba.setFont(font)
        self.laba.setGeometry(20, 20, 300, 60)
        self.laba.installEventFilter(self)
        self.labb = QLabel(self)
        self.labb.setText('I am Label B')
        font = self.labb.font()
        font.setPointSize(10)
        font.setBold(True)
        self.labb.setFont(font)
        self.labb.setGeometry(20, 100, 300, 60)
        self.labb.installEventFilter(self)
        # self.installEventFilter(self)

        self.grabKeyboard()  # 控件开始捕获键盘 只有控件开始捕获键盘，控件的键盘事件才能收到消息
        self.setMouseTracking(True)  # 只有设置此参数，鼠标移动才会实时连续响应

    def eventFilter(self, a0: 'QObject', a1: 'QEvent') -> bool:
        print('事件过滤', a0, a1)
        if a0 == self.laba:
            if a1.type() == QEvent.Enter:
                self.laba.setText('鼠标来啦')
                self.laba.setStyleSheet('background-color:rgb(170,255,255);')
            if a1.type() == QEvent.Leave:
                self.laba.setText('I am Label A')
                self.laba.setStyleSheet('')
        if a0 == self.labb:
            if a1.type() == QEvent.Enter:
                self.labb.setText('点我！')
                self.labb.setStyleSheet('background-color:rgb(85,255,127);')
            if a1.type() == QEvent.MouseButtonPress:
                self.labb.setText('还真点啊！')
                self.labb.setStyleSheet('background-color:rgb(85,255,127);')
            if a1.type() == QEvent.MouseButtonRelease:
                self.labb.setText('点我！')
                self.labb.setStyleSheet('background-color:rgb(85,255,127);')
            if a1.type() == QEvent.Leave:
                self.labb.setText('I am Label B')
                self.labb.setStyleSheet('')
        return super().eventFilter(a0, a1)

    def mouseMoveEvent(self, a0: QMouseEvent) -> None:  # 鼠标移动事件
        # 参考 https://blog.csdn.net/weixin_45553177/article/details/104513333
        print('鼠标移动', a0)
        aa = f'''
        # {a0.x()} 和 {a0.y()} # 返回相对于控件的鼠标坐标值;
        # {a0.pos()}  #  返回相对于控件空间的QPoint对象;
        # {a0.localPos()} # 返回相对于控件空间的QPointF对象;
        # {a0.globalX()} 和 {a0.globalY()}  #   返回相对于屏幕的x,y 坐标值；
        # {a0.globalPos()}  #  返回相对于屏幕的QPoint对象;
        # {a0.windowPos()}  #   返回相对于窗口的QPointF对象; 
        # {a0.screenPos()}  #  返回相对于屏幕的QPointF对象; 
        # {a0.buttons()}  #  返回前面所列枚举值的组合，用于判断同时按下了哪些键。
        #     # QtCore.Qt.NoButton - 0 - 没有按下鼠标键。例如移动鼠标时的button()返回值；
        #     # QtCore.Qt.LeftButton -1 -按下鼠标左键；
        #     # QtCore.Qt.RightButton -2 -按下鼠标右键；
        #     # QtCore.Qt.Mion 或 QtCore.Qt.MiddleButton -4 -按下鼠标中键；
        # {a0.modifiers()}  #  判断按下了哪些修饰键（Shift,Ctrl , Alt,等等）,详见键盘事件(18)中的modifiers()。
        # {a0.timestamp()}  #   返回事件发生的时间 毫秒；
        '''
        print(aa)
        return super().mouseMoveEvent(a0)

    def wheelEvent(self, a0: QWheelEvent) -> None:
        print('鼠标滚轮', a0)
        aa = f'''
        {a0.angleDelta()} - 返回QPoint对象，为滚轮转过的数值，单位为1/8度。例如：
        angle=event.angleDelta( ) /8
        angleX=angle.x()
        angleY=angle.y()
        {a0.pixelDelta()} - 返回QPoint对象，为滚轮转过的像素值。
        {a0.x()} 和 {a0.y()} - 返回相对于控件的当前鼠标的x,y位置;
        {a0.pos()} - 返回相对于控件的当前鼠标位置的QPoint对象;
        {a0.posF()} - 返回相对于控件的当前鼠标位置的QPoinFt对象;
        {a0.globalX()} 和{a0.globalY()} - 返回相对于屏幕的当前鼠标的x,y位置;
        {a0.globalPos()} - 返回相对于屏幕的当前鼠标QPoint位置;
        {a0.globalPosF()} - 返回相对于屏幕的当前鼠标QPointF位置;
        {a0.buttons()},{a0.modifiers()}和{a0.timestamp()}的用法参见本文“1.按下、松开鼠标按键”中的相关内容。
        '''
        print(aa)
        angle = a0.angleDelta() / 8
        angleX = angle.x()
        angleY = angle.y()
        print(angleX, angleY)
        return super().wheelEvent(a0)

    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:  # 鼠标键松开时调用;
        print('鼠标松开', a0)
        aa = f'''
        # {a0.x()} 和 {a0.y()} # 返回相对于控件空间的鼠标坐标值;
        # {a0.pos()}  #  返回相对于控件空间的QPoint对象;
        # {a0.localPos()} # 返回相对于控件空间的QPointF对象;
        # {a0.globalX()} 和 {a0.globalY()}  #   返回相对于屏幕的x,y 坐标值；
        # {a0.globalPos()}  #  返回相对于屏幕的QPoint对象;
        # {a0.windowPos()}  #   返回相对于窗口的QPointF对象; 
        # {a0.screenPos()}  #  返回相对于屏幕的QPointF对象; 
        # {a0.buttons()}  #  返回前面所列枚举值的组合，用于判断同时按下了哪些键。
        #     # QtCore.Qt.NoButton - 0 - 没有按下鼠标键。例如移动鼠标时的button()返回值；
        #     # QtCore.Qt.LeftButton -1 -按下鼠标左键；
        #     # QtCore.Qt.RightButton -2 -按下鼠标右键；
        #     # QtCore.Qt.Mion 或 QtCore.Qt.MiddleButton -4 -按下鼠标中键；
        # {a0.modifiers()}  #  判断按下了哪些修饰键（Shift,Ctrl , Alt,等等）,详见键盘事件(18)中的modifiers()。
        # {a0.timestamp()}  #   返回事件发生的时间 毫秒；
        '''
        print(aa)

        # 参考 https://blog.csdn.net/richenyunqi/article/details/80554257
        # 左键按下
        if a0.button() == Qt.LeftButton:
            print("左")
        # 右键按下
        elif a0.button() == Qt.RightButton:
            print("右")
        # 中键按下
        elif a0.button() == Qt.MidButton:
            print("中")
        # 左右键同时按下 以下测试没起作用
        elif a0.button() == Qt.LeftButton | Qt.RightButton:
            print("左右")
        # 左中键同时按下
        elif a0.button() == Qt.LeftButton | Qt.MidButton:
            print("左中")
        # 右中键同时按下
        elif a0.button() == Qt.MidButton | Qt.RightButton:
            print("右中")
        # 左中右键同时按下
        elif a0.button() == Qt.LeftButton | Qt.MidButton | Qt.RightButton:
            print("左中右")

        print(a0.button(), Qt.LeftButton, Qt.MidButton, Qt.RightButton)
        return super().mouseReleaseEvent(a0)

    def mouseDoubleClickEvent(self, a0: QMouseEvent) -> None:  # 双击鼠标时调用
        print('鼠标双击', a0)
        aa = f'''
        # {a0.x()} 和 {a0.y()} # 返回相对于控件空间的鼠标坐标值;
        # {a0.pos()}  #  返回相对于控件空间的QPoint对象;
        # {a0.localPos()} # 返回相对于控件空间的QPointF对象;
        # {a0.globalX()} 和 {a0.globalY()}  #   返回相对于屏幕的x,y 坐标值；
        # {a0.globalPos()}  #  返回相对于屏幕的QPoint对象;
        # {a0.windowPos()}  #   返回相对于窗口的QPointF对象; 
        # {a0.screenPos()}  #  返回相对于屏幕的QPointF对象; 
        # {a0.buttons()}  #  返回前面所列枚举值的组合，用于判断同时按下了哪些键。
        #     # QtCore.Qt.NoButton - 0 - 没有按下鼠标键。例如移动鼠标时的button()返回值；
        #     # QtCore.Qt.LeftButton -1 -按下鼠标左键；
        #     # QtCore.Qt.RightButton -2 -按下鼠标右键；
        #     # QtCore.Qt.Mion 或 QtCore.Qt.MiddleButton -4 -按下鼠标中键；
        # {a0.modifiers()}  #  判断按下了哪些修饰键（Shift,Ctrl , Alt,等等）,详见键盘事件(18)中的modifiers()。
        # {a0.timestamp()}  #   返回事件发生的时间 毫秒；
        '''
        print(aa)
        return super().mouseDoubleClickEvent(a0)

    def keyPressEvent(self, QKeyEvent) -> None:  # 键盘某个键被按下时调用
        # keyPressEvent(QKeyEvent)    键盘按下时调用
        # keyReleaseEvent(QKeyEvent)      键盘释放时调用
        print('按下了键盘:', QKeyEvent.key(), 'ctrl' if QKeyEvent.modifiers() == Qt.ControlModifier else '',
              'shift' if QKeyEvent.modifiers() == Qt.ShiftModifier else '',
              'alt' if QKeyEvent.modifiers() == Qt.AltModifier else '')
        # 参数1  控件
        if QKeyEvent.key() == Qt.Key_A:  # 判断是否按下了A键
            # key()  是普通键
            print('按下了A键')
        if QKeyEvent.modifiers() == Qt.ControlModifier and QKeyEvent.key() == Qt.Key_A:  # 两键组合
            # modifiers()   判断修饰键
            # Qt.NoModifier   没有修饰键
            # Qt.ShiftModifier    Shift键被按下
            # Qt.ControlModifier    Ctrl键被按下
            # Qt.AltModifier      Alt键被按下
            print('按下了Ctrl-A键')
        if QKeyEvent.modifiers() == Qt.ControlModifier | Qt.ShiftModifier and QKeyEvent.key() == Qt.Key_A:  # 三键组合
            print('按下了Ctrl+Shift+A键')
        return super().keyPressEvent(QKeyEvent)

    '''所有窗口事件 参考 https://blog.csdn.net/weixin_39955953/article/details/110981759?utm_term=pyqt5%20%E7%AA%97%E5%8F%A3%E7%BC%A9%E6%94%BE%E4%BA%8B%E4%BB%B6&utm_medium=distribute.pc_aggpage_search_result.none-task-blog-2~all~sobaiduweb~default-0-110981759-null-null&spm=3001.4430'''

    def changeEvent(self, a0: QEvent) -> None:
        print('当控件的窗口状态的状态发生变化时调用', a0)
        return super().changeEvent(a0)

    def showEvent(self, a0: QShowEvent) -> None:
        print('当控件显示时调用。event参数包含QShowEvent类的实例。', a0)
        return super().showEvent(a0)

    def hideEvent(self, a0: QHideEvent) -> None:
        print('当控件隐藏时调用。event参数包含QHideEvent类的实例。', a0)
        return super().hideEvent(a0)

    def moveEvent(self, a0: QMoveEvent) -> None:
        print('窗口移动时，将持续调用该方法。', a0)
        print(f'{a0.pos()}:返回包括窗口当前坐标的QPoint类对象；{a0.oldPos()}:返回包括窗口移动前坐标的QPoint类对象。')
        return super().moveEvent(a0)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        print('调整窗口尺寸时，将持续调用该方法。', a0)
        print(f'{a0.size()}:返回包括窗口当前尺寸的QSize类对象;{a0.oldSize()}:返回包括窗口调整前尺寸的QSize类对象')
        return super().resizeEvent(a0)

    def paintEvent(self, a0: QPaintEvent) -> None:
        print('执行重绘动作', a0)
        print(f'{a0.rect()}:返回包含需要重绘区域的QRect类的对象;{a0.region()}:返回包含需要重绘区域的QRegiont类的对象')
        return super().paintEvent(a0)

    def closeEvent(self, a0: QCloseEvent) -> None:
        print('关闭窗口时调用', a0)
        return super().closeEvent(a0)

    # 其它事件
    def leaveEvent(self, a0: QEvent) -> None:
        print('鼠标离开', a0)
        return super().leaveEvent(a0)

    def enterEvent(self, a0: QEvent) -> None:
        print('鼠标进入', a0)
        return super().enterEvent(a0)

    def event(self, a0: QEvent) -> bool:
        print('所有事件集合处，即所有事件均会先激活本方法', a0)
        return super().event(a0)

    def eventFilter(self, a0: 'QObject', a1: 'QEvent') -> bool:
        print('事件过滤器', a0, a1)
        return super().eventFilter(a0, a1)

    def childEvent(self, a0: 'QChildEvent') -> None:
        return super().childEvent(a0)

    def timerEvent(self, a0: 'QTimerEvent') -> None:
        print('时间控制器', a0)
        return super().timerEvent(a0)

    def focusInEvent(self, a0: QFocusEvent) -> None:
        print('部件或窗口获得焦点', a0)
        return super().focusInEvent(a0)

    def focusOutEvent(self, a0: QFocusEvent) -> None:
        print('部件或窗口失去焦点', a0)
        return super().focusOutEvent(a0)

    def dropEvent(self, a0: QDropEvent) -> None:
        print('drop拖拽控件时发生', a0)
        return super().dropEvent(a0)

    def dragMoveEvent(self, a0: QDragMoveEvent) -> None:
        print('drop拖拽控件移动时发生', a0)
        return super().dragMoveEvent(a0)

    def dragEnterEvent(self, a0: QDragEnterEvent) -> None:
        print('drop拖拽控件进入时发生', a0)
        return super().dragEnterEvent(a0)

    def dragLeaveEvent(self, a0: QDragLeaveEvent) -> None:
        print('drop拖拽控件离开时发生', a0)
        return super().dragLeaveEvent(a0)

    def tabletEvent(self, a0: QTabletEvent) -> None:
        print('QTabletEvent事件', a0)
        return super().tabletEvent(a0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = QmyWidget()
    form.show()
    sys.exit(app.exec_())