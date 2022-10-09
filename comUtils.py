"""
一些常用的utils工具函数
"""
import numpy as np
import os
import math
import pandas as pd
from globVar import GLCM_CLASS
from numpy.fft import fft,fftshift




"Rx beamforming"
def RxBeamforming_numRx(dataIn,selRange,selAngle,nBeamform,numDopplerBins,numTx):
    #某个selRange处对应的selAngle，进行nBeamform天线成形，对钱numDopplerBin个Chirp数据，128Chirp，一开始设置了numTx发射
    #只考虑一个virtual rx，接收了128个chirp数据，进行dopplerFFT，生成128dopplerBins
    radarCubeFFT1D = np.zeros((nBeamform, numDopplerBins), dtype=complex)
    bin_val=np.zeros((numDopplerBins),dtype=complex)
    if nBeamform==1:
        for dopplerIdx in range(numDopplerBins):
            tempDopplerIdx = dopplerIdx * numTx
            tup=dataIn[tempDopplerIdx, 0, selRange]
            radarCubeFFT1D[0, dopplerIdx] = complex(tup[0], tup[1])
            bin_val[dopplerIdx]=radarCubeFFT1D[0, dopplerIdx]#原本*8
    elif nBeamform==4:
        for dopplerIdx in range(numDopplerBins):
            tempDopplerIdx = dopplerIdx * numTx
            for rx in range(nBeamform):
                tup = dataIn[tempDopplerIdx, rx, selRange]
                radarCubeFFT1D[rx, dopplerIdx] = complex(tup[0], tup[1])
            bin_val[dopplerIdx] = beamforming(radarCubeFFT1D[:, dopplerIdx],selAngle) # 该chirp单个range聚合 *2
    elif nBeamform==8:
        for dopplerIdx in range(numDopplerBins):
            for tx in range(numTx):
                tempDopplerIdx = dopplerIdx * numTx + tx
                for rx in range(4):
                    virtualIdx = tx * 4 + rx
                    tup = dataIn[tempDopplerIdx, rx, selRange]
                    radarCubeFFT1D[virtualIdx, dopplerIdx] = complex(tup[0], tup[1])
            bin_val[dopplerIdx] = beamforming(radarCubeFFT1D[:, dopplerIdx],selAngle)  # 该chirp单个range聚合
    return bin_val#该frame数据dataIn在某个selRange上，128chirp点8天线成形后结果
def beamforming(rangeProf,theta):
    # 每个chirp，8个天线进行beamforming，总共128次beamformign
    sind = math.sin(math.radians(theta))  # theta是角度，转成弧度
    pi=math.pi
    temp_bin_val=0j
    for idx in range(len(rangeProf)):
        A=np.exp(-1j*pi*idx*sind)
        temp_bin_val=temp_bin_val+A*rangeProf[idx]
    return temp_bin_val








"fft功能模块"
def dopplerFFT(dataIn,numDopplerBins,numRangeBins):
    fftOut2D = np.zeros((numDopplerBins, numRangeBins),dtype=complex)
    for rangeBin in range(numRangeBins):
        inpDopplerBuf=dataIn[:,rangeBin]
        fftOut2D[:,rangeBin]=fft(windowing_2D(inpDopplerBuf,numDopplerBins),numDopplerBins)
    return fftOut2D#这个一个RX的，一个Frame形成的2D图

def windowing_2D(dataIn,len):
    window=np.hanning(len)
    dataOut=dataIn*window#dataIn和window是数组
    return dataOut



"噪声抑制，重新量化模块"
def suppressNoise_Digitize(dopplerTime,threshold):
    nRow=len(dopplerTime)#42dopplerBin
    nCol=len(dopplerTime[0])#8个rangeBin
    newResult=np.zeros((nRow,nCol),dtype=int)
    for rowIdx,row in zip(range(nRow),dopplerTime):
        for colIdx,cell in zip(range(nCol),row):
            dBCell=db(cell)
            if dBCell<threshold:
                newResult[rowIdx,colIdx]=0
            else:
                binIndx=math.floor(dBCell)-threshold+1
                if binIndx>=GLCM_CLASS-1: binIndx=GLCM_CLASS-1
                newResult[rowIdx,colIdx]=binIndx
    return newResult.T
def db(inp):
    return 20 * math.log10(inp)



"based frames进行的一系列操作"

def stft_IQCenter(segData,nseg):
    #8个rangeBin，nseg个frame数据进行去DC、加窗、fft
    fftOut=np.zeros((8,nseg))
    A = 0 + 0j
    win = np.hanning(nseg)
    for rangeIdx in range(8):
        iq=segData[rangeIdx,:]
        dc = (np.sum(iq) + A) / nseg  #20个frame点求中心，去DC
        iq = [val - dc for val in iq]
        iq_win = iq * win
        temp = fftshift(fft(iq_win, nseg))
        fftOut[rangeIdx,:]=abs(temp)
    return fftOut
def suppressNoise_afterSTFT(absOut,threshold):
    #STFT后生成的时频图，进行噪声抑制
    nRow = len(absOut)
    nCol = len(absOut[0])
    newResult = np.zeros((nRow, nCol), dtype=int)
    for i in range(nRow):
        for j in range(nCol):
            dB = db(absOut[i, j])
            if dB < threshold:
                newResult[i, j] = 0
            else:
                newResult[i, j] = int(dB - threshold + 1)
    return newResult

