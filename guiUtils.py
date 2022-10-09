import serial
import threading
import numpy as np
import sys
import re
from PySide6.QtWidgets import *
from PySide6.QtGui import *
import pyqtgraph as pg
import matplotlib.pyplot as plt
from main_cli import plot_IQData_fftOut1D_withoutDC,plot_IQData_fftOut1D


def load_IQGUI():
    #绘制IQ图的gui界面
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
    dcEdit.activated.connect(passDC)#IQ图是否去DC显示

    nBeamEdit=QComboBox()
    nBeamEdit.addItems(["1","4","8"])
    nBeamEdit.setCurrentIndex(0)
    nBeamEdit.activated.connect(passNBeam)#默认1天线

    btn_generator = QPushButton('IQGrpah Generator')
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