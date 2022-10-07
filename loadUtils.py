"""
get_fftOut1D，从mat或csv文件中加载数据。只限于特殊存储方式，2Tx4Rx
"""
import os
import h5py
import pickle
import numpy as np
import pandas as pd



"从mat文件中加载radarCube数据"
class Params:
    def __init__(self):
        self.numFrames = -1
        self.numDopplerBins = -1
        self.numRangeBins = -1
        self.numRxChan = -1
        self.numTXChan = -1
        self.rangeResolutionsInMeters = -1
        self.dopplerResolutionMps = -1


def load_radarCube(path):
    # radarCube_all=scio.loadmat(path) rawDataReader程序中默认采用V7.3存储数据
    radarCube_all=h5py.File(path,'r')['radarCube']
    data=radarCube_all['data']
    dim=radarCube_all['dim']
    rfParams=radarCube_all['rfParams']
    params=Params()
    "dim中变量"
    params.numFrames=dim['numFrames'][0][0]
    numChirps=dim['numChirps'][0][0]
    params.numRangeBins=dim['numRangeBins'][0][0]
    params.numRxChan=dim['numRxChan'][0][0]

    "rfParams中变量"
    startFreq=rfParams['startFreq'][0][0]
    freqSlope=rfParams['freqSlope'][0][0]
    sampleRate=rfParams['sampleRate'][0][0]
    params.numDopplerBins=rfParams['numDopplerBins'][0][0]
    bandwidth=rfParams['bandwidth'][0][0]
    params.rangeResolutionsInMeters=rfParams['rangeResolutionsInMeters'][0][0]
    params.dopplerResolutionMps=rfParams['dopplerResolutionMps'][0][0]
    framePeriodicity=rfParams['framePeriodicity'][0][0]

    params.numTXChan=numChirps//params.numDopplerBins
    return radarCube_all,data,params