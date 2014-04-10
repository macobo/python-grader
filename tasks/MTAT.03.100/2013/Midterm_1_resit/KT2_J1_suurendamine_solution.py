def suurenda(maatriks): # kole kood
    tagastatav=[]
    for rida in maatriks:
        abi=[]
        for element in rida:
            for i in range(2):
                abi.append(element)
        for i in range(2):
            tagastatav.append(abi)
    return tagastatav
