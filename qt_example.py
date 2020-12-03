from PyQt5 import uic
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, QTime, QObject, pyqtSignal, pyqtSlot, QThread, QWaitCondition, QMutex
# qthread -> global / queue / list 로 대기를 쌓는 방법.
# python deck / qt 자체 thread에서 제공하는 data pipeline.

import time
import sys
import os
from collections import deque

path = './sample_imgs/'

form_class = uic.loadUiType("qt_designer.ui")[0]

running_state = False

class Thread1(QThread):
    threadValue = QtCore.pyqtSignal(int)

    def __init__(self):
        QThread.__init__(self)
        self.cond = QWaitCondition()
        self.mutex = QMutex()
        self.deq = deque()

    def __del__(self):
        self.wait()

    def run(self):
        self.count = 0
        while self.isRunning:
            try:
                if self.count < 3:
                    time.sleep(1)
                    print("numbering : ", self.count)
                    self.deq.appendleft(self.count)
                    self.count += 1
                if(self.count == 3):
                    self.save()
                    self.threadValue.emit(self.two)
                    print(self.two)
                    self.count = 0
            except:
                pass

    def save(self):
        if self.deq:    # 비어있지 않다면,
            print(self.deq)
            self.two = self.deq.popleft()   # 2 꺼내기.
            self.deq.clear()    # 초기화
            pass
        else:           # 비어있다면,
            print("it's empty")
            pass


class Ui_Dialog(QDialog, form_class):
    sig_number = pyqtSignal()

    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.timer = QTimer(self)  # 타이머 객체 생성
        self.timer.timeout.connect(self.fibonacci)  # 슬롯 timeout() 객체 호출
        self.thread = Thread1()
        self.thread.threadValue.connect(self.eventHandler)

    @pyqtSlot()
    def numbering(self):
        self.thread.start()
        print(self.thread.isRunning())

    twos = 0
    @pyqtSlot(int)
    def eventHandler(self, two):
        self.twos += two
        self.h_1_textlabel.setText(str(self.twos))
        pass

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.h_1_textlabel.setText(_translate("Dialog", "0"))
        self.h_1_button.setText(_translate("Dialog", "+1"))
        self.h_2_textlabel.setText(_translate("Dialog", "0"))
        self.h_2_button.setText(_translate("Dialog", "피보나치"))
        self.h_3_textlabel.setText(_translate("Dialog", "Image"))
        self.h_3_button.setText(_translate("Dialog", "이미지 바꾸기"))


    a, b = 0, 1
    def fibonacci(self):
        for i in range(100000):
            if(i % 1000 == 0):
                print("fibbonacci : ", i)
        if running_state == True :
            self.timer.start(1000 * 1)  # 1초마다 타이머 실행, 시작
            self.a, self.b = self.b, self.a + self.b
            self.h_2_textlabel.setText(str(self.a))
        else:
            self.timer.stop()
    # with fibonacci
    def start(self):
        global running_state
        if running_state == False:
            running_state = True
            self.fibonacci()
        else:
            running_state = False
            self.fibonacci()


    idx = 0
    filelist = os.listdir(path)
    def image_load(self):
        pixmap = QtGui.QPixmap(path)
        pixmap.load(path+"images_{0}.jpg".format(self.idx))
        self.h_3_textlabel.setPixmap(QtGui.QPixmap(pixmap))
        self.idx += 1
        print(self.idx)
        if (self.idx == 10):
            self.idx = 0

"""
class Deque(Queue):
    def enqueue_back(self, item):
        self.items.append(item)

    def dequeue_front(self):
        value = self.items.pop(0)
        if value is not None:
            return value
        else:
            print("Deque is empty")

"""
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()

    ui.setupUi(Dialog)

    ui.h_1_button.clicked.connect(ui.numbering)
    ui.h_2_button.clicked.connect(ui.start)
    ui.h_3_button.clicked.connect(ui.image_load)


    Dialog.show()
    sys.exit(app.exec_())