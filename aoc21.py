with open('aoc21.txt') as f:
    lines = [line[:-1] if line.endswith('\n') else line for line in f]

nrows, ncols = len(lines), len(lines[0])

for i in range(nrows):
    for j in range(ncols):
        if lines[i][j] == 'S':
            start = (i,j)

possible_steps = {start}
possible_steps_next = set()

def check_pos(p):
    i,j = p
    return lines[i%nrows][j%ncols] != '#'

ps = []
for i in range(64):
    if i%100 == 0:
        print(i)
    possible_steps_next = set()
    for pos in possible_steps:
        j,k = pos
        for p in [(j+1,k), (j-1,k), (j,k+1), (j,k-1)]:
            if check_pos(p):
                possible_steps_next.add(p)
    possible_steps = possible_steps_next.copy()
    ps.append(len(possible_steps))

ps[63]

#part 2
D = 26501365
# After trying many geometrical stuff, looking for spatial periodicity and so on.... I realized that D-start[0] is a multiple of
# nrows, i.e D-start[0] = N*nrows. Then I started to play around with small values of N and realized that the number
# of possible steps is quadratic in N. This is actually not that surprising because when there are no rocks the
# solution is exactly in (nrows*(N+1))^2. I am not entirely sure about why it works with randomly placed rocks to be
# honest, but anyway, here we are and the problem becomes trivial:

N = (D-start[0])/nrows

# look for the solution as phi(n) = an^2+bn+c, evaluate at n=0,1,2 and solve for a,b,c
c=ps[64]
apb  = ps[64+nrows] - c
a = 0.5*(ps[64+2*nrows] - c - 2*apb)
b = apb -a
def phi(n):
    return int(a*n**2 + b*n + c)

phi(N)