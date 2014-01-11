from turtle import *

def fraktal(tase, pikkus):
    if tase == 1:
        forward(pikkus)
        backward(pikkus)
    else:
        forward(pikkus)
        left(90)
        forward(pikkus/2)
        right(90)
        kantpuu(tase-1, pikkus*0.5)
        right(90)
        forward(pikkus)
        left(90)
        kantpuu(tase-1, pikkus*0.5)
        left(90)
        forward(pikkus/2)
        left(90)
        forward(pikkus)
        left(180)



left(90)
delay(0)
speed(10)
kantpuu(5, 60)
#hideturtle()
exitonclick()
