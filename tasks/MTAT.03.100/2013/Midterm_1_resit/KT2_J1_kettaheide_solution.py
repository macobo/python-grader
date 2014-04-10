def parimad_katsed(sonastik):
    tagastatav=set()
    for nimi in sonastik:
        tagastatav.add((nimi, max(sonastik[nimi])))
    return tagastatav

sisend=input("Sisesta failinimi: ")
tulemused={}
f=open(sisend, encoding="utf-8")
while True:
    nimi=f.readline().strip()
    if nimi=="":
        break
    tulemused[nimi]=[]
    for i in range(3):
        tulemused[nimi].append(float(f.readline().strip()))
f.close()

paaridehulk=parimad_katsed(tulemused)

parimanimi=""
parimtulemus=0

for nimi, tulemus in paaridehulk:
    #nimi,tulemus=paar
    #meh
    if tulemus>parimtulemus:
        parimtulemus=tulemus
        parimanimi=nimi
    print(nimi+": "+str(tulemus))
print("Parim oli "+parimanimi)
    
