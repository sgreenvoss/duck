import turtle as td
import math as m
import face_functionality as f

"""model: https://sketchfab.com/3d-models/lowpoly-duck-animated-0242fe38361c4bdabadcfddb42eb3325"""

GREENS = ["DarkSeaGreen1", "DarkSeaGreen3", "DarkSeaGreen4"]
BLUES = ["DarkSlateGray1", "DarkSlateGray3", "DarkSlateGrey"]
PINKS = ["DeepPink", "DeepPink3", "DeepPink4"]

TRANSLATE_AMT = 0.05
ROTATE_AMT = m.pi / 45


class Shape():
    def __init__(self, data, color_scheme, p=False, l=True, f=False, scale_factor=100, turtle=td.Turtle(), initd=(0, 0), show=True):
        self.points = {}
        for i in range(len(data["points"])):
            self.points[i + 1] = Point(data["points"][i])
            # print(f"{i}, {self.points[i]}")

        self.scale_factor = scale_factor
        self.color_scheme = color_scheme
        self.l = l
        self.f = f
        self.p = p
        self.sorted_pts = sorted(self.points, key=self.points.get)
        # print(self.points)
        
        self.lines = data["lines"]
        if self.f:
            faceinfo = data["faces"]
            self.faces = {}
            for i in range(len(faceinfo) - 1):
                pointlist = [self.points[j] for j in faceinfo[i][:-1]]
                pointlist.append(faceinfo[i][-1])
                # print(pointlist)
                self.faces[i] = Face(pointlist)
           
            # print("FACES:", self.faces)
        if initd:
            for point in self.points.values():
                point.dx += initd[0] * TRANSLATE_AMT
                point.dy += initd[1] * TRANSLATE_AMT
        self.t = turtle

        if show:
            self.draw()
            
        
    
    def re_sort_faces(self):
        self.sorted_faces = sorted(self.faces.values())
        
        # print(self.sorted_faces)


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
                for v in self.points.values():
                    v.x_rotate(ROTATE_AMT * sign)
            case 'y':
                for v in self.points.values():
                    v.y_rotate(ROTATE_AMT * sign)
            case 'z':
                for v in self.points.values():
                    v.z_rotate(ROTATE_AMT * sign)
        self.draw()

    def find_center(self):
        s_x = s_y = s_z = 0
        ln = len(self.points)
        for v in self.points.values():
            s_x += v.get_x()
            s_y += v.get_y()
            s_z += v.get_z()
        self.center = s_x / ln, s_y / ln, s_z / ln
        

    def draw_points(self):
        for v in self.points.values():
            self.t.setposition((v.get_x() + v.dx) * self.scale_factor, (v.get_y() + v.dy) * self.scale_factor)
            size, color = self.scale_points(v.get_z())
            self.t.dot(size, self.color_scheme[color])

    def draw_lines(self):
        self.t.penup()
        self.t.hideturtle()
        for line in self.lines:
            point = self.points[line[0]]
            self.recolor_line(point)
            self.go_to_scaled_x_y(point)
            self.t.pendown()
            new_point = self.points[line[1]]
            self.go_to_scaled_x_y(new_point)
            self.t.penup()

    def draw_faces(self):
        self.t.penup()
        self.t.hideturtle()
        self.re_sort_faces()
        # print("\n\n\nNEW:")
        for face in self.sorted_faces: # self.sorted_faces?
            # print("face:", face)
            self.t.fillcolor(face.color)
            start = True
            for point in face.pts: 
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
        self.t.setposition((point.dx + point.get_x()) * self.scale_factor, (point.dy + point.get_y()) * self.scale_factor)

    
    def translate(self, axis:str, sign:int):
        """
        axis: 'x' or 'y'
        sign: + or - 1
        """
        self.t.clear()
        match axis:
            case 'x':
                for v in self.points.values():
                    v.dx += TRANSLATE_AMT * sign
            case 'y':
                for v in self.points.values():
                    v.dy += TRANSLATE_AMT * sign
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
    def __init__(self, lyst):
        self.x = lyst[0]
        self.y = lyst[1]
        self.z = lyst[2]
        self.dx = 0
        self.dy = 0

    def __repr__(self):
        return f"Point({self.x}, {self.y}, {self.z})"

    def __gt__(self, other):
        return self.z > other.z

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

class Face():
    def __init__(self, points_col):
        # points_col is a list of Point objects
        # print("this is points_col:", points_col)
        self.pts = []
        avgz = 0
        for point in points_col[:-1]:
            self.pts.append(point)
            avgz += point.z
        self.average_z = avgz / (len(points_col) - 1)
        self.color = points_col[-1]
        # print("COLOR: ", self.color)

    def __gr__(self, other):
        return self.average_z < other.average_z
    
    def __lt__(self, other):
        return self.average_z > other.average_z

    def __repr__(self):
        return f"Face(average z: {self.average_z})"
        
def main():
    screen = td.Screen()
    screen.tracer(0)
    data = f.get_data("models-not-mine/duck.txt")
    turt = td.Turtle()
    Duck = Shape(data, BLUES, scale_factor=400, l=False, f=True, initd=(1, 1))
    Duck2 = Shape(data, PINKS, scale_factor=300, initd=(-5, 4), turtle=turt)

    screen.update()

    Duck.set_listeners()

    td.mainloop()

if __name__ == '__main__':
    main()
