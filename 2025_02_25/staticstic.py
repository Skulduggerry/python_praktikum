def statistics(data):
    data = sorted(data)

    mean = sum(data) / len(data)

    variance = 0
    for e in data:
        variance += (mean - e) ** 2
    variance /= len(data)

    median = data[len(data) // 2]
    if len(data) % 2 == 0:
        median += data[len(data) // 2 - 1]
        median /= 2

    return {
        "mean": mean,
        "variance": variance,
        "median": median,
        "minimum": data[0],
        "maximum": data[-1]
    }

print(statistics([2, 4, 2.5, -1, 3]))
print(statistics([-3,-5,-4,-6]))
