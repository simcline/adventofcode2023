import numpy as np
from itertools import product

with open('aoc7.txt') as f:
    lines = [line for line in f]

class Hand:

    CARD_VALUES = {**{str(i):i for i in range(2,10)}, **{'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}}

    def __init__(self,cardlist):
        self.cardlist=cardlist
        self.type= self.compute_type()

    def _computegroups(self):
        self.groups={}
        for c in self.cardlist:
            if c in self.groups:
                self.groups[c]+=1
            else:
                self.groups[c]=1

    def compute_type(self):
        self._computegroups()
        contains2=False
        contains3=False
        for v in self.groups.values():
            if v in (4,5):
                return v+1
            elif v==3:
                if contains2:
                    return 4
                else:
                    contains3=True
            elif v==2:
                if contains3:
                    return 4
                elif contains2:
                    return 2
                else:
                    contains2=True
        if contains2:
            return 1
        if contains3:
            return 3
        return 0

    def get_type(self):
        types = ['HC', 'Pair', '2Pairs', '3ofakind', 'FH', '4ofakind', '5ofakind']
        return types[self.type]

    def __lt__(self, another):
        if self.type <another.type:
            return True
        elif self.type==another.type:
            for c1,c2 in zip(self.cardlist, another.cardlist):
                if self.CARD_VALUES[c1]< self.CARD_VALUES[c2]:
                    return True
                if self.CARD_VALUES[c1]>self.CARD_VALUES[c2]:
                    return False
        return False

raw_hands = [l[:-1].split(' ')[0] for l in lines]
bids = [int(l[:-1].split(' ')[1]) for l in lines]
hands = [Hand(t) for t in raw_hands]

idx = np.argsort(hands)

sorted=[hands[i].cardlist for i in idx]
sorted_bids=[bids[i] for i in idx]

sum((i+1)*sorted_bids[i] for i in range(len(sorted)))

#part 2

class Hand2:
    CARD_VALUES = {**{str(i): i for i in range(2, 10)}, **{'T': 10, 'J': 1, 'Q': 12, 'K': 13, 'A': 14}}

    def __init__(self,cardlist):
        self.cardlist=cardlist
        self.possible_hands=self.compute_possible_hands()
        self.type, self.besthand= self.compute_type_and_best_hand()

    def compute_possible_hands(self):
        baselist=[str(i) for i in range(2,10)]+['T','Q','K','A']
        to_enum= [[c] if c!='J' else baselist for c in self.cardlist]
        return [Hand(''.join(x)) for x in product(*to_enum)]

    def compute_type_and_best_hand(self):
        possible_types = [h.type for h in self.possible_hands]
        idx = np.argmax(possible_types)
        return possible_types[idx], self.possible_hands[idx]

    def get_type(self):
        types = ['HC', 'Pair', '2Pairs', '3ofakind', 'FH', '4ofakind', '5ofakind']
        return types[self.type]

    def __lt__(self, another):
        if self.type <another.type:
            return True
        elif self.type==another.type:
            for c1,c2 in zip(self.cardlist, another.cardlist):
                if self.CARD_VALUES[c1]< self.CARD_VALUES[c2]:
                    return True
                if self.CARD_VALUES[c1]>self.CARD_VALUES[c2]:
                    return False
        return False

hands2 = [Hand2(t) for t in raw_hands]

idx2 = np.argsort(hands2)

sorted = [hands2[i].cardlist for i in idx2]
sorted_bids = [bids[i] for i in idx2]

sum((i+1)*sorted_bids[i] for i in range(len(sorted)))