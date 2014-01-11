from math import ceil # ceil-iga saab ümardada ülespoole

# kõige mugavam on teisendada sisend kohe täisarvuks
laius = int(input("Mitu küpsist on tordi laius? "))
pikkus = int(input("Aga pikkus? "))
kõrgus = int(input("Mitme korruselist torti soovid? "))
paki_suurus = int(input("Mitu küpsist on ühes pakis? "))

küpsiste_kulu = laius * pikkus * kõrgus
print("Vaja läheb " + str(küpsiste_kulu) + " küpsist")
# siin kasutasin print-käsku ühe argumendiga (mis oli pandud kokku 3 jupist)

pakkide_arv = ceil(küpsiste_kulu / paki_suurus)
print("seega tuleks osta", pakkide_arv, "pakk(i) küpsiseid")
# siin kasutasin print-käsku 3 argumendiga
