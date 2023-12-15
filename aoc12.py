from functools import reduce, lru_cache
import time

with open('aoc12.txt') as f:
    lines = [line[:-1] if line.endswith('\n') else line for line in f]

patterns = []
rules = []

for l in lines:
    p, r = l.split(' ')
    patterns.append(p)
    rules.append([int(x) for x in r.split(',') if x != ''])


@lru_cache(maxsize=None)
def get_num_combinations(p, r):
    if len(r) == 0:
        return int(all(c != '#' for c in p))
    if all(c == '#' for c in p):
        if len(r) > 1:
            return 0
        else:
            return int(r[0] == len(p))
    if len(p) == 1:
        if p == '.' and len(r) > 0:
            return 0
        if p == '?' and len(r) > 1:
            return 0
        if p == '?' and len(r) == 1:
            return int(r[0] in [0, 1])
    if sum(x for x in r) > len([c for c in p if c != '.']):
        return 0
    if 2 * len(r) - 1 > len(p):
        return 0
    else:
        idxs = [0] + reduce(lambda x, y: x + y, [[i, -i] for i in range(1, len(p) // 2 + 2)])
        for k in idxs:
            id = min(len(p) // 2 + 1 + k, len(p) - 1)
            if id == 0:
                if p[id] == '.':
                    return get_num_combinations(p[1:], r)
                if p[id] == '?':
                    return get_num_combinations(p[1:], r) + get_num_combinations('#' + p[1:], r)
            if id == len(p) - 1:
                if p[id] == '.':
                    return get_num_combinations(p[:-1], r)
                if p[id] == '?':
                    return get_num_combinations(p[:-1], r) + get_num_combinations(p[:-1] + '#', r)
            else:
                if p[id] == '.':
                    return sum(get_num_combinations(p[:id], r[:i]) * get_num_combinations(p[id + 1:], r[i:]) for i in
                               range(len(r) + 1))
                if p[id] == '?':
                    return sum(get_num_combinations(p[:id], r[:i]) * get_num_combinations(p[id + 1:], r[i:]) for i in
                               range(len(r) + 1)) + get_num_combinations(p[:id] + '#' + p[id + 1:], r)
    print(p, r)


def get_total_cmb(patterns, rules):
    n = 0
    for i in range(0, len(patterns)):
        t = time.time()
        num = get_num_combinations(patterns[i], tuple(rules[i]))
        print(f'step {i} took {time.time() - t} seconds')
        n += num
    return n


get_total_cmb(patterns, rules)

##part 2
patterns2 = [''.join([p + '?'] * 5)[:-1] for p in patterns]
rules2 = [r * 5 for r in rules]

get_total_cmb(patterns2, rules2)
