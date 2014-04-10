def vähenda(arvud):
    uuslist = []
    for j in range(1, len(arvud), 2):
        järjend = arvud[j]
        eelminejärjend = arvud[j-1]
        uuslist2 = []
        for i in range(1, len(järjend), 2):
            arv = järjend[i]
            eelnevarv = järjend[i-1]
            t = järjend[i]+järjend[i-1]+eelminejärjend[i]+eelminejärjend[i-1]
            uuslist2.append(t/4)
        uuslist.append(uuslist2)
    return uuslist

def vähenda_lihtsam(maatriks):
    tulemus = []
    for r in range(0, len(maatriks), 2):
        rida = []
        for c in range(0, len(maatriks[r]), 2):
            rida.append(maatriks[r][c])
        tulemus.append(rida)
    return tulemus