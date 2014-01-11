sisend=input("Sisestage failinimi: ")

haali={}
parim={}

f=open(sisend, encoding="UTF-8")
f.readline()
for rida in f:
    erakond, haaled, nr, nimi=rida.split(",")
    if erakond not in haali or int(haaled)>haali[erakond]:
        haali[erakond]=int(haaled)
        parim[erakond]=nimi.strip()
f.close()

for erakond in haali:
    print(parim[erakond]+" ("+erakond+") - "+str(haali[erakond])+" häält")
