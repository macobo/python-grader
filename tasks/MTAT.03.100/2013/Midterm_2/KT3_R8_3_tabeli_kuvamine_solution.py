f = open("tulemused.csv", encoding="utf-8")


päis = f.readline().strip('\n').split(",")

kriips = ""
for veerg in päis:
    kriips += "-" * (len(veerg) + 3)
kriips += '-'

print(kriips)
for veerg in päis:
    print("| " + veerg + " ", end="")
print("|")

print(kriips)

for rida in f:
    veerud = rida.strip().split(",")
    for i in range(len(veerud)):
        veerg = veerud[i]
        print("| " + veerg.ljust(len(päis[i])) + " ", end="")
        
    print("|")

print(kriips)

f.close()
