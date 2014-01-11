from turtle import *

def nurgik(tase, pikkus):
    if tase > 0:
        for _ in range(3):
            forward(pikkus)
            right(60)
            nurgik(tase-1, pikkus/2)
            right(60)

delay(0)
speed(10)
nurgik(1, 200)
hideturtle()
