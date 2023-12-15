from random import randint

with open('aoc5.txt') as f:
    lines = [line for line in f]

seeds = [int(x) for x in lines[0][:-1].split(':')[1].split(' ') if x != '']

maps = {}
mapping_order = []

for l in lines[1:]:
    if len(l) == 1:
        map_name = ''
    else:
        if map_name == '':
            map_name = l.split(' map:')[0]
            maps[map_name] = []
            mapping_order.append(map_name)
        else:
            maps[map_name].append([int(x) for x in l[:-1].split(' ') if x != ''])


def parse_rule(x, rule):
    if x in range(rule[1], rule[1] + rule[2]):
        return rule[0] + x - rule[1]
    return x


def get_location(s):
    current = s
    for mapping in mapping_order:
        hasbeen_transformed = False
        for rule in maps[mapping]:
            if not hasbeen_transformed:
                t = parse_rule(current, rule)
                hasbeen_transformed = t != current
            current = t
    return current


locations = [get_location(s) for s in seeds]
min_locs = min(locations)
min_locs

# part2: we do a probabilistic search starting from candidate minimal values and trace them back to on of the initial seeds in the given ranges.
# each time we have a hit we update our best candidate for minimal value

seed_ranges = [range(seeds[2 * i], seeds[2 * i] + seeds[2 * i + 1]) for i in range(len(seeds) // 2)]


def parse_rule_reverse(x, rule):
    if x in range(rule[0], rule[0] + rule[2]):
        return rule[1] + x - rule[0]
    return x


def get_seed(loc):
    current = loc
    mo = [x for x in mapping_order]
    mo.reverse()
    for mapping in mo:
        hasbeen_transformed = False
        for rule in maps[mapping]:
            if not hasbeen_transformed:
                t = parse_rule_reverse(current, rule)
                hasbeen_transformed = t != current
        current = t
    return current


upper_min = min_locs

exit_counter = 0
while exit_counter <= 1e5:
    close_or_far = randint(0,
                           1)  # we bias the sampling toward close candidates because the function is locally continuous
    test_val = randint(0, upper_min - 1) * close_or_far + randint(max(0, upper_min - 100), upper_min - 1) * (
                1 - close_or_far)

    s = get_seed(test_val)
    if any(s in r for r in seed_ranges):
        print(f'match at {test_val}')
        upper_min = test_val
        exit_counter = 0
    else:
        exit_counter += 1

upper_min
