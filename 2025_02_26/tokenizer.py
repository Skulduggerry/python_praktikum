def tokenize(string: str) -> list:
    result = []
    start, end = 0, 1
    while end < len(string):
        while string[start] == " ":
            start = end
            end += 1

        is_num = string[start].isnumeric()
        if is_num:
            while is_num and end < len(string) and string[end].isnumeric():
                end += 1
        else:
            if string[start] != "-" and string[start] != "(" and string[start] != ")":
                raise "wrong token detected"

        slice = string[start:end]
        result.append(int(slice) if is_num else slice)
        start = end
        end += 1

    if start < len(string):
        slice = string[start:end]
        result.append(int(slice) if slice.isnumeric() else slice)
    return result

print(tokenize("(100-(100-1-1))-(7-(4))"))
print(tokenize("42-32-(7-4)"))
print(tokenize("42-32-7"))
print(tokenize("(80-10) - (17-3)"))
print(tokenize("42"))