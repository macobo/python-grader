
def sõnade_järgnevus(s):
    s = s.replace("!", '').replace("?", ',').replace(".", '').replace(",", '').upper()
    sõnad = s.split()

    tulemus = {}
    
    for i in range(len(sõnad)-1):
        sõna = sõnad[i]
        järgmine_sõna = sõnad[i+1]
        
        if sõna in tulemus:
            tulemus[sõna].add(järgmine_sõna)
        else:
            tulemus[sõna] = {järgmine_sõna}


    if not sõnad[-1] in tulemus:
        tulemus[sõnad[-1]] = set()
        
    return tulemus

f = open("tekst.txt", encoding="utf-8")
sõnade_info = sõnade_järgnevus(f.read())
f.close()

for sõna in sõnade_info:
    if sõna in sõnade_info[sõna]:
        print(sõna)
