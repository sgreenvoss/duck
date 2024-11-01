import turtle as td
import math as m
import face_functionality as f
from duck import *


def dancing_ducks():
    screen = td.Screen()
    screen.tracer(0)
    data = f.get_data("models-not-mine/duck.txt")
    turt = td.Turtle()
    turt.hideturtle()
    turt2 = td.Turtle()
    turt2.hideturtle()
    Duck = Shape(data, BLUES, scale_factor=400, l=False, f=True, initd=(1, 1))
    Duck2 = Shape(data, PINKS, scale_factor=300, initd=(-5, 4), turtle=turt)
    # Duck3 = Shape(data, GREENS, scale_factor=150, initd=(5, -10), p=True, l=False, turtle=turt2)

    screen.update()

    while True:

        Duck.rotate('x', 1)
        Duck2.rotate('y', -1)
        # Duck3.rotate('y', 1)
        Duck.draw()
        Duck2.draw()
        # Duck3.draw()
        
        screen.update()

dancing_ducks()