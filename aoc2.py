import re
import numpy as np

col_rules = {'red': 12, 'green': 13, 'blue': 14}

with open('aoc2.txt') as f:
    lines = [line for line in f]


def parse_game(line):
    head, body = re.split(': ', line)
    game_num = int(head.split('Game ')[1])
    rounds = re.split(';', body)

    colors_search = {c: [re.search(f'([0-9])+ {c}', r) for r in rounds] for c in col_rules}
    color_maxes = {c: max([int(x.group(0).split(f' {c}')[0]) if x is not None else 0 for x in colors_search[c]]) for c
                   in col_rules}
    return game_num*all(color_maxes[c] <= col_rules[c] for c in col_rules)


sum(parse_game(l) for l in lines)


# part 2
def parse_game2(line):
    head, body = re.split(': ', line)
    rounds = re.split(';', body)

    colors_search = {c: [re.search(f'([0-9])+ {c}', r) for r in rounds] for c in col_rules}
    color_maxes = {c: max([int(x.group(0).split(f' {c}')[0]) if x is not None else 0 for x in colors_search[c]]) for c
                   in col_rules}
    return np.prod([x for x in color_maxes.values()])


sum(parse_game2(l) for l in lines)
