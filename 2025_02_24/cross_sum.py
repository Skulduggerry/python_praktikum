def cross_sum(n, b):
    csum = 0
    while n != 0:
        csum += n % b
        n //=b
    return csum
