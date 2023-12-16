import numpy as np
with open('aoc14.txt') as f:
    lines = [line[:-1] if line.endswith('\n') else line for line in f]

m = np.zeros((len(lines), len(lines[0])))

for i in range(len(lines)):
    for j in range(len(lines[i])):
        match lines[i][j]:
            case '#':
                m[i,j]=2
            case '.':
                m[i,j]=1
            case '_':
                pass

def get_one_step_ahead_north(m):
    something_moved = True
    while(something_moved):
        something_moved=False
        for i in range(1,len(lines)):
            for j in range(len(lines[i])):
                if m[i,j]==0 and m[i-1,j]==1:
                    m[i-1,j]=0
                    m[i,j]=1
                    something_moved=True
    return m

def get_one_step_ahead_east(m):
    something_moved = True
    while(something_moved):
        something_moved=False
        for i in range(len(lines)):
            for j in range(len(lines[i])-1):
                if m[i,j]==0 and m[i,j+1]==1:
                    m[i,j+1]=0
                    m[i,j]=1
                    something_moved=True
    return m

def get_one_step_ahead_south(m):
    something_moved = True
    while(something_moved):
        something_moved=False
        for i in range(len(lines)-1):
            for j in range(len(lines[i])):
                if m[i,j]==0 and m[i+1,j]==1:
                    m[i+1,j]=0
                    m[i,j]=1
                    something_moved=True
    return m


def get_one_step_ahead_west(m):
    something_moved = True
    while(something_moved):
        something_moved=False
        for i in range(len(lines)):
            for j in range(1,len(lines[i])):
                if m[i,j]==0 and m[i,j-1]==1:
                    m[i,j-1]=0
                    m[i,j]=1
                    something_moved=True
    return m

sum( (m.shape[1] -i)*sum(m[i,:] == 0) for i in range(m.shape[1]))



#part 2

weights = []
m2 = m.copy()
for i in range(1000):
    if i%50 == 0:
        print(i)
    m2 = get_one_step_ahead_north(m2)
    m2 = get_one_step_ahead_west(m2)
    m2 = get_one_step_ahead_south(m2)
    m2 = get_one_step_ahead_east(m2)
    weights.append(sum( (m2.shape[1] -i)*sum(m2[i,:] == 0) for i in range(m2.shape[1])))

#looking at the vector, we easily see that it is ultimately periodic with T=42 starting from index 117 at value 95254

T = 42
init = 117
one_period_vec = weights[init:(init+T)]
v = 1e9
one_period_vec[int(v-1-init)%T]