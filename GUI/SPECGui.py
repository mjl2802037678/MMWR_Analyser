"spectrogram gui"
"""
2022.8.23
该版本增加保存按钮，open seiral后不自动存储数据，点击save后才自动保存数据
可以随时保存，不用重启
"""
import serial
import threading
import numpy as np
import sys
import re
from PySide6.QtWidgets import *
from PySide6.QtGui import *
import pyqtgraph as pg
import matplotlib.pyplot as plt
from main_cli import plot_spectrogram,plot_spectrogram_basedFrames


meanList=["NO", "YES"]
withoutMEAN=True#默认不求均值

nBeam=1
threshold=60
filePath = r"D:\Minjl\阶段六：验证model数据\mat文件\4.20头端雷达\闵佳乐\手大幅度adc_data.mat"

#针对based frames panel的参数设置, nseg点短时傅里叶变化
nseg_1=20
nBeam_1=1
threshold_1=60

def press_Generator():
    global filePath,nBeam,threshold
    global withoutMEAN,nseg_1,nBeam_1,threshold_1
    if withoutMEAN:
        plot_spectrogram(filePath, nBeam, threshold)
    else:
        #每个frame求均值，然后stft
        plot_spectrogram_basedFrames(filePath, nseg_1, nBeam_1, threshold_1)
    plt.show()

def press_Close():
    plt.close('all')


def passThreshold(txt):
    global threshold
    threshold=int(txt)
def passThreshold_1(txt):
    global threshold_1
    threshold_1=int(txt)


def passNBeam(indx):
    global nBeam
    beamList=["1","4","8"]
    nBeam=int(beamList[indx])
def passNBeam_1(indx):
    global nBeam_1
    beamList=["1","4","8"]
    nBeam_1=int(beamList[indx])

def passNSeg_1(txt):
    global nseg_1
    nseg_1=int(txt)
def passMEAN(indx):
    global meanList,withoutMEAN
    if meanList[indx]=="NO":
        withoutMEAN=True
    else:
        withoutMEAN=False

def passFilepath(txt):
    global filePath
    filePath=str(txt)


if __name__ == "__main__":
    app = QApplication([])
    w=QWidget()
    layout=QGridLayout()

    '1. IQ generator部分'
    pathEdit=QLineEdit()
    pathEdit.setText(filePath)
    pathEdit.textChanged.connect(passFilepath)#导入文件名
    nBeamEdit=QComboBox()
    nBeamEdit.addItems(["1","4","8"])
    nBeamEdit.setCurrentIndex(0)
    nBeamEdit.activated.connect(passNBeam)#默认1天线
    thresholdEdit=QLineEdit()
    thresholdEdit.setText(str(threshold))
    thresholdEdit.textChanged.connect(passThreshold)#导入文件名
    formLayout = QFormLayout()
    formLayout.addRow("filePath            ",pathEdit)
    formLayout.addRow("nBeam       ",nBeamEdit)
    formLayout.addRow("threshold       ",thresholdEdit)

    '2. 对frame生成average点进行stft'
    extraLabel = QLabel("Based Frames, STFT config")
    meanEdit = QComboBox()
    meanEdit.addItems(meanList)
    meanEdit.setCurrentIndex(0)
    meanEdit.activated.connect(passMEAN)  # 默认不对chirps进行平均
    nBeamEdit_1 = QComboBox()
    nBeamEdit_1.addItems(["1", "4", "8"])
    nBeamEdit_1.setCurrentIndex(0)
    nBeamEdit_1.activated.connect(passNBeam_1)  # 默认1天线
    thresholdEdit_1 = QLineEdit()
    thresholdEdit_1.setText(str(threshold_1))
    thresholdEdit_1.textChanged.connect(passThreshold_1)  # 导入文件名
    nsegEdit_1 = QLineEdit()
    nsegEdit_1.setText(str(nseg_1))
    nsegEdit_1.textChanged.connect(passNSeg_1)  # 导入文件名
    formLayout_1 = QFormLayout()
    formLayout_1.addRow(extraLabel)
    formLayout_1.addRow("MEAN       ", meanEdit)
    formLayout_1.addRow("nSeg_1       ", nsegEdit_1)
    formLayout_1.addRow("nBeam_1       ", nBeamEdit_1)
    formLayout_1.addRow("threshold_1       ", thresholdEdit_1)




    btn_generator = QPushButton('Spectrogram Generator')
    btn_generator.clicked.connect(press_Generator)
    btn_close = QPushButton('Close All')
    btn_close.clicked.connect(press_Close)
    layout.addLayout(formLayout,0,0)
    layout.addLayout(formLayout_1,1,0)
    layout.addWidget(btn_generator,2,0)
    layout.addWidget(btn_close,3,0)
    w.setLayout(layout)
    w.setWindowTitle("spectrogram")
    w.show()
    app.exec()