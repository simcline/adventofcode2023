with open('aoc15.txt') as f:
    instructions = [line for line in f][0][:-1].split(',')


def hash(s):
    r = 0
    for c in s:
        r = ((r + ord(c)) * 17) % 256
    return r


sum(hash(ins) for ins in instructions)

# part 2
boxes = [[] for i in range(256)]

for ins in instructions:
    if '=' in ins:
        key, value = ins.split('=')
        h = hash(key)

        to_replace = -1
        for i in range(len(boxes[h])):
            if boxes[h][i][0] == key:
                to_replace = i

        if to_replace == -1:
            boxes[h].append((key, int(value)))
        else:
            boxes[h][to_replace] = (key, int(value))
    else:
        key = ins.split('-')[0]
        h = hash(key)
        for i in range(len(boxes[h])):
            if boxes[h][i][0] == key:
                boxes[h].remove(boxes[h][i])
                break

sum((i + 1) * sum((j + 1) * boxes[i][j][1] for j in range(len(boxes[i]))) for i in range(len(boxes)))
