import numpy as np

with open('aoc24.txt') as f:
    lines = [line[:-1] if line.endswith('\n') else line for line in f]

xmin = 200000000000000
ymin = 200000000000000
xmax = 400000000000000
ymax = 400000000000000
area = (xmin, xmax, ymin, ymax)


class Trajectory:

    def __init__(self, line):
        pos, velocity = line.split(' @ ')
        self.position = [int(x) for x in pos.split(', ')]
        self.velocity = [int(x) for x in velocity.split(', ')]

    def pointBelongsToAreaXY(self, point, area):
        xmin, xmax, ymin, ymax = area
        return xmin <= point[0] <= xmax and ymin <= point[1] <= ymax

    def isVertical(self):
        return self.velocity[0] == 0

    def getTFromXY(self, pos):
        if not self.isVertical():
            return (pos[0] - self.position[0]) / self.velocity[0]
        return (pos[1] - self.position[1]) / self.velocity[1]

    def getLineEquationXY(self):
        if not self.isVertical():
            return self.position[1] - self.velocity[1] / self.velocity[0] * self.position[0], \
                   self.velocity[1] / self.velocity[0]
        return np.Inf, np.Inf

    def getStartEndXY(self, area):
        xmin, xmax, ymin, ymax = area
        if self.isVertical():
            return (self.position[0], ymin), (self.position[0], ymax)

        a, b = self.getLineEquationXY()
        ret = []
        if ymin <= a + b * xmin <= ymax:
            ret.append((xmin, a + b * xmin))
        if ymin <= a + b * xmax <= ymax:
            ret.append((xmax, a + b * xmax))
        if xmin < (ymin - a) / b < xmax:
            ret.append(((ymin - a) / b, ymin))
        if xmin < (ymax - a) / b < xmax:
            ret.append(((ymax - a) / b, ymax))
        return tuple(ret)

    def passesThroughAreaXY(self, area):
        se = self.getStartEndXY(area)
        return any([self.getTFromXY(x) >= 0 for x in se])

    def intersectsXY(self, other):
        vx, vy = self.velocity[0:2]
        vxo, vyo = other.velocity[0:2]

        x, y = self.position[0:2]
        xo, yo = other.position[0:2]

        dx, dy = x - xo, y - yo
        A = np.array([[-vx, vxo], [-vy, vyo]])
        det = np.linalg.det(A)

        if det != 0:
            t_to = np.dot(np.linalg.inv(A), np.array([dx, dy]))

            if t_to[0] >= 0 and t_to[1] >= 0:
                return self.pointBelongsToAreaXY((x + t_to[0] * vx, y + t_to[0] * vy), area)
            else:
                return False
        else:
            if x * vy - y * vx == xo * vy - yo * vx:  # infinite number of solutions
                return self.passesThroughAreaXY(area) and other.passesThroughAreaXY(area)
            else:
                return False

    def __repr__(self):
        ret = f'position : {self.position}; velocity : {self.velocity};'
        if self.isVertical():
            ret += f'equation: x= {self.position[0]}'
        else:
            a, b = self.getLineEquationXY()
            ret += f'equation: y= {a} + {b}x'
        return ret


trajectories = [Trajectory(l) for l in lines]

counter = 0
for i in range(len(trajectories)):
    for j in range(i + 1, len(trajectories)):
        counter += trajectories[i].intersectsXY(trajectories[j])

counter

# part 2
# using (in vector notation) that x+t*v = x' + t*v', we essentially use the fact that the vector product of x-x' and v-v' is 0 for all x' and v' in the hailstone set. This yields linear equations that can be projected in (X,Y) and (X,Z).
# Not particularly interesting and tedious...
n = 4
mat = np.zeros((n, n), dtype = 'float64')

j=0
for i in range(1,5):
    mat[i-1,0] = trajectories[i].velocity[1] - trajectories[j].velocity[1]
    mat[i-1,1] = trajectories[j].velocity[0] - trajectories[i].velocity[0]
    mat[i-1,2] = trajectories[j].position[1] - trajectories[i].position[1]
    mat[i-1,3] = trajectories[i].position[0] - trajectories[j].position[0]

B = np.zeros((n,))
for i in range(1,5):
    B[i - 1] = trajectories[j].position[1] * trajectories[j].velocity[0] - trajectories[i].position[1] * \
                     trajectories[i].velocity[0] + trajectories[i].position[0] * trajectories[i].velocity[1] - \
                     trajectories[j].position[0] * trajectories[j].velocity[1]
x,y = np.dot(np.linalg.inv(mat), B)[0:2]

mat = np.zeros((n, n), dtype = 'float64')
for i in range(1,5):
    mat[i-1,0] = trajectories[i].velocity[2] - trajectories[j].velocity[2]
    mat[i-1,1] = trajectories[j].velocity[0] - trajectories[i].velocity[0]
    mat[i-1,2] = trajectories[j].position[2] - trajectories[i].position[2]
    mat[i-1,3] = trajectories[i].position[0] - trajectories[j].position[0]

B = np.zeros((n,))
for i in range(1,5):
    B[i - 1] = trajectories[j].position[2] * trajectories[j].velocity[0] - trajectories[i].position[2] * \
                     trajectories[i].velocity[0] + trajectories[i].position[0] * trajectories[i].velocity[2] - \
                     trajectories[j].position[0] * trajectories[j].velocity[2]

x,z = np.dot(np.linalg.inv(mat), B)[0:2]
round(x+y+z)