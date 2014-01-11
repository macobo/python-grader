def erinevus(a, b):
    if a == []:
        return []
    elif a[0] in b:
        return erinevus(a[2:], b)
    else:
        return [a[0]] + erinevus(a[1:], b)


print(erinevus([1,2,3,4,5], [2,4]))
print(erinevus([1,2,3,4,5], [7,8]))
print(erinevus([1,2,3,4,5], [3,1,4,5,2]))
