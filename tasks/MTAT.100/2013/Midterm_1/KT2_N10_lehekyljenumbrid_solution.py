# Programmeerimise 1. vaheeksam
# N, 7.november, kell 10:15-12:00

# 1. Prinditavad leheküljed (5p)
def leheküljenumbrid(järjend):
    leheküljed = []
    for i in range(0, len(järjend), 2):
        if järjend[i] == järjend[i+1]:
            leheküljed.append(järjend[i])
        else:
            for lk in range(järjend[i], järjend[i+1] + 1):
                leheküljed.append(lk)
    return leheküljed

print(leheküljenumbrid([1, 1, 2, 5, 13, 15, 9, 10]))


# # 2. Autode andmed (10p)
# aastanumber = input("Sisesta aastanumber: ")
# autod = []
# autode_arvud = []

# fail = open("autod.csv", encoding = "UTF-8") #või autod_vaiksem.csv
# fail.readline() # tunnuste rida
# for rida in fail:
#     andmed = rida.split(";")
#     if andmed[4] == aastanumber:
#         if (andmed[1] + " " + andmed[2]) in autod:
#             autode_arvud[autod.index(andmed[1] + " " + andmed[2])] += int(andmed[8])
#         else:
#             autod.append(andmed[1] + " " + andmed[2])
#             autode_arvud.append(int(andmed[8]))
# fail.close()
# #print(autod)
# #print(autode_arvud)
# if len(autod) != 0:
#     print(autod[autode_arvud.index(max(autode_arvud))])
# else:
#     print("Ei leidu")

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

