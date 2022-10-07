"""
一些常用的utils工具函数
"""
import numpy as np
import os
import math
import pandas as pd





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
