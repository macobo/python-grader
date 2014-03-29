a = [1,2,3]
b = list(a)
c = b

b.append(4)

print(c) # should print [1,2,3,4]
print(b) # should print [1,2,3,4]
print(a) # should print [1,2,3]