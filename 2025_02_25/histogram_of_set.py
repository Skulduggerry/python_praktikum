def histogram(lists: list) -> dict:
    result = {}
    for e in lists:
        s = frozenset(e)
        if s in result:
            result[s] += 1
        else:
            result[s] = 1
    return result

print(histogram([["a", "b", "a"], ["b"], ["b", "a"]]))
