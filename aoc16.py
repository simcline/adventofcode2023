import time
import numpy as np

with open('aoc16.txt') as f:
    lines = [line[:-1] if line.endswith('\n') else line for line in f]

nrows = len(lines)
ncols = len(lines[0])


def get_energy(init):
    beams = [init]  # i,j, i before j before

    marked = np.zeros((nrows, ncols))
    marked[init[0], init[1]] = 1

    past_events = []

    start = time.time()
    while len(beams):
        to_destruct = []
        to_add = []
        for k, b in enumerate(beams):
            if b in past_events:
                to_destruct.append(b)
            else:
                i, j, i_old, j_old = b
                d_j = j - j_old
                d_i = i - i_old
                match lines[i][j]:
                    case '.':
                        if i + d_i >= nrows or i + d_i < 0 or j + d_j >= ncols or j + d_j < 0:
                            to_destruct.append(b)
                        else:
                            beams[k] = (i + d_i, j + d_j, i, j)
                            marked[i + d_i, j + d_j] = 1
                    case '|':
                        if d_j != 0:
                            if i + 1 < nrows:
                                to_add.append((i + 1, j, i, j))
                                marked[i + 1, j] = 1
                            if i - 1 >= 0:
                                to_add.append((i - 1, j, i, j))
                                marked[i - 1, j] = 1
                            to_destruct.append(b)
                        else:
                            if i + d_i >= nrows or i + d_i < 0 or j + d_j >= ncols or j + d_j < 0:
                                to_destruct.append(b)
                            else:
                                beams[k] = (i + d_i, j + d_j, i, j)
                                marked[i + d_i, j + d_j] = 1
                    case '-':
                        if d_i != 0:
                            if j + 1 < ncols:
                                to_add.append((i, j + 1, i, j))
                                marked[i, j + 1] = 1
                            if j - 1 >= 0:
                                to_add.append((i, j - 1, i, j))
                                marked[i, j - 1] = 1
                            to_destruct.append(b)
                        else:
                            if i + d_i >= nrows or i + d_i < 0 or j + d_j >= ncols or j + d_j < 0:
                                to_destruct.append(b)
                            else:
                                beams[k] = (i + d_i, j + d_j, i, j)
                                marked[i + d_i, j + d_j] = 1
                    case '/':
                        if d_i > 0:
                            if j - 1 >= 0:
                                beams[k] = (i, j - 1, i, j)
                                marked[i, j - 1] = 1
                            else:
                                to_destruct.append(b)
                        elif d_i < 0:
                            if j + 1 < ncols:
                                beams[k] = (i, j + 1, i, j)
                                marked[i, j + 1] = 1
                            else:
                                to_destruct.append(b)
                        elif d_j > 0:
                            if i - 1 >= 0:
                                beams[k] = (i - 1, j, i, j)
                                marked[i - 1, j] = 1
                            else:
                                to_destruct.append(b)
                        else:
                            if i + 1 < nrows:
                                beams[k] = (i + 1, j, i, j)
                                marked[i + 1, j] = 1
                            else:
                                to_destruct.append(b)
                    case '\\':
                        if d_i > 0:
                            if j + 1 < ncols:
                                beams[k] = (i, j + 1, i, j)
                                marked[i, j + 1] = 1
                            else:
                                to_destruct.append(b)
                        elif d_i < 0:
                            if j - 1 >= 0:
                                beams[k] = (i, j - 1, i, j)
                                marked[i, j - 1] = 1
                            else:
                                to_destruct.append(b)
                        elif d_j > 0:
                            if i + 1 < nrows:
                                beams[k] = (i + 1, j, i, j)
                                marked[i + 1, j] = 1
                            else:
                                to_destruct.append(b)
                        else:
                            if i - 1 >= 0:
                                beams[k] = (i - 1, j, i, j)
                                marked[i - 1, j] = 1
                            else:
                                to_destruct.append(b)
            past_events.append(b)
        for d in to_destruct:
            beams.remove(d)
        beams += to_add

    print(f'{init} event computed in {time.time() - start} seconds')
    return int(sum(sum(marked[i, :]) for i in range(nrows)))


get_energy((0, 0, 0, -1))
# part 2

init_events = []

for i in range(nrows):
    init_events.append((i, 0, i, -1))
    init_events.append((i, ncols - 1, i, ncols))

for j in range(ncols):
    init_events.append((0, j, -1, j))
    init_events.append((nrows - 1, j, nrows, j))

energies = [get_energy(init) for init in init_events]
max(energies)
