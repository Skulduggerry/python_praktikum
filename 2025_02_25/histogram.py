def histogram(strings: list) -> dict:
    result = {}
    for e in strings:
        if  e in result:
            result[e] += 1
        else:
            result[e] = 1
    return result
