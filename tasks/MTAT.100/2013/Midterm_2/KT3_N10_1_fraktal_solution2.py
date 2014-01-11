from turtle import *


def fraktal(tase, pikkus):
    if tase > 0:
        for _ in range(4):
            forward(pikkus)

            right(45)
            fraktal(tase-1, pikkus/2)
            left(45)
            left(90)

speed(0)
fraktal(3, 60)
exitonclick()