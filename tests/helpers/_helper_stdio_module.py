from time import sleep
import random
print('1')

a = input()
while a != 'END':
    print(a)
    a = input()
    sleep(random.uniform(0.5, 1.5))