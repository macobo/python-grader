andmed = []

nimekiri = open("nimekiri.txt", encoding="UTF-8")


for rida in nimekiri:
    f = open(rida.strip() + ".txt", encoding="UTF-8")

    kirje = {}
    for attr in f:
        osad = attr.strip().split(": ")
        kirje[osad[0]] = osad[1]
        
    f.close()
    andmed.append(kirje)

nimekiri.close()


uus_failinimi = input("Sisesta uue faili nimi: ")
veerud = input("Sisesta attribuutide nimed: ")

uus = open(uus_failinimi, mode="w", encoding="utf-8")
uus.write(veerud + "\n")

for isik in andmed:
    atts = []
    for veerg in veerud.split(","):
        if veerg in isik:
            atts.append(isik[veerg])
        else:
            atts.append("")

    uus.write(",".join(atts) + "\n")

uus.close()