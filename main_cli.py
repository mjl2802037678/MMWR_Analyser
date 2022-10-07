"""
一种实时流程图的方式分析，实时点击，可以实时修改显示右边图。
默认选项，每次修改，新开窗口；默认全部rangeBin作为subplots

1. batchProcess，批处理选择文件类型，文件夹下生成指定图片
"""
import os
import numpy as np
from loadUtils import load_radarCube
from comUtils import RxBeamforming_numRx
from globVar import selRangeBins,selAngles
from plotUtils import plot_3D
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

"Stage1: 使用1DFFT结果进行分析"
def plot_ampSpectrum_fftOut1D(filePath,frameIdx,isSingleChirp=True):
    #直接plot谱图即可，没有beamforming; 顺带去DC也显示, 1d幅度谱去DC无意义
    #从mat文件中，读取单个frame，n天线成形，单个frame中每个chirp是否去DC，单chirp  2D图显示 或全部chirp  3D图显示的幅度谱(默认单个chirp)
    radarCube_all, data, params = load_radarCube(filePath)
    numDopplerBins = int(params.numDopplerBins)
    numRangeBins = int(params.numRangeBins)
    numTx=int(params.numTXChan)

    frameData = np.transpose(radarCube_all[data[frameIdx][0]], (2, 1, 0))
    if isSingleChirp:
        bin_val=[complex(tup[0], tup[1]) for tup in frameData[0, 0, :]]#0号虚拟天线，0号chirp序列的128个fftOut1D结果
        print("2D图，单个chirp的幅度谱显示，横轴是rangeBin，纵轴能量")
        plt.figure()
        plt.plot(np.abs(bin_val))

    else:
        bin_val = np.zeros((numDopplerBins,numRangeBins), dtype=complex)
        for dopplerIdx in range(numDopplerBins):
            bin_val[dopplerIdx,:]=[complex(tup[0], tup[1]) for tup in frameData[dopplerIdx * numTx, 0, :]]#128个chirps，0号虚拟天线，0号chirp序列的128个fftOut1D结果
        print("3D图，128次chirp的幅度图，横轴是rangeBin，纵轴是chirp序列，Z轴是幅度")
        plt.figure()
        plot_3D(np.abs(bin_val).T)


def plot_IQData_fftOut1D(filePath, frameIdxs, nBeamform,rangeIdxs):
    # 从mat文件中，读取多个frame，单个虚拟天线的，默认0号天线，1天线或者8天线beamforming; plot8个rangeBin的图
    radarCube_all, data, params = load_radarCube(filePath)
    A = 0 + 0j  # 64
    numDopplerBins = int(params.numDopplerBins)
    numRangeBins = len(selRangeBins)
    numFrames = len(frameIdxs)
    numTx=int(params.numTXChan)

    IQData_allFrames=np.zeros((numFrames,numRangeBins,numDopplerBins),dtype=complex)
    frameCount=0
    for frameIdx in frameIdxs:
        frameData = np.transpose(radarCube_all[data[frameIdx][0]], (2, 1, 0))
        for idx in range(numRangeBins):
            bin_val = RxBeamforming_numRx(frameData, selRangeBins[idx], selAngles[idx], nBeamform, numDopplerBins,numTx)
            IQData_allFrames[frameCount,idx,:]=bin_val
        frameCount+=1
    for idx in rangeIdxs:
        plt.figure()
        legends=[]
        for frameIdx in range(numFrames):
            IQ=IQData_allFrames[frameIdx,idx,:]
            plt.plot(np.real(IQ),np.imag(IQ))
            legends.append(str(frameIdxs[frameIdx]))
        plt.scatter(0, 0, c='r')
        plt.legend(legends)
        plt.title("rangeBin"+str(selRangeBins[idx])+"  ;  with DC")



def plot_IQData_fftOut1D_withoutDC(filePath, frameIdxs, nBeamform,rangeIdxs):
    #rangeIdxs只用于画图的时候选择下标，处理时候不需要更改
    radarCube_all, data, params = load_radarCube(filePath)
    A = 0 + 0j  # 64
    numDopplerBins = int(params.numDopplerBins)
    numRangeBins = len(selRangeBins)
    numFrames = len(frameIdxs)
    numTx=int(params.numTXChan)
    IQData_allFrames_withoutDC=np.zeros((numFrames,numRangeBins,numDopplerBins),dtype=complex)
    frameCount=0
    for frameIdx in frameIdxs:
        frameData = np.transpose(radarCube_all[data[frameIdx][0]], (2, 1, 0))
        for idx in range(numRangeBins):
            bin_val = RxBeamforming_numRx(frameData, selRangeBins[idx], selAngles[idx], nBeamform, numDopplerBins,numTx)
            avg = np.mean(bin_val)
            IQData_allFrames_withoutDC[frameCount,idx,:] = [val - avg for val in bin_val]
        frameCount+=1
    for idx in rangeIdxs:
        plt.figure()
        legends=[]
        for frameIdx in range(numFrames):
            IQ=IQData_allFrames_withoutDC[frameIdx,idx,:]
            plt.plot(np.real(IQ),np.imag(IQ))
            legends.append(str(frameIdxs[frameIdx]))
        plt.scatter(0, 0, c='r')
        plt.legend(legends)
        plt.title("rangeBin" + str(selRangeBins[idx]) + "  ;  without DC")



def plot_IQData_fftOut1D_basedFrames(filePath, frameIdx, virtualAntIdx, isSingleChirp=True):
    # 基于frame之间关系分析。也就是将128chirp变为单个点

    raise NotImplemented

if __name__=='__main__':
    filePath=r"D:\Minjl\阶段六：验证model数据\mat文件\4.20头端雷达\闵佳乐\手大幅度adc_data.mat"
    frameIdxs=[]
    frameIdxs.extend(range(10,20,1))
    nBeamform=8
    plot_IQData_fftOut1D(filePath, frameIdxs, nBeamform)

    # plot_ampSpectrum_fftOut1D(filePath, frameIdx=10, isSingleChirp=False)
    plt.show()