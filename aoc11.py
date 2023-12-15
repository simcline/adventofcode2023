with open('aoc11.txt') as f:
    lines = [line[:-1] if line.endswith('\n') else line for line in f]

big_lines = []
for i in range(len(lines)):
    if all(c == '.' for c in lines[i]):
        big_lines.append(i)

big_cols = []
for j in range(len(lines[0])):
    if all(c=='.' for c in [lines[i][j] for i in range(len(lines))]):
        big_cols.append(j)

galaxies = []

for i in range(len(lines)):
    for j in range(len(lines[i])):
        if lines[i][j] == '#':
            galaxies.append((i,j))

galaxies.sort()

def compute_sum_dist(m):

    galaxies2 = []
    for g in galaxies:
        g_i, g_j = g
        for i in big_lines:
            if i < g[0]:
                g_i+=m-1
        for j in big_cols:
            if j < g[1]:
                g_j+=m-1
        galaxies2.append((g_i,g_j))
    galaxies2.sort()
    dists=0
    for i in range(len(galaxies2)):
        for j in range(i+1, len(galaxies2)):
            dists+= abs(galaxies2[i][0] - galaxies2[j][0]) + abs(galaxies2[j][1]-galaxies2[i][1])
    return(dists)

compute_sum_dist(2)

#part 2
compute_sum_dist(1e6)