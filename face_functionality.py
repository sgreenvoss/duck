f = open("models not mine/duck.txt", "r")
faces = []
lines = []
points = []

#TODO: organize file structure so user doesn't have to look at this one

def get_data():
    color = "black" #set as default
    for l in f.readlines():
        l = l.split()
        match l[0]:
            case "usemtl":
                color = l[1]
            case "f":
                l = l[1:]
                real_list = []
                for i in range(len(l)):
                    item = l[i].split('/')
                    real_list.append(int(item[0]))
                real_list.append(color)
                faces.append(real_list)

            case "l":
                line = l[1:]
                for i in range(len(line)):
                    line[i] = int(line[i])
                lines.append(line)

            case "v":
                l = l[1:]
                for i in range(len(l)):
                    l[i] = float(l[i])
                points.append(l)

    return {"faces": faces, "lines": lines, "points": points}
