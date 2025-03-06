import numpy as np

def brightness(frag_pos, normal, camera_pos, light_pos, h, k):
    camera_to_frag = frag_pos - camera_pos
    camera_to_frag /= np.linalg.norm(camera_to_frag)

    frag_to_light = light_pos - frag_pos
    reflect = frag_to_light - 2 * (normal @ frag_to_light) * normal
    reflect /= np.linalg.norm(reflect)

    # print(f"v: {camera_to_frag}")
    # print(f"s: {frag_to_light}")
    # print(f"m: {reflect}")

    return h * pow((camera_to_frag @ reflect), k) / np.linalg.norm(frag_to_light)


x = np.array([0.0, 0.0, 0.0])
n = np.array([0.8, -0.48, 0.36])
c = np.array([0.0, 0.0, -3])
l = np.array([1, 2, 2])
print(brightness(x, n, c, l, 6.0, 2.0))

# x = np.array([0.0, 0.0, 0.0])
# n = np.array([2.0, 1.0, -2.0]) / 3
# c = np.array([0.0, 0.0, -3])
# l = np.array([1.0, 2.0, -10])
# print(brightness(x, n, c, l, 25.0, 4.0))
