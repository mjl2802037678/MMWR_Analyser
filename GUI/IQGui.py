import serial
import threading
import numpy as np
import sys
import re
from PySide6.QtWidgets import *
from PySide6.QtGui import *
import pyqtgraph as pg
import matplotlib.pyplot as plt
from main_cli import plot_IQData_fftOut1D_withoutDC,plot_IQData_fftOut1D, plot_IQData_fftOut1D_basedFrames

dcList = ['with dc', 'without dc']
meanList=["NO", "YES"]
withoutDC=False#默认存在DC
withoutMEAN=True#默认不求均值
nBeam=1
filePath = r"D:\Minjl\阶段六：验证model数据\mat文件\4.20头端雷达\闵佳乐\手大幅度adc_data.mat"
frameIdxs=[]
frameIdxs.extend(range(0,10))
frameIdxs.extend(range(20,30))

rangeIdxs=[0,1,2,3,4,5,6,7]

def press_Generator():
    global withoutDC,frameIdxs,filePath,nBeam,rangeIdxs
    global withoutMEAN

    if withoutMEAN==True:
        if withoutDC==True:
            plot_IQData_fftOut1D_withoutDC(filePath, frameIdxs, nBeam,rangeIdxs)
        else:
            plot_IQData_fftOut1D(filePath, frameIdxs, nBeam,rangeIdxs)
    else:
        #frame内求均值，暂时不考虑这些frame之间去DC
        plot_IQData_fftOut1D_basedFrames(filePath, frameIdxs, nBeam, rangeIdxs)

    plt.show()

def press_Close():
    plt.close('all')


def passDC(indx):
    global dcList,withoutDC
    if dcList[indx]=="with dc":
        withoutDC=False
    else:
        withoutDC=True

def passMEAN(indx):
    #每个frame对所有chirp进行均值
    global meanList,withoutMEAN
    if meanList[indx]=="NO":
        withoutMEAN=True
    else:
        withoutMEAN=False

def passFrameIdx(txt):
    global frameIdxs
    frames = re.findall("\d+\.?\d*", txt)  # 正则表达式
    # frameIdxs=[int(i) for i in frames]
    startIdx=0
    endIdx=0
    frameIdxs = []
    for i in range(len(frames)):
        if i%2==0:
            startIdx=int(frames[i])
        else:
            endIdx=int(frames[i])
            frameIdxs.extend(range(startIdx, endIdx))



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
    layout=QGridLayout()

    '1. IQ generator部分'
    pathEdit=QLineEdit()
    pathEdit.setText(filePath)
    pathEdit.textChanged.connect(passFilepath)#导入文件名
    frameIdxEdit=QLineEdit()
    frameIdxEdit.setText("[0,10),[20,30)")
    frameIdxEdit.textChanged.connect(passFrameIdx)#IQ图显示几个frame数据
    rangeIdxEdit=QLineEdit()
    rangeIdxEdit.setText("[0,1,2,3,4,5,6,7]")
    rangeIdxEdit.textChanged.connect(passRangeIdx)#使用预设的8个rangeBin分析，是否只选择部分
    dcEdit=QComboBox()
    dcEdit.addItems(dcList)
    dcEdit.setCurrentIndex(0)
    dcEdit.activated.connect(passDC)#IQ图是否去DC显示；如果extraPanel中选择mean，此处dc对应了frames序列的dc
    nBeamEdit=QComboBox()
    nBeamEdit.addItems(["1","4","8"])
    nBeamEdit.setCurrentIndex(0)
    nBeamEdit.activated.connect(passNBeam)#默认1天线
    btn_generator = QPushButton('IQGrpah Generator')
    btn_generator.clicked.connect(press_Generator)
    btn_close = QPushButton('Close All')
    btn_close.clicked.connect(press_Close)

    "基础的IQ选项panel,基于chirp之间分析"
    formLayout_0=QFormLayout()
    formLayout_0.addRow("filePath            ",pathEdit)
    formLayout_0.addRow("frameIdxs       ",frameIdxEdit)
    formLayout_0.addRow("rangeIdxs       ",rangeIdxEdit)
    formLayout_0.addRow("withDC       ",dcEdit)
    formLayout_0.addRow("nBeam       ",nBeamEdit)
    layout.addLayout(formLayout_0, 0, 0)

    "增加额外的panel，基于frame进行分析；"
    extraLabel=QLabel("Based Frames")
    meanEdit=QComboBox()
    meanEdit.addItems(meanList)
    meanEdit.setCurrentIndex(0)
    meanEdit.activated.connect(passMEAN)  #默认不对chirps进行平均
    formLayout_1 = QFormLayout()
    formLayout_1.addRow(extraLabel)
    formLayout_1.addRow("MEAN        ",meanEdit)

    layout.addLayout(formLayout_1, 1, 0)
    layout.addWidget(btn_generator,2,0)
    layout.addWidget(btn_close,3,0)
    w.setLayout(layout)
    w.setWindowTitle("IQ data")
    w.show()
    app.exec()