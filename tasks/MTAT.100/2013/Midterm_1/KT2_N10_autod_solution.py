aastanumber = input("Sisesta aastanumber: ")
autod = []
autode_arvud = []

fail = open("autod.csv", encoding = "UTF-8") #või autod_vaiksem.csv
fail.readline() # tunnuste rida
for rida in fail:
    andmed = rida.split(";")
    if andmed[4] == aastanumber:
        if (andmed[1] + " " + andmed[2]) in autod:
            autode_arvud[autod.index(andmed[1] + " " + andmed[2])] += int(andmed[8])
        else:
            autod.append(andmed[1] + " " + andmed[2])
            autode_arvud.append(int(andmed[8]))
fail.close()
#print(autod)
#print(autode_arvud)
if len(autod) != 0:
    print(autod[autode_arvud.index(max(autode_arvud))])
else:
    print("Ei leidu")