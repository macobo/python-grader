from turtle import *

def nool(tase, pikkus):
    if tase > 0:
        forward(pikkus)
        left(120)
        nool(tase-1, pikkus*0.5)
        right(240)
        nool(tase-1, pikkus*0.5)
        left(120)
        backward(pikkus)
        

right(90)
delay(0)
speed(10)
nool(1, 200)
hideturtle()
