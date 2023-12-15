import numpy as np
from functools import reduce

with open('aoc6.txt') as f:
    lines = [line for line in f]

times = [int(x) for x in lines[0][:-1].split('Time: ')[1].split(' ') if x != '']
distances = [int(x) for x in lines[1][:-1].split('Distance: ')[1].split(' ') if x != '']

reachable_dists = []
for t, d in zip(times, distances):
    reachable_dists.append([(t - k) * k > d for k in range(t + 1)])

np.prod([sum(rd) for rd in reachable_dists])

# part 2 : by monotonicity of x->x(t-x) on [0,t/2], we find the first time it reaches the threshold d by dichotomy
time = reduce(lambda x, y: int(str(x) + str(y)), times)
distance = reduce(lambda x, y: int(str(x) + str(y)), distances)

up_first_idx_above = time // 2
down_first_idx_above = 0

cont = True
while cont:
    test = (up_first_idx_above + down_first_idx_above) // 2
    if (time - test) * test > distance:
        up_first_idx_above = test
    else:
        down_first_idx_above = test

    if up_first_idx_above - down_first_idx_above <= 1:
        cont = False

fst = down_first_idx_above if (time - down_first_idx_above) * down_first_idx_above > distance else up_first_idx_above
# by a symmetry argument of x(t-x) we know that we span (res, t-res)
len(range(fst, time - fst + 1))
