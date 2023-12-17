import numpy as np

with open('aoc17.txt') as f:
    lines = [line[:-1] if line.endswith('\n') else line for line in f]


def solve(minmove, maxmove):
    nrows = len(lines)
    ncols = len(lines[0])

    final_state = (nrows, ncols - 1, '', 0)
    init_state = (-1, 0, '', 0)
    states = [(i, j, d, k) for i in range(nrows) for j in range(ncols) for d in ['u', 'd', 'l', 'r'] for k in
              range(1, maxmove + 1)] + [final_state, init_state] + [(0, 0, d, 0) for d in ['d', 'r']]
    distances = {s: np.Inf for s in states}

    distances[init_state] = -int(lines[0][0])

    neighbours = {}
    neighbours[init_state] = distances[init_state]

    def find_minimal(neighbours):
        mn = np.Inf
        for s in neighbours:
            if neighbours[s] < mn:
                mn = neighbours[s]
                best = s
        del neighbours[best]
        return mn, best

    current_graph = set()

    def get_neighbours(state):
        if state == final_state:
            return []

        if state == init_state:
            return [(0, 0, d, 0) for d in ['d', 'r']]

        nhgb = []
        i, j, d, k = state
        if i == ncols - 1 and j == ncols - 1:
            nhgb += [final_state]

        match d:
            case 'u':
                if i > 0 and k < maxmove:
                    nhgb.append((i - 1, j, d, k + 1))
                if j >= minmove and k >= minmove:
                    nhgb.append((i, j - 1, 'l', 1))
                if j < ncols - minmove and k >= minmove:
                    nhgb.append((i, j + 1, 'r', 1))
            case 'd':
                if i < nrows - 1 and k < maxmove:
                    nhgb.append((i + 1, j, d, k + 1))
                if j >= minmove and k >= minmove:
                    nhgb.append((i, j - 1, 'l', 1))
                if j < ncols - minmove and k >= minmove:
                    nhgb.append((i, j + 1, 'r', 1))
            case 'l':
                if j > 0 and k < maxmove:
                    nhgb.append((i, j - 1, d, k + 1))
                if i >= minmove and k >= minmove:
                    nhgb.append((i - 1, j, 'u', 1))
                if i < nrows - minmove and k >= minmove:
                    nhgb.append((i + 1, j, 'd', 1))
            case 'r':
                if j < ncols - 1 and k < maxmove:
                    nhgb.append((i, j + 1, d, k + 1))
                if i >= minmove and k >= minmove:
                    nhgb.append((i - 1, j, 'u', 1))
                if i < nrows - minmove and k >= minmove:
                    nhgb.append((i + 1, j, 'd', 1))
        return nhgb

    ##Disjktra algo on the extended oriented graph
    while len(neighbours) > 0:
        if len(current_graph) % 10000 == 0:
            print(
                f'size of the explored graph {len(current_graph)}, total size is {len(states)}, neighbours in queue {len(neighbours)}')
        d, next = find_minimal(neighbours)
        for nnext in get_neighbours(next):
            if nnext == final_state:
                delta_dist = 0
            else:
                delta_dist = int(lines[nnext[0]][nnext[1]])
            if d + delta_dist < distances[nnext]:
                distances[nnext] = d + delta_dist
            if nnext not in current_graph:
                neighbours[nnext] = distances[nnext]
        current_graph.add(next)

    return distances[final_state]


solve(1, 3)
# part 2

solve(4, 10)
