from functools import reduce

with open('aoc19.txt') as f:
    lines = [line[:-1] if line.endswith('\n') else line for line in f if line != '\n']

rules = {l.split('{')[0]: l.split('{')[1][:-1].split(',') for l in lines if not l.startswith('{x')}
items = [{keyval.split('=')[0]: int(keyval.split('=')[1]) for keyval in l[1:-1].split(',')} for l in lines if
         l.startswith('{x')]


def parse_rule(it, r):
    if '>' not in r and '<' not in r:
        return r
    ret = 'N'  # next
    if r[1] == '>':
        v, dest = r.split('>')[1].split(':')
        if it[r[0]] > int(v):
            ret = dest
    else:
        v, dest = r.split('<')[1].split(':')
        if it[r[0]] < int(v):
            ret = dest
    return ret


def parse_rule_list(it, rl, rules):
    for r in rl:
        ret = parse_rule(it, r)
        match ret:
            case 'A':
                return True
            case 'R':
                return False
            case 'N':
                pass
            case _:
                return parse_rule_list(it, rules[ret], rules)


def parse_item(x):
    return parse_rule_list(x, rules['in'], rules)


acc = [x for x in items if parse_item(x)]
sum(sum(x.values()) for x in acc)

# part2
dico = {'x': 0, 'm': 1, 'a': 2, 's': 3}


def get_possib(poss):
    return reduce(lambda x, y: x * y, [p[1] - p[0] + 1 for p in poss])


def parse(poss, rl, rules):
    if get_possib(poss) == 0:
        return 0

    match rl[0]:
        case 'A':
            return get_possib(poss)
        case 'R':
            return 0
        case x if '<' in x:
            v, dest = rl[0].split('<')[1].split(':')
            v = int(v)
            new_poss_left = [poss[i] if i != dico[rl[0][0]] else (min(poss[i][0], v - 1), min(poss[i][1], v - 1)) for i
                             in range(len(poss))]
            new_poss_right = [poss[i] if i != dico[rl[0][0]] else (max(poss[i][0], v), max(poss[i][1], v)) for i in
                              range(len(poss))]
        case x if '>' in x:
            v, dest = rl[0].split('>')[1].split(':')
            v = int(v)
            new_poss_left = [poss[i] if i != dico[rl[0][0]] else (max(poss[i][0], v + 1), max(poss[i][1], v + 1)) for i
                             in
                             range(len(poss))]
            new_poss_right = [poss[i] if i != dico[rl[0][0]] else (min(poss[i][0], v), min(poss[i][1], v)) for i in
                              range(len(poss))]
        case x if '>' not in x and '<' not in x:
            return parse(poss, rules[rl[0]], rules)
    return parse(new_poss_left, rules[dest], rules) + parse(new_poss_right, rl[1:], rules)


rules['A'] = ['A']
rules['R'] = ['R']
poss = [(1, 4000), (1, 4000), (1, 4000), (1, 4000)]
parse(poss, rules['in'], rules)
