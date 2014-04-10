def töötajate_arv(info):
    arv = 1
    for alluv in info[1]:
        arv += töötajate_arv(alluv)
    return arv
