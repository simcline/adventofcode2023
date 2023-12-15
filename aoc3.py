import numpy as np

with open('aoc3.txt') as f:
    lines = [line for line in f]

ncols = len(lines[0]) - 1
nrows = len(lines)

adj_matrix = np.zeros((nrows, ncols))

for i in range(nrows):
    for j in range(ncols):
        if lines[i][j] not in ['.'] + [str(x) for x in range(10)]:
            im1 = max(i - 1, 0)
            jm1 = max(j - 1, 0)
            ip1 = min(i + 1, nrows - 1)
            jp1 = min(j + 1, ncols - 1)

            for i2 in range(im1, ip1 + 1):
                for j2 in range(jm1, jp1 + 1):
                    adj_matrix[i2, j2] = 1

res = 0
for i in range(nrows):
    current_value = 0
    coeff = 0
    for j in range(ncols):
        if lines[i][j].isnumeric():
            current_value = 10 * current_value + int(lines[i][j])
            coeff = max(coeff, adj_matrix[i, j])
            if j == ncols - 1:
                res += current_value * coeff
        else:
            res += current_value * coeff
            current_value = 0
            coeff = 0
res

##part 2
gear_adj_dict = {(i, j): [] for i in range(nrows) for j in range(ncols)}
gear_dict = {}
gear_neighbours = {}

for i in range(nrows):
    for j in range(ncols):
        if lines[i][j] == '*':
            gear_dict[(i, j)] = 1
            gear_neighbours[(i, j)] = 0

            im1 = max(i - 1, 0)
            jm1 = max(j - 1, 0)
            ip1 = min(i + 1, nrows - 1)
            jp1 = min(j + 1, ncols - 1)

            for i2 in range(im1, ip1 + 1):
                for j2 in range(jm1, jp1 + 1):
                    gear_adj_dict[(i2, j2)].append((i, j))

for i in range(nrows):
    current_value = 0
    gears = set()
    for j in range(ncols):
        if lines[i][j].isnumeric():
            current_value = 10 * current_value + int(lines[i][j])
            gears = gears.union(set(gear_adj_dict[(i, j)]))
            if j == ncols - 1:
                for g in gears:
                    gear_neighbours[g] += 1
                    gear_dict[g] *= current_value
                current_value = 0
                gears = set()
        else:
            for g in gears:
                gear_neighbours[g] += 1
                gear_dict[g] *= current_value
            current_value = 0
            gears = set()
res = 0
for g in gear_neighbours:
    if gear_neighbours[g] == 2:
        res += gear_dict[g]
res
