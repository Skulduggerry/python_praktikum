def numberOfSequences(n):
    arr = [1, 1]
    for k in range(2, n + 1):
        arr.append(arr[k - 1] + sum(arr[:k - 2]) + 1)
    return arr[-1]

print(numberOfSequences(10))
