from PyQt5 import uic
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, QTime

import sys
import os
import cv2

path = './sample_imgs/'
form_class = uic.loadUiType("qt_designer.ui")[0]

running_state = False
# 설정문제같다.
class Ui_Dialog(QDialog, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.timer = QTimer(self)  # 타이머 객체 생성
        self.timer.timeout.connect(self.fibonacci)  # 슬롯 timeout() 객체 호출

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.h_1_textlabel.setText(_translate("Dialog", "0"))
        self.h_1_button.setText(_translate("Dialog", "+1"))
        self.h_2_textlabel.setText(_translate("Dialog", "0"))
        self.h_2_button.setText(_translate("Dialog", "피보나치"))
        self.h_3_textlabel.setText(_translate("Dialog", "Image"))
        self.h_3_button.setText(_translate("Dialog", "이미지 바꾸기"))


    number = 0
    def numbering(self):
        timeVar = QTimer()
        timeVar.setInterval(1000)
        timeVar.start()
        self.h_1_textlabel.setText(str(self.number))
        self.number += 1


    a, b = 0, 1
    flag = False
    def fibonacci(self):
        for i in range(0,10000000):
            print(i)
        if running_state == True :
            self.timer.start(1000 * 1)  # 1초마다 타이머 실행, 시작
            self.a, self.b = self.b, self.a + self.b
            self.h_2_textlabel.setText(str(self.a))
        else:
            self.timer.stop()


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
    print(filelist)
    def image_load(self):
        pixmap = QtGui.QPixmap(path)
        pixmap.load(path+"images_{0}.jpg".format(self.idx))
        self.h_3_textlabel.setPixmap(QtGui.QPixmap(pixmap))
        self.idx += 1
        print(self.idx)
        if (self.idx == 10):
            self.idx = 0


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
