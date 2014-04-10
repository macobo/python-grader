# #mida teha?

def mida_teha(a, b):
    if b== "P" or b== "p":
        return("puhka")
    elif a==1 or a==2 or a==12:
        return("küta ahju")
    elif a==3 or a==4 or a==5:
        return("külva redist")
    elif a==6 or a==7 or a==8:
        return("rauta rege")
    elif a==9 or a==10 or a== 11:
        return("riisu lehti")
    elif a<1 or a>12:
        return("õpi kalender selgeks")

n = int(input('Sisesta kuu number: '))
lyh = input('Sisesta nädalapäeva lühend: ')
print(mida_teha(n, lyh).capitalize() + '!')
