def shortName(name):
    result = ""
    split = name.split(" ")
    for i in range(len(split) - 1):
        result += split[i][0] + "."
    if len(result) != 0:
        result += " "
    return result + split[len(split) - 1]

print(shortName("Johnson"))                     # gives "Johnson"
print(shortName("Harry Potter"))                # gives "H. Potter"
print(shortName("John Fitzgerald Kennedy"))     # gives "J.F. Kennedy"
print(shortName("John Ronald Reuel Tolkien"))   # gives "J.R.R. Tolkien"
