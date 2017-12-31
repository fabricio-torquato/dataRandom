
import glob
import os
import random
import sys
from datetime import datetime
from os import listdir
from os.path import isfile, join

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from PyQt5.QtWidgets import (QApplication, QGridLayout, QGroupBox, QHBoxLayout,
                             QLabel, QPushButton, QSlider, QStyle, QVBoxLayout,
                             QWidget)


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Data Random'
        self.imageNumber = 0
        self.timer = None
        self.visible = False
        self.files = self.getFiles()
        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        self.label = QLabel(self)
        layout.addWidget(self.label, 0, 1)
        layout.addWidget(self.initControl(), 1, 1)
        self.setLayout(layout)

        # Set black theme
        # self.setStyle('Fusion')
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(15, 15, 15))
        palette.setColor(QPalette.AlternateBase,
                         QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)

        palette.setColor(QPalette.Highlight,
                         QColor(142, 45, 197).lighter())
        palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(palette)

        self.setWindowTitle(self.title)
        self.showMaximized()
        self.nextImage()

    def initControl(self):
        self.groupBox = QGroupBox()
        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        self.durationChanged(len(self.files))

        self.pybutton = QPushButton(' Iniciar', self)
        self.pybutton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.pybutton.clicked.connect(self.handleButton)
        self.pybutton.resize(50, 32)
        self.pybutton.move(50, 50)

        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.pybutton)
        controlLayout.addWidget(self.positionSlider)

        self.groupBox.setLayout(controlLayout)

        return self.groupBox

    def getFiles(self):
        onlyfiles = ["data/" + f for f in listdir("data/")]
        return onlyfiles

    def nextImage(self):
        if self.visible:
            self.imageNumber = self.imageNumber + 1
            if self.imageNumber == len(self.files):
                self.stop()
            else:
                self.showImage(self.imageNumber)
            self.visible = False
        else:
            self.showBlackView(self.imageNumber)
            self.visible = True

    def setPosition(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def handleButton(self):
        if(self.timer):
            self.stop()
        else:
            self.play()

    def play(self):
        self.randomList()
        self.imageNumber = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.nextImage)
        self.timer.start(5000)
        self.pybutton.setText(" Parar")
        self.pybutton.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))

    def stop(self):
        self.timer.stop()
        self.timer = None
        self.imageNumber = 0
        self.visible = True
        self.showBlackView(self.imageNumber)
        self.pybutton.setText(" Iniciar")
        self.pybutton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def randomList(self):
        self.files = random.sample(self.files, len(self.files))
        file = open("output/" + str(datetime.now()) + ".txt", "w")
        for (index, value) in enumerate(self.files):
            file.write(str(index) + " " + value.replace("data/", "") + "\n")
        file.close()

    def showImage(self, imageNumber):
        QSound.play("public/beep.wav")
        self.setPosition(imageNumber)
        self.groupBox.setTitle(
            "Centro de controle    Tempo:   " + str(datetime.now()) + "  " + "Image:  " + str(imageNumber) + "      ")
        pixmap = QPixmap(self.files[imageNumber])
        self.label.setScaledContents(False)
        pixmap = pixmap.scaled(760, 950, Qt.KeepAspectRatio)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setPixmap(pixmap)

    def showBlackView(self, imageNumber):
        self.setPosition(imageNumber)
        self.groupBox.setTitle(
            "Centro de controle    Tempo:   " + str(datetime.now()) + "  " + "Image:  " + str(imageNumber) + "      ")
        pixmap = QPixmap("public/None.png")
        self.label.setScaledContents(True)
        pixmap = pixmap.scaled(1080, 950, Qt.KeepAspectRatio)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
