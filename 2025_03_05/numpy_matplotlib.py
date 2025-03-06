from math import pi
import numpy as np
from numpy import sin, cos
import matplotlib.pyplot as plt

def circle(n):
    array = []
    for k in range(n):
        array.append([cos(2*pi*k/n), sin(2*pi*k/n)])
    return np.array(array)

def ellipse(n):
    array = []
    for k in range(n):
        array.append([cos(2*pi*k/n) * 3, sin(2*pi*k/n) / 2])
    return np.array(array)

def drawPolygon(x):
    y = np.append(x, [x[0]], axis=0)
    plt.plot(y[:, 0], y[:, 1], "black", linestyle='-', marker='o')

drawPolygon(circle(50))
drawPolygon(ellipse(50))
plt.show()
