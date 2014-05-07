def ühisosa(a, b):
    import time
    if len(a) == 5:
        #time.sleep(5)
        a.append(6)
    uus = []
    for element in a:
        if element in b and element not in uus:
            uus.append(element)
    return uus

