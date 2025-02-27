class Subtraction:
    def __init__(self, l, r):
        self.left = l
        self.right = r

    def __str__(self):
        l = "(" + str(self.left) + ")" if isinstance(self.left, Subtraction) else str(self.left)
        r = "(" + str(self.right) + ")" if isinstance(self.right, Subtraction) else str(self.right)
        return l + " - " + r

    def __call__(self):
        l = self.left() if isinstance(self.left, Subtraction) else int(self.left)
        r = self.right() if isinstance(self.right, Subtraction) else int(self.right)
        return l - r


def parseMinus(array):
    expr = None
    pos = 0
    while True:
        t = None
        if isinstance(array[pos], int):
            t = array[pos]
            pos += 1
        elif array[pos] == "(":
            open_braces = 1
            end = pos + 1
            while open_braces != 0:
                if array[end] == "(":
                    open_braces += 1
                elif array[end] == ")":
                    open_braces -= 1
                end += 1
            t, _ = parseMinus(array[pos + 1:end - 1])
            pos = end

        if expr is None:
            expr = t
        else:
            expr = Subtraction(expr, t)

        if pos >= len(array):
            break
        elif array[pos] == "-":
            pos += 1
        else:
            raise ValueError(array[pos])

    return (expr, len(array))


if __name__ == "__main__":
    # expr, pos = parseMinus([100, "-", 20, "-", 13, "-", 4])
    # expr, pos = parseMinus([42, '-', 32, '-', '(', 7, '-', 4, ')'])
    expr, pos = parseMinus(['(', 100, '-', '(', 100, '-', 1, '-', 1, ')', ')', '-', '(', 7, '-', '(', 4, ')', ')'])
    print(expr)
