def taisnurkne(a, b, c):
    a, b, c = sorted([a, b, c])
    return abs(a**2 + b**2 - c**2) < 0.0001
