with open('aoc1.txt') as f:
    lines = [line for line in f]


def parseline(line):
    first = -1
    last = -1
    for x in line:
        if x.isnumeric():
            first = first if first > 0 else int(x)
            last = x
    if first == -1:
        return 0
    return int(str(first) + str(last))


sum(parseline(l) for l in lines)


## part 2

def parseline2(line):
    patterns = [str(x) for x in range(10)] + ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',
                                              'nine']
    firstocc = [line.find(x) for x in patterns]
    firstocc = [x if x != -1 else len(line) + 1 for x in firstocc]
    lastocc = [line.rfind(x) for x in patterns]
    values = [x for x in range(10)] * 2

    first = len(line) + 1
    first_idx = -1
    last = -1
    last_idx = -1
    for i in range(len(patterns)):
        if firstocc[i] < first:
            first = firstocc[i]
            first_idx = i
        if lastocc[i] > last:
            last = lastocc[i]
            last_idx = i
    return int(str(values[first_idx]) + str(values[last_idx]))


sum(parseline2(l) for l in lines)
