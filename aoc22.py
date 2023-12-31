with open('aoc22.txt') as f:
    lines = [line[:-1] if line.endswith('\n') else line for line in f]





class Brick:

    def __init__(self, line=None):
        if line is not None:
            self.name = ""
            l, r = line.split('~')
            self.start = [int(x) for x in l.split(',')]
            self.end = [int(x) for x in r.split(',')]

        self.bricksbelow = []
        self.bricksabove = []

    @classmethod
    def fromStartEnd(cls, start, end):
        inst = cls()
        inst.start = start
        inst.end = end
        return inst

    def getMinZ(self):
        return min(self.start[2], self.end[2])

    def getMaxZ(self):
        return max(self.start[2], self.end[2])

    def intersects(self, axis, other):
        se = range(self.start[axis], self.end[axis] + 1)
        seo = range(other.start[axis], other.end[axis] + 1)
        return other.start[axis] in se or other.end[axis] in se or self.start[axis] in seo or self.end[axis] in seo

    def intersects_XY(self, other):
        return self.intersects(0, other) and self.intersects(1, other)

    def moveZStartTo(self, z):
        delta_z = z - self.start[2]
        self.start[2] = z
        self.end[2] += delta_z

    def canBeDisintegrated(self):
        return all(len(bricks[j].bricksbelow) > 1 for j in self.bricksabove)

    def setName(self, name):
        self.name = name

    def resetAboveBelow(self):
        self.bricksabove = []
        self.bricksbelow = []

    def __deepcopy__(self):
        ret = Brick.fromStartEnd(self.start.copy(), self.end.copy())
        ret.setName(self.name)
        return ret

    def __lt__(self, other):
        return self.getMinZ() < other.getMinZ()

    def __repr__(self):
        return f'{self.name}; x: {self.start[0]} -> {self.end[0]} | y: {self.start[1]} -> {self.end[1]} | z: {self.start[2]} -> {self.end[2]} | above: {",".join([str(i) for i in self.bricksabove])} | below:  {",".join([str(i) for i in self.bricksbelow])}'


bricks = [Brick(l) for l in lines]


def sort_and_make_fall_and_link(bricks):
    bricks.sort()
    for b in bricks:
        b.resetAboveBelow()

    for i in range(len(bricks)):
        bricks[i].setName(str(i))
        lowest_reachable_z = 1
        supports_candidates = []
        for j in range(i):
            if bricks[i].intersects_XY(bricks[j]):
                if bricks[j].getMaxZ() + 1 == lowest_reachable_z:
                    supports_candidates.append(j)
                elif bricks[j].getMaxZ() + 1 > lowest_reachable_z:
                    lowest_reachable_z = bricks[j].getMaxZ() + 1
                    supports_candidates = [j]
        bricks[i].moveZStartTo(lowest_reachable_z)
        bricks[i].bricksbelow = supports_candidates
        for k in supports_candidates:
            bricks[k].bricksabove.append(i)


sort_and_make_fall_and_link(bricks)
len([b for b in bricks if b.canBeDisintegrated()])


# part 2
def compute_number_fall(i0, bricks0):
    print(f'removing brick {i0}')
    n = 0
    bricks = [b.__deepcopy__() for b in bricks0]

    for i in range(i0 + 1, len(bricks)):
        lowest_reachable_z = 1
        supports_candidates = []
        for j in range(i):
            if j != i0:
                if bricks[i].intersects_XY(bricks[j]):
                    if bricks[j].getMaxZ() + 1 == lowest_reachable_z:
                        supports_candidates.append(j)
                    elif bricks[j].getMaxZ() + 1 > lowest_reachable_z:
                        lowest_reachable_z = bricks[j].getMaxZ() + 1
                        supports_candidates = [j]
        if lowest_reachable_z < bricks[i].getMinZ():
            n += 1
        bricks[i].moveZStartTo(lowest_reachable_z)
        bricks[i].bricksbelow = supports_candidates
        for k in supports_candidates:
            bricks[k].bricksabove.append(i)
    return n


sort_and_make_fall_and_link(bricks)
sum(compute_number_fall(i, bricks) for i in range(len(bricks)) if not bricks[i].canBeDisintegrated())
