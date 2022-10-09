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
from main_cli import plot_ampSpectrum_fftOut1D,plot_ampSpectrum_fftOut1D_withoutDC

dcList = ['with dc', 'without dc']
withoutDC=False#默认存在DC
nBeam=1
filePath = r"D:\Minjl\阶段六：验证model数据\mat文件\4.20头端雷达\闵佳乐\手大幅度adc_data.mat"
frameIdxs=[0,10]
rangeIdxs=[0,1,2,3,4,5,6,7]

def press_Generator():
    global withoutDC,frameIdxs,filePath,nBeam,rangeIdxs
    if withoutDC==True:
        plot_ampSpectrum_fftOut1D_withoutDC(filePath, frameIdxs, nBeam,rangeIdxs)
    else:
        plot_ampSpectrum_fftOut1D(filePath, frameIdxs, nBeam,rangeIdxs)
    plt.show()

def press_Close():
    plt.close('all')


def passDC(indx):
    global dcList,withoutDC
    if dcList[indx]=="with dc":
        withoutDC=False
    else:
        withoutDC=True

def passFrameIdx(txt):
    global frameIdxs
    frames = re.findall("\d+\.?\d*", txt)  # 正则表达式
    frameIdxs = []
    for i in frames:
        frameIdxs.append(int(i))



def passRangeIdx(txt):
    global rangeIdxs
    rangeBins = re.findall("\d+\.?\d*", txt)  # 正则表达式
    rangeIdxs = [int(i) for i in rangeBins]

def passNBeam(indx):
    global nBeam
    beamList=["1","4","8"]
    nBeam=int(beamList[indx])



def passFilepath(txt):
    global filePath
    filePath=str(txt)


if __name__ == "__main__":
    app = QApplication([])
    w=QWidget()

    '2. amp generator部分'
    pathEdit=QLineEdit()
    pathEdit.setText(filePath)
    pathEdit.textChanged.connect(passFilepath)#导入文件名
    frameIdxEdit=QLineEdit()
    frameIdxEdit.setText("[0,10]")
    frameIdxEdit.textChanged.connect(passFrameIdx)#IQ图显示几个frame数据
    rangeIdxEdit=QLineEdit()
    rangeIdxEdit.setText("[0,1,2,3,4,5,6,7]")
    rangeIdxEdit.textChanged.connect(passRangeIdx)#使用预设的8个rangeBin分析，是否只选择部分
    dcEdit=QComboBox()
    dcEdit.addItems(dcList)
    dcEdit.setCurrentIndex(0)
    dcEdit.activated.connect(passDC)#IQ图是否去DC显示
    nBeamEdit=QComboBox()
    nBeamEdit.addItems(["1","4","8"])
    nBeamEdit.setCurrentIndex(0)
    nBeamEdit.activated.connect(passNBeam)#默认1天线
    btn_generator = QPushButton('AMPGrpah Generator')
    btn_generator.clicked.connect(press_Generator)
    btn_close = QPushButton('Close All')
    btn_close.clicked.connect(press_Close)
    layout=QGridLayout()
    formLayout=QFormLayout()
    w.setLayout(layout)
    formLayout.addRow("filePath            ",pathEdit)
    formLayout.addRow("frameIdxs       ",frameIdxEdit)
    formLayout.addRow("rangeIdxs       ",rangeIdxEdit)
    formLayout.addRow("withDC       ",dcEdit)
    formLayout.addRow("nBeam       ",nBeamEdit)
    layout.addLayout(formLayout,0,0)
    layout.addWidget(btn_generator,1,0)
    layout.addWidget(btn_close,2,0)
    w.setWindowTitle("amp")
    w.show()
    app.exec()