def nädalapalk(tunde, tavapalk):
    tulemus = tunde * tavapalk
    if tunde > 40:
        tulemus = tulemus + (tunde - 40) * tavapalk / 2
    return tulemus

tunde = float(input("Tunde: "))
palk = float(input("Palk: "))

tulemus = nädalapalk(tunde, palk)
#print(tulemus)
f = open('palk.txt', 'w')
f.write(str(tulemus))
f.close()