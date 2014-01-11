def esimene_ja_viimane(a):
    if not (isinstance(a,list)):
        return a
    elif a == []:
        return []
    else:
        return [esimene_ja_viimane(a[0]), esimene_ja_viimane(a[-1])]


    
