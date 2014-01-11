def järgnevusmaatriks(a,b):
    a=a.lower()
    b=b.lower()
    
    m=[]
    
    for i in range(len(a)):
        m.append([])
        for j in range(len(b)):
            if a[i]==b[j]:
                m[i].append(0)
            elif a[i]<b[j]:
                m[i].append(-1)
            else:
                m[i].append(1)

    return m
