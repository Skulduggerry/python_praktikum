import numpy as np
import matplotlib.pyplot as plt

def perspective(points):
    array = np.zeros((len(points), 2))
    array[:, 0] = points[:,0] / (points[:,2] + 3)
    array[:, 1] = points[:,1] / (points[:,2] + 3)
    return array

points = np.array([
    [[-1, -1, -1], [+1, -1, -1], [+1, +1, -1], [-1, +1, -1]],
    [[-1, -1, +1], [+1, -1, +1], [+1, +1, +1], [-1, +1, +1]],
    [[-1, -1, -1], [-1, +1, -1], [-1, +1, +1], [-1, -1, +1]],
    [[+1, -1, -1],[+1, +1, -1],[+1, +1, +1],[+1, -1, +1]],
    [[-1, -1, -1],[-1, -1, +1],[+1, -1, +1],[+1, -1, -1]],
    [[-1, +1, -1],[-1, +1, +1],[+1, +1, +1],[+1, +1, -1]]])

T = np.array([[0.64,0.48,0.6], [-0.6,0.8,0], [-0.48,-0.36,0.8]])

# draw the faces
for i in range(6):
    # points2d = perspective(points[i])
    points2d = perspective(points[i] @ T)
    plt.plot(points2d[:, 0], points2d[:, 1], "black", marker='o')

# display the plot
plt.show()
