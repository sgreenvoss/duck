def get_lines(filename):
    f = open(filename, "r")
    duck_lines = []
    for l in f.readlines():
        line = l[2:]
        line = line.split()
        for i in range(len(line)):
            line[i] = int(line[i])
        duck_lines.append(line)
    return duck_lines
