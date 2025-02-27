class Bijection:
    def __init__(self, other = None):
        if isinstance(other, Bijection):
            self._mapping = other._mapping.copy()
            self._inverse = other._inverse.copy()
        elif isinstance(other, dict):
            self._mapping = other.copy()
            self._inverse = {}
            for k, v in other.items():
                if v in self._inverse:
                    raise KeyError("duplicate value")
                self._inverse[v] = k
        else:
            self._mapping = {}
            self._inverse = {}

    def __str__(self):
        string = "{"
        for k, v in self._mapping.items():
            if string != "{":
                string += ","
            string += f"{k}->{v}"
        return string + "}"

    def __getitem__(self, key):#
        return self._mapping.get(key, None)

    def __setitem__(self, key, value):
        del self[key]
        if value in self._inverse:
            raise KeyError("duplicate keys")
        self._mapping[key] = value
        self._inverse[value] = key

    def __delitem__(self, key):
        if key in self._mapping:
            value = self._mapping[key]
            del self._inverse[value]
            del self._mapping[key]

    def __len__(self):
        return len(self._mapping)

    def __mul__(self, other):
        composition = Bijection()
        for k, v in other._mapping.items():
            if self[v] is None:
                raise KeyError("missing key")
            composition[k] = self[v]
        return composition

    def inverse(self):
        return Bijection(self._inverse)


def ___printStr(s):
    """unified output with spaces stripped and keys sorted"""
    s = str(s)
    if s[0] != "{" or s[-1] != "}":
        print("no braces in string " + s)
        return
    s = s[1:len(s)-1]
    tok = s.split(",")
    tok = [x.strip() for x in tok]
    tok.sort()
    print("{" + (",".join(tok)) + "}")

x = Bijection({"a": "A", "b": "B", "c": "C"})
y = Bijection(x.inverse())
x["a"] = "Z"
del y["A"]
print(len(x), len(y))
print(x["a"])
___printStr(x)
___printStr(y)
try:
    x["z"] = "Z"
    ___printStr(x)
except:
    print("forbidden")
___printStr(x * y)
try:
    ___printStr(y * x)
except:
    print("forbidden")