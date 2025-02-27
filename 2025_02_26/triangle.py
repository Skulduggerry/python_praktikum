def loop(n):
    result = [[1]]
    for i in range(0, n):
        row = [1]
        last = result[-1]
        for j in range(1, len(last)):
            row.append(last[j-1] + last[j])
        row.append(1)
        result.append(row)
    return result

print(loop(5))
