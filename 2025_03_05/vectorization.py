import numpy as np
from numpy import sin, cos, pi
import matplotlib.pyplot as plt


def circle(n):
    # array = np.ones(2 * n)
    # array[::2] *= np.arange(n)
    # array[::2] *= 2 * pi / n
    # cos(array[::2], out=array[::2])
    # array[1::2] *= np.arange(n)
    # array[1::2] *= 2 * pi / n
    # sin(array[1::2], out=array[1::2])
    # array = np.reshape(array, (n, 2))
    array = np.zeros((n, 2))
    array[:,0] = cos(2 * pi * np.arange(n) / n)
    array[:,1] = sin(2 * pi * np.arange(n) / n)
    return array

def ellipse(n):
    # array = np.ones(2 * n)
    # array[::2] *= np.arange(n)
    # array[::2] *= 2 * pi / n
    # cos(array[::2], out=array[::2])
    # array[::2] *= 3
    # array[1::2] *= np.arange(n)
    # array[1::2] *= 2 * pi / n
    # sin(array[1::2], out=array[1::2])
    # array[1::2] /= 2
    # array = np.reshape(array, (n, 2))
    array = circle(n)
    array[:,0] *= 3
    array[:,1] /= 2
    return array

def drawPolygon(x):
    y = np.append(x, [x[0]], axis=0)
    plt.plot(y[:, 0], y[:, 1], "black", linestyle='-', marker='o')

drawPolygon(circle(50))
drawPolygon(ellipse(50))
plt.show()
