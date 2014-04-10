def arvuta(tehe, a, b):
    if tehe == '+': return a+b
    if tehe == '-': return a-b
    if tehe == '/': return a/b
    if tehe == '*': return a*b

# tehe = input('Tehe: ')
# a = float(input())
# b = float(input())
# print(arvuta(tehe, a, b))

f = open('algandmed.txt')
tehe = f.readline().strip()
a = float(f.readline().strip())
b = float(f.readline().strip())
print(arvuta(tehe, a, b))
f.close()