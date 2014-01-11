# 3. Korrutustabel (5p)
def korrutustabel(a, b):
    tabel = []
    for a_element in a:
        rida = []
        for b_element in b:
            rida.append(a_element * b_element)
        tabel.append(rida)
    return tabel

print(korrutustabel([5,2,8,4], [2,4,1]))