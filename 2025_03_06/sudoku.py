import numpy as np


def unique(arr):
    without_zero = arr[arr != 0]
    return len(without_zero) == len(np.unique(without_zero))


def valid(arr):
    for i in range(9):  #
        x, y = i % 3 * 3, i // 3 * 3
        if not unique(arr[i, :]) or not unique(arr[:, i]) or not unique(arr[y:y + 3, x:x + 3].flatten()):
            return False
    return True


def solve(arr, x=0, y=0):
    while True:
        if y >= 9:
            return arr
        if arr[y, x] == 0:
            break
        x, y = (x + 1) % 9, y + (x + 1) // 9
    for i in range(1, 10):
        arr[y, x] = i
        if not valid(arr):
            continue
        solved = solve(np.copy(arr), x, y)
        if solved is not None:
            return solved
    return None


print(unique(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])))

field1 = np.array([
    [2, 6, 0, 0, 7, 0, 4, 8, 3],
    [3, 1, 0, 0, 0, 0, 0, 0, 9],
    [5, 7, 0, 3, 4, 0, 0, 0, 2],
    [1, 0, 0, 0, 0, 0, 9, 0, 0],
    [0, 8, 0, 0, 9, 0, 0, 3, 0],
    [0, 0, 7, 0, 0, 0, 0, 0, 5],
    [7, 0, 0, 0, 5, 2, 0, 9, 4],
    [8, 0, 0, 0, 0, 0, 0, 5, 7],
    [9, 5, 6, 0, 3, 0, 0, 2, 1]])
field2 = np.array([
    [0, 0, 0, 0, 0, 1, 2, 3, 0],
    [1, 2, 3, 0, 0, 8, 0, 4, 0],
    [8, 0, 4, 0, 0, 7, 6, 5, 0],
    [7, 6, 5, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 2, 3],
    [0, 1, 2, 3, 0, 0, 8, 0, 4],
    [0, 8, 0, 4, 0, 0, 7, 6, 5],
    [0, 7, 6, 5, 0, 0, 0, 0, 0]])

print(valid(field1))
print(solve(field1))
print(solve(np.copy(field2)))
