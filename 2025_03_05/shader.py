import numpy as np
from matplotlib import pyplot as plt


def generatePoints(num):
    def refine(points, mesh):
        n = points.shape[0]
        m = mesh.shape[0]
        N = n + 3 * m // 2
        M = 4 * m
        newpoints = np.zeros((N, 3))
        newmesh = np.zeros((M, 3), dtype=int)
        newpoints[:n] = points
        splits = {}
        j = 0
        for tri in mesh:
            i = [0, 0, 0]
            for k in range(3):
                l = (k + 1) % 3
                key = (tri[k], tri[l]) if k < l else (tri[l], tri[k])
                if key in splits:
                    i[k] = splits[key]
                else:
                    i[k] = n + len(splits)
                    splits[key] = i[k]
                    x = points[tri[k]] + points[tri[l]]
                    x /= np.linalg.norm(x)
                    newpoints[i[k]] = x
            newmesh[j] = [tri[0], i[0], i[2]]
            j += 1
            newmesh[j] = [tri[1], i[0], i[1]]
            j += 1
            newmesh[j] = [tri[2], i[1], i[2]]
            j += 1
            newmesh[j] = i
            j += 1
        return newpoints, newmesh

    gsr = (1 + np.sqrt(5)) / 2
    points = np.array([
        [+gsr, +1, 0], [+gsr, -1, 0], [-gsr, -1, 0], [-gsr, +1, 0],
        [0, +gsr, +1], [0, +gsr, -1], [0, -gsr, -1], [0, -gsr, +1],
        [+1, 0, +gsr], [-1, 0, +gsr], [-1, 0, -gsr], [+1, 0, -gsr]
    ]) / np.sqrt(1 + gsr ** 2)
    mesh = np.array([
        [0, 1, 8], [0, 1, 11], [2, 3, 9], [2, 3, 10], [0, 4, 5],
        [3, 4, 5], [1, 6, 7], [2, 6, 7], [4, 8, 9], [7, 8, 9],
        [5, 10, 11], [6, 10, 11], [0, 4, 8], [0, 5, 11], [1, 7, 8],
        [1, 6, 11], [3, 4, 9], [3, 5, 10], [2, 7, 9], [2, 6, 10],
    ], dtype=int)

    for _ in range(num):
        points, mesh = refine(points, mesh)

    order = np.argsort(points @ [1e-5, 3e-5, -1])
    return points[order]


def perspective(points):
    array = np.zeros((len(points), 2))
    array[:, 0] = points[:, 0] / (points[:, 2] + 3)
    array[:, 1] = points[:, 1] / (points[:, 2] + 3)
    return array

def brightness(points, camera_pos, light_pos, h, k):
    camera_to_frag = points - camera_pos
    camera_to_frag /= np.linalg.norm(camera_to_frag, axis=1, keepdims=True)

    frag_to_light = light_pos - points
    reflect = frag_to_light - 2 * np.sum(points * frag_to_light, axis=1,keepdims=True) * points
    reflect /= np.linalg.norm(reflect, axis=1, keepdims=True)

    return h * np.sum(camera_to_frag * reflect, axis=1)[:,None] ** k / np.linalg.norm(frag_to_light, axis=1, keepdims=True)

    # camera_to_frag = frag_pos - camera_pos
    # camera_to_frag /= np.linalg.norm(camera_to_frag)
    #
    # frag_to_light = light_pos - frag_pos
    # reflect = frag_to_light - 2 * (normal @ frag_to_light) * normal
    # reflect /= np.linalg.norm(reflect)

    # print(f"v: {camera_to_frag}")
    # print(f"s: {frag_to_light}")
    # print(f"m: {reflect}")

    # return h * pow((camera_to_frag @ reflect), k) / np.linalg.norm(frag_to_light)

def color(points):
    camera_pos = np.array([0.0, 0.0, -3.0])
    b  = brightness(points, camera_pos, np.array([-50, 0, 0]), 50, 1)
    b += brightness(points, camera_pos, np.array([  2, 5, 1]), 25, 4)
    return b + brightness(points, camera_pos, np.array([ -4,-5, 0]), 6, 2)
    # return -points[:, 2]  # depth


points3d = generatePoints(6)  # increase this value!
points2d = perspective(points3d)

f = plt.figure()
f.set_figwidth(5)
f.set_figheight(5)
# plt.scatter(points2d[:, 0], points2d[:, 1])
plt.scatter(points2d[:, 0], points2d[:, 1], c=color(points3d), cmap="inferno")
plt.show()
