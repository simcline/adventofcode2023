from math import lcm

with open('aoc8.txt') as f:
    lines = [line for line in f]

hmap = {}
for l in lines[2:]:
    s = l.split(' = ')
    hmap[s[0]] = (s[1][1:4], s[1][6:9])

directions = lines[0][:-1]
n = len(directions)

x = 'AAA'
dirpos = 0

while x != 'ZZZ':
    x = hmap[x][0 if directions[dirpos % n] == 'L' else 1]
    dirpos += 1

dirpos


# part 2
def get_n_steps(x):
    dirpos = 0
    while not x.endswith('Z') or dirpos == 0:
        x = hmap[x][0 if directions[dirpos % n] == 'L' else 1]
        dirpos += 1
    return dirpos


x_vec = [z for z in hmap.keys() if z.endswith('A')]


def run_steps(x, k):
    dirpos = 0

    while dirpos < k:
        x = hmap[x][0 if directions[dirpos % n] == 'L' else 1]
        dirpos += 1

    return x


n_steps = [get_n_steps(x) for x in x_vec]  # k1,...,kN
z_vec = [run_steps(x, k) for x, k in zip(x_vec, n_steps)]
zn_steps = [get_n_steps(z) for z in z_vec]  # p1,...,pN

# answer is the smallest Q such that Q is of the form k1+alpha1 p1 = ... = kN +alphaN pN with alpha a vector of
# integers. since we have ki=pi, the answer is the least common multiple of k1,...,kn.

Q = lcm(*n_steps)
Q
