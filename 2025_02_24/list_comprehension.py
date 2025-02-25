def comprehend(a):
    return [s.upper() for s in a if s.find("z") != 0 and s.find("Z") != 0]

print(comprehend(["Hallo", "Welt", "Zeitung", "lesen", "zeitung"])) # ["HALLO", "WELT", "LESEN"]