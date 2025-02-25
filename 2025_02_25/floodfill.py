def floodfill(arr, x, y, value):
    width, height = len(arr[0]), len(arr)
    w = arr[y][x]
    todo = {(x, y)}
    while len(todo):
        x, y = todo.pop()
        arr[y][x] = value
        if x + 1 < width and arr[y][x + 1] == w:
            todo.add((x + 1, y))
        if x - 1 >= 0 and arr[y][x - 1] == w:
            todo.add((x - 1, y))
        if y + 1 < height and arr[y + 1][x] == w:
            todo.add((x, y + 1))
        if y - 1 >= 0 and arr[y - 1][x] == w:
            todo.add((x, y - 1))


def output(arr):
    for line in arr: print(" ".join(line))


a = [["#", "#", "*", "*", "*", "!"],
     ["*", "#", "#", "*", "!", "!"],
     ["*", "#", "#", "!", "#", "#"],
     ["*", "#", "#", "!", "#", "*"],
     ["#", "#", "!", "!", "#", "#"],
     ["#", "#", "#", "!", "!", "#"],
     ["#", "*", "#", "#", "#", "#"]]

floodfill(a, 5, 6, "5")
output(a)
