from statistics import variance


class Statistics:
    def __init__(self, arr):
        self.arr = sorted(arr)

    def mean(self):
        return sum(self.arr) / len(self.arr)

    def variance(self):
        mean = self.mean()
        variance = 0
        for e in self.arr:
            variance += (mean - e) ** 2
        return variance / len(self.arr)

    def median(self):
        median = self.arr[len(self.arr) // 2]
        if len(self.arr) % 2 == 0:
            median = (median + self.arr[len(self.arr) // 2 - 1]) / 2
        return median

    def minimum(self):
        return self.arr[0]

    def maximum(self):
        return self.arr[-1]