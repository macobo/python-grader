f = open("nimed.txt")
nimed = {}
for rida in f:
    osad = rida.split(maxsplit=1)
    nimed[osad[0]] = osad[1].strip()

f.close()

f = open("lapsed.txt")
lapsevanemad = {}

for rida in f:
    osad = rida.split()
    vanema_nimi = nimed[osad[0]]
    if not vanema_nimi in lapsevanemad:
        lapsevanemad[vanema_nimi] = set()

    lapsevanemad[vanema_nimi].add(nimed[osad[1]])

f.close()

for vanem in lapsevanemad:
    print(vanem + ": " + ", ".join(lapsevanemad[vanem]))
