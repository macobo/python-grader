summa = int(input("Sisesta pangakontol olev summa: "))
intress = int(input("Sisesta intress: ")) / 100

in5years = summa * (1 + intress) ** 5

print("5 aasta pärast on teie kontol",in5years,"eurot")