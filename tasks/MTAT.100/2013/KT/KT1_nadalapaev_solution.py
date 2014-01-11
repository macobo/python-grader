"""
Task description (in Estonian):

1. Nädalapäev (3p)
2014. aasta 1. september on esmaspäev. Kirjuta funktsioon nädalapäev, mis võtab
argumendiks täisarvu, mis tähistab mõnda 2014. a. septembri päeva, ning tagastab
sellele päevale vastava nädalapäeva nime. Näiteks nädalapäev(3) peab tagastama 
"kolmapäev" ja nädalapäev(13) peab tagastama "laupäev". Kui mainitud kuus pole
sellist päeva, siis tuleb tagastada "Viga!".

Demonstreeri funktsiooni tööd kasutajalt küsitud päevaga. Funktsiooni
tagastusväärtus tuleb väljastada ekraanile täislausega kujul 
    <päeva number>. september 2014 on <nädalapäeva nimi>. 
Näiteks: 13. september 2014 on laupäev.

Kui funktsioon tagastab "Viga!" (nt. kui kasutaja sisestab 45),  siis tuleb ka 
ekraanile kuvada lihtsalt Viga! (mitte 45. september 2014 on Viga!.).

Vihje: Proovi väärtustada avaldised 12 % 10 ja 22 % 10.
Alternatiiv (-1p). Lahenda sama ülesanne ilma funktsiooni kasutamata.
"""

def nädalapäev(kp):
    j = (kp - 1) % 7
    if kp < 1 or kp > 30: return "Viga!"
    elif j == 0: return "esmaspäev"
    elif j == 1: return "teisipäev"
    elif j == 2: return "kolmapäev"
    elif j == 3: return "neljapäev"
    elif j == 4: return "reede"
    elif j == 5: return "laupäev"
    elif j == 6: return "pühapäev"

kp = int(input('> '))
ans = nädalapäev(kp)
if ans == "Viga!":
    print(ans)
else:
    print(str(kp)+". september 2014 on "+nädalapäev(kp))