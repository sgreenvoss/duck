import turtle as td
import math as m
import face_functionality as f

"""model: https://sketchfab.com/3d-models/lowpoly-duck-animated-0242fe38361c4bdabadcfddb42eb3325"""

GREENS = ["DarkSeaGreen1", "DarkSeaGreen3", "DarkSeaGreen4"]
BLUES = ["DarkSlateGray1", "DarkSlateGray3", "DarkSlateGrey"]
PINKS = ["DeepPink", "DeepPink3", "DeepPink4"]

t = td.Turtle()

#prob should pass a turtle in rather than have global turtle accessed by this
# TODO add turtle param
class Shape():
    def __init__(self, data, color_scheme, scale_factor, turtle):
        self.points = []
        for i in range(len(data["points"])):
            self.points.append(Point(data["points"][i], i + 1))
        self.scale_factor = scale_factor
        self.color_scheme = color_scheme

        self.lines = data["lines"]
        self.faces = data["faces"]
        self.t = turtle

    def rotate(self, axis, angle):
        """axis:int, 0 = x, 1 = y, 2 = z"""
        match axis:
            case 0:
                for p in self.points:
                    p.x_rotate(angle)
            case 1:
                for p in self.points:
                    p.y_rotate(angle)
            case 2:
                for p in self.points:
                    p.z_rotate(angle)

    def draw_points(self):
        t.penup()
        for p in self.points:
            t.setposition(p.get_x() * self.scale_factor, p.get_y() * self.scale_factor)
            size, color = self.scale_points(p.get_z())
            self.t.dot(size, self.color_scheme[color])

    def draw_lines(self):
        for line in self.lines:
            point = self.points[line[0] - 1]
            self.recolor_line(point)
            self.go_to_scaled_x_y(point)
            self.t.pendown()
            new_point = self.points[line[1] - 1]
            self.go_to_scaled_x_y(new_point)
            self.t.penup()

    def draw_faces(self):

        for line in self.faces:
            self.t.fillcolor(line[-1])
            self.t.begin_fill()
            for item in line[:-1]:
                point = self.points[item - 1]
                self.go_to_scaled_x_y(point)
            self.t.end_fill()


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

    def crx(self):
        self.t.clear()
        self.rotate(0, m.pi / 6)
        self.draw_points()
        self.draw_lines()
        self.draw_faces()

    def rx(self):
        self.t.clear()
        self.rotate(0, - m.pi / 6)
        self.draw_points()
        self.draw_lines()
        self.draw_faces()

    def crz(self):
        self.t.clear()
        self.rotate(2, m.pi / 6)
        self.draw_points()
        self.draw_lines()
        self.draw_faces()

    def rz(self):
        self.t.clear()
        self.rotate(2, - m.pi / 6)
        self.draw_points()
        self.draw_lines()
        self.draw_faces()

    def ry(self):
        self.t.clear()
        self.rotate(1, m.pi / 6)
        self.draw_points()
        self.draw_lines()
        self.draw_faces()

    def cry(self):
        self.t.clear()
        self.rotate(1, - m.pi / 6)
        self.draw_points()
        self.draw_lines()
        self.draw_faces()

    def set_listeners(self):
        screen.listen()

        td.onkey(self.rx, "Down")
        td.onkey(self.crx, "Up")
        td.onkey(self.crz, "z")
        td.onkey(self.rz, "x")
        td.onkey(self.ry, "Right")
        td.onkey(self.cry, "Left")


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


cubestruct = [
    [-1, 1, 1],
    [-1, -1, 1],
    [1, 1, 1],
    [1, -1, 1],
    [-1, 1, -1],
    [-1, -1, -1],
    [1, 1, -1],
    [1, -1, -1]
]

screen = td.Screen()
screen.tracer(0)
data = f.get_data()
Duck = Shape(data, PINKS, 400, t)

screen.update()

Duck.set_listeners()

td.mainloop()