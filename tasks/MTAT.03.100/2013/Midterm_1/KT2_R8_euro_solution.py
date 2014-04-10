#Näidislahendus - 1. vaheeksam ül. 2
#Reede 8:15-10:00, 8. november
#Jaan Janno - jaan911@ut.ee

#Tekitan esmalt tühja sõnastiku.
#Kasutan seda hiljem selliselt, et võtmeks
#on nimi ja valuuta ning võtmele vastavaks
#väärtuseks on rahasumma.
#Nt. kontod["Ivars Godmanis: USD"] = 1600.0

kontod = {}

for rida in open("kontod.txt"):

	#Võtan järjest läbi failis
	#asuvad read kasutades for tsüklit.
	
	#Jagan rea juppideks. Nad on listis "rida" kujul:
	# ["eesnimi", "perenimi", "valuuta", "summa"]

	rida = rida.split(":")
	valuuta, raha = rida[1].split()
	
	#Tekitan muutuja raha hulga hoidmiseks.
	#Algseks väärtuseks listi "rida" neljas 
	#element, mille teisendan reaalarvuks.
	
	raha = float(raha)
	
	#Kui tegemist on lattidega, muudan valuuta
	#listis "rida" eurodeks ja arvutan lattidele 
	#vastava rahasumma eurodes.
	
	if valuuta == "LVL":
		valuuta = "EUR"
		raha = raha / 0.702804
		
	#Koostan võtme nimesta ja valuutast.
		
	key = rida[0] + ": " + valuuta + " "
	
	#Kui vaadeldaval inimesel on juba vaadeldavas
	#valuutas raha olemas (ehk võtmele juba vastab 
	#mingi väärtus), siis lisan sinna summale
	#juurde.
	#Kui ei, tekitan sõnastikku uue sissekande.
	
	if key in kontod:
		kontod[key] = raha+kontod[key]
	else:
		kontod[key] = raha
		
#Tekitan uue tekstifaili.

f = open("uued_kontod.txt", "w")

#Võtan for tsükliga läbi kõik
#sõnastiku võtmed.
	
for voti in kontod:

	#Ümardan võtmele vastava rahasumma kahe
	#komakohani ning teisendan sõneks.
	
	kontol_raha = str(round(kontod[voti], 2))
	
	#Kirjutan järjest faili sõnastikus olevad võtmed ning
	#neile vastavad väärtused.
	
	f.write(voti + kontol_raha+"\n")
	
f.close()