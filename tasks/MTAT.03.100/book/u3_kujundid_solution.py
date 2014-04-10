def ruut(n):
    return "\n".join(["*"*n] + ['*'+' '*(n-2)+'*' for _ in range(n-2) ] + ["*"*n])

def kolmnurk(n):
    return "\n".join("*"*i for i in range(1, n+1))

ridu = int(input("Ridu: "))

print(ruut(ridu))
print(kolmnurk(ridu))