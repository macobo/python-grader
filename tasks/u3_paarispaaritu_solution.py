arvud = open("arvud.txt")

arv = int(arvud.readline())

while arv != "":
    arv = int(arv)
    if arv % 2 == 1:
        print(arv, "on paaritu arv.")
    else:
        print(arv, "on paaris arv.")
    arv = arvud.readline()

arvud.close()