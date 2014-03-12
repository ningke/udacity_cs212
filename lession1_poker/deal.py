# -----------
# User Instructions
# 
# Write a function, deal(numhands, n=5, deck), that 
# deals numhands hands with n cards each.
#

import random # this will be a useful library for shuffling

# This builds a deck of 52 cards. If you are unfamiliar
# with this notation, check out Andy's supplemental video
# on list comprehensions (you can find the link in the 
# Instructor Comments box below).

mydeck = [r+s for r in '23456789TJQKA' for s in 'SHDC'] 

def deal(numhands, n=5, deck=mydeck):
    # shuffle deck
    shuffled = []
    d = deck[:]
    while len(d) > 0:
        idx = random.randint(0, len(d)-1)
        shuffled.append(d.pop(idx))
    assert len(d) == 0
    assert len(shuffled) == 52
    assert sorted(shuffled) == sorted(deck)
    # now distribute cards from shuffuled deck
    hands = [[] for i in range(0, numhands)]
    for i in range(0, n):
        for j in range(0, numhands):
            hands[j].append(shuffled.pop(-1))
    return hands


if __name__ == "__main__":
    print deal(3, 5)
