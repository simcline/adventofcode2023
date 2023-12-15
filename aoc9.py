import numpy as np

with open('aoc9.txt') as f:
    lines = [line for line in f]

series = [[int(x) for x in l.split(' ') if x != ''] for l in lines]

res = 0
for s in series:
    delta_list = [np.array(s)]

    while any(delta_list[-1] != 0):
        delta_list.append(np.diff(delta_list[-1]))

    res += sum(d[-1] for d in delta_list)
res

# part 2
res = 0
for s in series:
    delta_list = [np.array(s)]

    while any(delta_list[-1] != 0):
        delta_list.append(np.diff(delta_list[-1]))

    res += sum((-1) ** i * delta_list[i][0] for i in range(len(delta_list)))
res
