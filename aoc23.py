import time

with open('aoc23.txt') as f:
    lines = [line[:-1] if line.endswith('\n') else line for line in f]

nrows, ncols = len(lines), len(lines[0])
start = 0, [j for j in range(ncols) if lines[0][j] == '.'][0]
end = nrows - 1, [j for j in range(ncols) if lines[nrows - 1][j] == '.'][0]

def get_next_moves(pos):
    i, j = pos
    match lines[i][j]:
        case '>':
            return [(i, j + 1)]
        case '<':
            return [(i, j - 1)]
        case 'v':
            return [(i + 1, j)]
        case '^':
            return [(i - 1, j)]

    ret = []
    if i < nrows - 1 and lines[i + 1][j] in ('.', 'v'):
        ret.append((i + 1, j))
    if i > 0 and lines[i - 1][j] in ('.', '^'):
        ret.append((i - 1, j))
    if j < ncols - 1 and lines[i][j + 1] in ('.', '>'):
        ret.append((i, j + 1))
    if j > 0 and lines[i][j - 1] in ('.', '<'):
        ret.append((i, j - 1))
    return ret


paths = [[start]]
finished_paths = []

while len(paths):
    if len(paths) % 20 == 0:
        print(f'possible cadidates paths: {len(paths)}')
    to_remove = []
    to_add = []
    for p in paths:
        if p[-1] == end:
            finished_paths.append(p)
            to_remove.append(p)
        else:
            nm = [q for q in get_next_moves(p[-1]) if q not in p]
            match len(nm):
                case 0:
                    to_remove.append(p)
                case 1:
                    p.append(nm[0])
                case x if x > 1:
                    to_remove.append(p)
                    to_add.extend([p + [q] for q in nm])
    for r in to_remove:
        paths.remove(r)
    paths.extend(to_add)

max(len(p) - 1 for p in finished_paths)


## part 2
class Path:

    def __init__(self, head, lasthead=None, crossroads=None, length=0):
        self.head = head
        self.lasthead = lasthead
        self.crossroads = [] if crossroads is None else crossroads
        self.length = length

    @classmethod
    def clone(cls, path):
        return cls(path.head, path.lasthead, path.crossroads.copy(), path.length)

    def pushHead(self, head, saveLastHead=False, length=1):
        if saveLastHead:
            self.crossroads.append(self.lasthead)
        self.lasthead = self.head
        self.head = head
        self.length += length
        return self

    def __len__(self):
        return self.length

    def __contains__(self, item):
        return item in self.crossroads or item in (self.head, self.lasthead)

    def __repr__(self):
        return f'length {len(self)}: {"->".join([f"({x[0]},{x[1]})" for x in self.crossroads + [self.lasthead, self.head] if x is not None])}'


def get_next_moves2(pos):
    i, j = pos
    ret = []
    if i < nrows - 1 and lines[i + 1][j] != '#':
        ret.append((i + 1, j))
    if i > 0 and lines[i - 1][j] != '#':
        ret.append((i - 1, j))
    if j < ncols - 1 and lines[i][j + 1] != '#':
        ret.append((i, j + 1))
    if j > 0 and lines[i][j - 1] != '#':
        ret.append((i, j - 1))
    return ret


def find_neighbours(pos):
    nm = get_next_moves2(pos)
    neighb = []
    to_remove = []

    if len(nm):
        paths = [Path(pos).pushHead(q) for q in nm]
        while len(paths):
            for p in paths:
                nmp = get_next_moves2(p.head)
                if len(nmp) > 2 or p.head in (start, end):
                    neighb.append((p.head, len(p)))
                    to_remove.append(p)
                else:
                    p.pushHead([q for q in nmp if q not in p][0])
            for r in to_remove:
                if r in paths:
                    paths.remove(r)

    return neighb


def check_connected_to_end(pos, barriers):
    cc = set()
    frontier = {pos}

    while len(frontier):
        to_add = set()
        to_remove = set()
        for f in frontier:
            if f == end:
                return True
            nm = {q[0] for q in graph[f] if q[0] not in frontier and q[0] not in cc and q[0] not in barriers}
            if len(nm):
                to_add |= nm
            else:
                to_remove.add(f)
                cc.add(f)
        frontier -= to_remove
        frontier |= to_add
    return False


def build_graph():
    d = {}
    visited = set()
    frontier = {start}

    while len(frontier):
        to_add = set()
        to_remove = set()

        for f in frontier:
            visited.add(f)
            d[f] = find_neighbours(f)
            to_remove.add(f)
            for v in d[f]:
                if v[0] not in visited:
                    to_add.add(v[0])
        frontier -= to_remove
        frontier |= to_add
    return d


graph = build_graph()
starttime = time.time()

def compute_longest_path(p):
    if p.head == end:
        return len(p)
    else:
        nm = [q for q in graph[p.head] if
              q[0] not in p and check_connected_to_end(q[0], p.crossroads + [p.head, p.lasthead])]
        if len(nm):
            return max([compute_longest_path(Path.clone(p).pushHead(q[0], saveLastHead=True, length=q[1])) for q in nm])
    return 0


lp = compute_longest_path(Path(head=start))
print(f'finished search after {int(time.time() - starttime)} seconds, best length is {lp} steps!')
