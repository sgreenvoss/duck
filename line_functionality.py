f = open("models not mine/duck_lines.txt", "r")
duck_lines = []


def get_lines():
    for l in f.readlines():
        line = l[2:]
        line = line.split()
        for i in range(len(line)):
            line[i] = int(line[i])
        duck_lines.append(line)
    return duck_lines

print(duck_lines)

