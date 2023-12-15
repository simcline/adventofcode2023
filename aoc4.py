with open('aoc4.txt') as f:
    lines = [line for line in f]

res = 0
for l in lines:
    winning, have = l.split(':')[1].split('|')
    winning = [int(x) for x in winning.split(' ') if x != '']
    have = [int(x) for x in have[:-1].split(' ') if x != '']
    matches = 0
    for h in have:
        if h in winning:
            matches += 1
    res += 2 ** (matches - 1) if matches > 0 else 0
res

# part 2
card_list = [1] * len(lines)
for i in range(len(lines)):
    winning, have = lines[i].split(':')[1].split('|')
    winning = [int(x) for x in winning.split(' ') if x != '']
    have = [int(x) for x in have[:-1].split(' ') if x != '']
    matches = 0
    for h in have:
        if h in winning:
            matches += 1
    if matches > 0:
        for k in range(1, matches + 1):
            if i + k <= len(lines) - 1:
                card_list[i + k] += card_list[i]
sum(card_list)
