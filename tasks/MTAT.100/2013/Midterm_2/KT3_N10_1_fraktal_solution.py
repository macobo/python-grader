from turtle import *


def fraktal(tase, külg):
    if tase > 0:
        for _ in range(4):
            forward(külg)
            right(45)
            ruudik(tase-1, külg*0.4)
            left(135)


delay(0)
speed(10)
ruudik(3, 60)
hideturtle()
