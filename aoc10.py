import heapq
import numpy as np

with open('aoc10.txt') as f:
    lines = [line for line in f]

graph = {}
for i in range(len(lines)):
    for j in range(len(lines[i]) - 1):
        graph[(i, j)] = []
        if lines[i][j] == '|':
            if i - 1 >= 0:
                graph[(i, j)].append((i - 1, j))
            if i + 1 < len(lines):
                graph[(i, j)].append((i + 1, j))
        elif lines[i][j] == '-':
            if j - 1 >= 0:
                graph[(i, j)].append((i, j - 1))
            if j + 1 < len(lines[i]) - 1:
                graph[(i, j)].append((i, j + 1))
        elif lines[i][j] == 'L':
            if i - 1 >= 0:
                graph[(i, j)].append((i - 1, j))
            if j + 1 < len(lines[i]) - 1:
                graph[(i, j)].append((i, j + 1))
        elif lines[i][j] == 'J':
            if i - 1 >= 0:
                graph[(i, j)].append((i - 1, j))
            if j - 1 >= 0:
                graph[(i, j)].append((i, j - 1))
        elif lines[i][j] == 'F':
            if i + 1 < len(lines):
                graph[(i, j)].append((i + 1, j))
            if j + 1 < len(lines[i]) - 1:
                graph[(i, j)].append((i, j + 1))
        elif lines[i][j] == '7':
            if i + 1 < len(lines):
                graph[(i, j)].append((i + 1, j))
            if j - 1 >= 0:
                graph[(i, j)].append((i, j - 1))
        elif lines[i][j] == 'S':
            spos = (i, j)

for i in range(max(0, spos[0] - 1), spos[0] + 2):
    for j in range(max(0, spos[1] - 1), spos[1] + 2):
        if spos in graph[(i, j)]:
            graph[spos].append((i, j))

distances = {k: np.Inf for k in graph.keys()}

neighbours = []
heapq.heappush(neighbours, (0, spos))

current_graph = []

while len(neighbours) > 0:
    d, next = heapq.heappop(neighbours)
    for nnext in graph[next]:
        d_nnext = distances[nnext]
        if d + 1 < distances[nnext]:
            distances[nnext] = d + 1
        if nnext not in current_graph:
            heapq.heappush(neighbours, (distances[nnext], nnext))
    current_graph.append(next)

max(x for x in distances.values() if x < np.Inf)
# This is a Disjktra algo, overkill... didn't see it was a simple loop at first.

# part 2
# everytime we cross a portion of the loop that does not do a U turn (e.g L--J) we increment a counter. Only tiles having an odd counter value are inside the loop.

enclosed = []

for i in range(len(lines)):
    cross_counter = 0
    current_curve_direction = 0
    for j in range(len(lines[i]) - 1):
        if (i, j) in current_graph:
            if j == 0 or (i, j - 1) not in graph[(i, j)]:
                cross_counter += current_curve_direction != 0
                current_curve_direction = 0
            if lines[i][j] in ('L', '|', '7'):
                current_curve_direction -= 1
            elif lines[i][j] in ('F', 'J'):
                current_curve_direction += 1

        else:
            if current_curve_direction != 0:
                cross_counter += 1
                current_curve_direction = 0

            if cross_counter % 2 == 1:  # we are inside
                enclosed.append((i, j))

len(enclosed)
