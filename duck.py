import turtle as td
import math as m
import face_functionality as f

"""model: https://sketchfab.com/3d-models/lowpoly-duck-animated-0242fe38361c4bdabadcfddb42eb3325"""

GREENS = ["DarkSeaGreen1", "DarkSeaGreen3", "DarkSeaGreen4"]
BLUES = ["DarkSlateGray1", "DarkSlateGray3", "DarkSlateGrey"]
PINKS = ["DeepPink", "DeepPink3", "DeepPink4"]

TRANSLATE_AMT = 0.05
ROTATE_AMT = m.pi / 6


class Shape():
    def __init__(self, data, color_scheme, p=False, l=True, f=False, scale_factor=100, turtle=td.Turtle()):
        self.points = []
        for i in range(len(data["points"])):
            self.points.append(Point(data["points"][i], i + 1))
        self.scale_factor = scale_factor
        self.color_scheme = color_scheme
        self.l = l
        self.f = f
        self.p = p
        
        if self.l:
            self.lines = data["lines"]
        if self.f:
            self.faces = data["faces"]

        self.t = turtle

    def draw(self):
        self.t.clear()
        self.t.penup()
        if self.p:
            self.draw_points()
        if self.l:
            self.draw_lines()
        if self.f:
            self.draw_faces()

    

    def rotate(self, axis, sign):
        """axis:str, x, y, z
            sign: int, 1, -1"""
        match axis:
            case 'x':
                for p in self.points:
                    p.x_rotate(ROTATE_AMT)
            case 'y':
                for p in self.points:
                    p.y_rotate(ROTATE_AMT)
            case 'z':
                for p in self.points:
                    p.z_rotate(ROTATE_AMT)
        self.draw()

    def draw_points(self):
        for p in self.points:
            self.t.setposition(p.get_x() * self.scale_factor, p.get_y() * self.scale_factor)
            size, color = self.scale_points(p.get_z())
            self.t.dot(size, self.color_scheme[color])

    def draw_lines(self):
        self.t.penup()
        self.t.hideturtle()
        for line in self.lines:
            point = self.points[line[0] - 1]
            self.recolor_line(point)
            self.go_to_scaled_x_y(point)
            self.t.pendown()
            new_point = self.points[line[1] - 1]
            self.go_to_scaled_x_y(new_point)
            self.t.penup()

    def draw_faces(self):
        self.t.penup()
        self.t.hideturtle()
        for line in self.faces:
            self.t.fillcolor(line[-1])
            start = True
            for item in line[:-1]: 
                point = self.points[item - 1]
                self.go_to_scaled_x_y(point)
                if start:
                    self.t.begin_fill()
                    start = False
            self.t.end_fill()


# dupid magic numebrs here
# TODO: fix
    def scale_points(self, z):
        if z > 0.5:
            return 6, 0
        elif 0.5 >= z > 0:
            return 5, 1
        else:
            return 3, 2

    def recolor_line(self, point):
        size, color = self.scale_points(point.get_z())
        self.t.pensize(size)
        self.t.pencolor(self.color_scheme[color])

    def go_to_scaled_x_y(self, point):
        self.t.setposition(point.get_x() * self.scale_factor, point.get_y() * self.scale_factor)

    
    def translate(self, axis:str, sign:int):
        """
        axis: 'x' or 'y'
        sign: + or - 1
        """
        self.t.clear()
        match axis:
            case 'x':
                for point in self.points:
                    point.x += TRANSLATE_AMT * sign
            case 'y':
                for point in self.points:
                    point.y += TRANSLATE_AMT * sign
        self.draw()

    def set_listeners(self):
        screen.listen()

        td.onkey(lambda: self.rotate('x', -1), "Down")
        td.onkey(lambda:self.rotate('x', 1), "Up")
        td.onkey(lambda: self.rotate('z', 1), "z")
        td.onkey(lambda: self.rotate('z', -1), "x")
        td.onkey(lambda: self.rotate('y', 1), "Right")
        td.onkey(lambda: self.rotate('y', -1), "Left")

        td.onkey(lambda: self.translate('y', -1), "j")
        td.onkey(lambda: self.translate('y', 1), "u")
        td.onkey(lambda: self.translate('x', 1), "k")
        td.onkey(lambda: self.translate('x', -1), "h")



class Point():
    def __init__(self, lyst, i):
        self.x = lyst[0]
        self.y = lyst[1]
        self.z = lyst[2]
        self.index = i

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_z(self):
        return self.z

    def x_rotate(self, angle):
        x, y, z = self.x, self.y, self.z
        self.x = x
        self.y = y * m.cos(angle) - z * m.sin(angle)
        self.z = y * m.sin(angle) + z * m.cos(angle)

    def y_rotate(self, angle):
        x, y, z = self.x, self.y, self.z
        self.x = x * m.cos(angle) + z * m.sin(angle)
        self.y = y
        self.z = z * m.cos(angle) - x * m.sin(angle)

    def z_rotate(self, angle):
        x, y, z = self.x, self.y, self.z
        self.x = x * m.cos(angle) - y * m.sin(angle)
        self.y = x * m.sin(angle) + y * m.cos(angle)
        self.z = z
    




screen = td.Screen()
screen.tracer(0)
data = f.get_data("models-not-mine/duck.txt")
Duck = Shape(data, BLUES, scale_factor=400, l=False, f=True)

screen.update()

Duck.set_listeners()

td.mainloop()
