import numpy as np
from random import sample
import itertools
from collections import defaultdict as ddict

# ## general idea: the three edges we are looking for appear in any path that connects two points from the two
# disconnected components, so if we sample at random pairs from the graph and look at any path that connects them,
# the frequency of appearance of these three edges should be higher than for other edges. This is heuristic but worked.

with open('aoc25.txt') as f:
    lines = [line[:-1] if line.endswith('\n') else line for line in f]

graph = ddict(set)
for l in lines:
    left, right = l.split(': ')
    for r in right.split(' '):
        graph[left].add(r)
        graph[r].add(left)

def connected_component(g,graph):
    cc = set()
    frontier = {g}
    while len(frontier):
        to_add = set()
        to_remove = set()
        for c in frontier:
            for neighb in graph[c]:
                if neighb not in frontier and neighb not in cc:
                    to_add.add(neighb)
            to_remove.add(c)
            cc.add(c)
        frontier -= to_remove
        frontier |= to_add
    return cc

def delete_edge(g1, g2, graph):
    if g2 in graph[g1]:
        graph[g1].remove(g2)
    if g1 in graph[g2]:
        graph[g2].remove(g1)

def get_ccs(graph):
    answ = []
    while len(graph):
        g = graph.keys().__iter__().__next__()
        answ.append(connected_component(g,graph))
        to_delete = set()
        for c in graph:
            if c in answ[-1]:
                to_delete.add(c)
        for c in to_delete:
            del graph[c]
    return answ

def find_path(start,end):
    """"dijsktra between start and end"""

    current_graph = set()
    neighbours = {}
    distances = {s: np.Inf for s in graph}
    distances[start] = 0
    neighbours[start] = distances[start]

    while len(neighbours):
        next, d = min(neighbours.items(), key = lambda x: neighbours[x[0]])
        if next in neighbours: del neighbours[next]
        for nnext in graph[next]:
            distances[nnext] = min(distances[nnext], d + 1)
            if nnext not in current_graph:
                neighbours[nnext] = distances[nnext]
        current_graph.add(next)

    path = []
    dist = distances[end]
    current = end
    while dist:
        for g in graph[current]:
            if distances[g] == dist-1:
                path.append(g)
                current = g
                dist -= 1
                break

    path.reverse()
    return path

vertices = list(graph)
n = 500
freqs = {(v1,v2):0 for v1,v2 in itertools.combinations(vertices,2)}

for i in range(n):
    s = sample(vertices,2)
    path = find_path(s[0],s[1])
    for p1,p2 in itertools.pairwise(path):
        if (p1,p2) in freqs:
            freqs[(p1,p2)]+=1
        else:
            freqs[(p2,p1)]+=1

bests=[]
for i in range(3):
    bests.append(max(freqs, key = lambda x:freqs[x] if x not in bests else -1))

for i in range(3):
    delete_edge(*bests[i], graph)
ccs = get_ccs(graph)
len(ccs[0]) * len(ccs[1])