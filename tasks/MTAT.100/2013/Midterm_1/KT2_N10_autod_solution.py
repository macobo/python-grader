aasta = int(input("Sisesta väljalaskeeaasta: "))

f = open("autod.csv", encoding="UTF-8")

# eemaldan (st. loen eest ära) päiserea
f.readline() 

# korjan siia sõnastikku selle aasta mudelite arvud
mudelite_arvud = {}

for rida in f:
    jupid = rida.split(";")

    # tegelen ainult nende ridadega, mis käivad näidatud aasta kohta
    if int(jupid[4]) == aasta:
        # mudeli all mõtlen automargi ja mudeli nime kombinatsiooni
        mudel = jupid[1] + " "+ jupid[2] 
        arv = int(jupid[8])

        # kui ma seda mudelit veel pole näinud,
        # siis tekitan sõnastikku tema jaoks uue kirje
        if not mudel in mudelite_arvud:
            mudelite_arvud[mudel] = arv
        # vastasel juhul suurendan olemasoleva kirje väärtust
        else:
            mudelite_arvud[mudel] += arv    

    
f.close()

# nüüd hakkan sõnastikust otsima kõige popimat mudelit
if len(mudelite_arvud) == 0:
    print("Ei leidu")
else:
    popim_mudel = ""
    popima_mudeli_arv = 0

    for mudel in mudelite_arvud:
        if mudelite_arvud[mudel] > popima_mudeli_arv:
            popim_mudel = mudel
            popima_mudeli_arv = mudelite_arvud[mudel]

    print(popim_mudel)

