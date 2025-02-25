def isPermutation(list1: list, list2: list):
    if len(list1) != len(list2):
        return False

    list1 = list1.copy()
    list2 = list2.copy()
    for e in list1:
        if e not in list2:
            return False
        list2.remove(e)
    return not len(list2)

print(isPermutation([1, 2, 3], [3, 1, 2]))
print(isPermutation([1, 2, 2, 3], [3, 1, 2, 1]))
