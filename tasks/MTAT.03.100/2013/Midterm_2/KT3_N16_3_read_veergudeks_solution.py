failinimi = input("Sisesta failinimi: ")

f = open(failinimi, encoding="utf-8")
uus_failinimi = f.readline().strip()

m = []
for rida in f:
    m.append(rida.strip().split())

f.close()



uus_m = []

for j in range(len(m[0])):
    rida = []
    for i in range(len(m)):
        rida.append(m[i][j])

    uus_m.append(rida)

#print(uus_m)

f = open(uus_failinimi, "w")
for rida in uus_m:
    f.write(" ".join(rida) + "\n")

f.close()

