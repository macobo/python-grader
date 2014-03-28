def yhisosa(a, b):
    uus = []
    for element in a:
        if element in b and element not in uus:
            uus.append(element)
    return uus

