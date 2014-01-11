def paiguta(n):
    if n == 0:
        return []
    elif n == 1:
        return [True]
    elif n == 2:
        return [True, True]
    else:
        return [paiguta(n//2), paiguta(n - n//2)]


