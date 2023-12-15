import numpy as np

with open('aoc13.txt') as f:
    lines = [line[:-1] if line.endswith('\n') else line for line in f]

matrices = []
current = []
for i in range(len(lines)):
    if lines[i] != '' and i != len(lines) - 1:
        current.append(lines[i])
    else:
        m = np.zeros((len(current), len(current[0])))
        for j in range(len(current)):
            for k in range(len(current[j])):
                if current[j][k] == '#':
                    m[j, k] = 1
        matrices.append(m)
        current = []


def find_vertical_symmetries(m):
    m2 = m[:, ::-1]
    for j in range(1, m.shape[1] // 2 + 1):
        if all(all(x == y) for x, y in zip(m[:, :j], m[:, j:(2 * j)][:, ::-1])):
            return j
        if all(all(x == y) for x, y in zip(m2[:, :j], m2[:, j:(2 * j)][:, ::-1])):
            return m.shape[1] - j
    return 0


def find_horizontal_symmetries(m):
    m2 = m[::-1, :]
    for j in range(1, m.shape[0] // 2 + 1):
        if all(all(x == y) for x, y in zip(m[:j, :], m[j:(2 * j), :][::-1, :])):
            return j
        if all(all(x == y) for x, y in zip(m2[:j, :], m2[j:(2 * j), :][::-1, :])):
            return m.shape[0] - j
    return 0


sum(find_vertical_symmetries(m) + 100 * find_horizontal_symmetries(m) for m in matrices)


# part 2
def find_almost_vertical_symmetries(m):
    m2 = m[:, ::-1]
    for j in range(1, m.shape[1] // 2 + 1):
        if sum(sum(x != y) for x, y in zip(m[:, :j], m[:, j:(2 * j)][:, ::-1])) == 1:
            return j
        if sum(sum(x != y) for x, y in zip(m2[:, :j], m2[:, j:(2 * j)][:, ::-1])) == 1:
            return m.shape[1] - j
    return 0


def find_almost_horizontal_symmetries(m):
    m2 = m[::-1, :]
    for j in range(1, m.shape[0] // 2 + 1):
        if sum(sum(x != y) for x, y in zip(m[:j, :], m[j:(2 * j), :][::-1, :])) == 1:
            return j
        if sum(sum(x != y) for x, y in zip(m2[:j, :], m2[j:(2 * j), :][::-1, :])) == 1:
            return m.shape[0] - j
    return 0


sum(find_almost_vertical_symmetries(m) + 100 * find_almost_horizontal_symmetries(m) for m in matrices)
