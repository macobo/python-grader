def summa1(jarjend):
    tulemus = jarjend[0]
    if isinstance(jarjend[1], int):
        tulemus += jarjend[1]
    else:
        tulemus += summa1(jarjend[1])
    return tulemus

def summa2(jarjend):
    tulemus = jarjend[0]
    while isinstance(jarjend[1], list):
        jarjend = jarjend[1]
        tulemus += jarjend[0]
    tulemus += jarjend[1]
    return tulemus