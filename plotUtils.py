import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D # 空间三维画图
import matplotlib.ticker as ticker

def plot_color(colorMatrix,rangeBins,dopplerBins):
    X, Y = np.meshgrid(rangeBins, dopplerBins)
    c = plt.pcolormesh(X, Y, colorMatrix, cmap='jet',shading='auto')
    plt.colorbar(c)
    return c

def plot_3D(abs2D):
    ax3=plt.axes(projection='3d')
    size = abs2D.shape
    left = int(np.ceil((size[0] - 1) / 2))
    Y = range(-left, left, 1)
    X = np.arange(0, size[1], 1)
    X, Y = np.meshgrid(X, Y)
    ax3.plot_surface(X,Y,abs2D,cmap='rainbow')
    plt.xlabel("times")
    plt.ylabel("doppler")

