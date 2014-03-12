# CS 212, hw1-1: 7-card stud
#
# -----------------
# User Instructions
#
# Write a function best_hand(hand) that takes a seven
# card hand as input and returns the best possible 5
# card hand. The itertools library has some functions
# that may help you solve this problem.
#
# -----------------
# Grading Notes
# 
# Muliple correct answers will be accepted in cases 
# where the best hand is ambiguous (for example, if 
# you have 4 kings and 3 queens, there are three best
# hands: 4 kings along with any of the three queens).

import itertools

def best_hand(hand):
    "From a 7-card hand, return the best 5 card hand."
    # Each item in mhand is a two-tuple of (rank, card)
    def rank(r):
        return '--23456789TJQKA'.index(r)
    mhand = [(rank(card[0]), card) for card in hand]
    ranks= [item[0] for item in mhand]
    # fix the straight with 'A'
    if set([14, 5, 4, 3, 2]) <= set(ranks):
        for i, mh in enumerate(mhand):
            if mh[0] == 14:
                mhand[i] = (1, mh[1])
                break
    # sort by rank
    mhand.sort(key=lambda x: x[0], reverse=True)
    ranks= [item[0] for item in mhand]
    #print 'mhand >>>', mhand
    #print 'ranks >>>', ranks
    def flush_hand(mhd):
        ''' returns the flush hand if any. '''
        s = [[], [], [], []]
        for c in mhd:
            idx = "HDSC".index(c[1][1])
            s[idx].append(c)
        s.sort(key=lambda x: len(x), reverse=True)
        return s[0] if len(s[0]) >= 5 else []
    #print 'flush >>>', flush_hand(mhand)
    def straight_hand(mhd, rks):
        ''' Returns all straight hands. '''
        return [mhd[i:i+5] for i in range(0, 3) if (
                len(set(rks[i:i+5])) == 5 and rks[i] - rks[i+4] == 4)]
    #print 'straight >>>', straight_hand(mhand, ranks)
    def straight_flush(shands, fh):
        ''' Returns the first (highest) straight flush hand. '''
        if shands and fh:
            for s in shands:
                if set(s) <= set(fh):
                    return s
        return []
    def kinds(mhd):
        ''' Returns a list of list of cards of the same rank, sorted by
        highest number of cards in each group. '''
        groups = [list(g) for k, g in itertools.groupby(
                mhd,key=lambda x: x[0])]
        groups.sort(key=lambda g: len(g), reverse=True)
        return groups
    def ohand(mhd):
        #print "Best Hand is: ", [c[1] for c in mhd]
        return [c[1] for c in mhd]
    def top5(groups):
        return list(itertools.chain(*groups))[:5]
    shands = straight_hand(mhand, ranks)
    fh = flush_hand(mhand)
    sfh = straight_flush(shands, fh)
    groups = kinds(mhand)
    counts = tuple(len(g) for g in groups)
    return (
        ohand(sfh) if sfh else # straight flush
        ohand(groups[0][:4] + [max(itertools.chain(groups[0][4:], *groups[1:]), key=lambda c: c[0])]) \
            if counts[0] >= 4 else # 4 of a kind
        ohand(list(itertools.chain(groups[0], groups[1]))) \
            if counts[:2] == (3, 2) else # full house
        ohand(fh[:5]) if fh else # flush
        ohand(shands[0]) if shands else # straight
        ohand(top5(groups)) if counts[0] == 3 else # 3 of a kind
        ohand(top5(groups)) if counts[:2] == (2, 2) else # two pairs
        ohand(top5(groups)) if counts[0] == 2 else # 2 of a kind
        ohand(top5(groups)) # nothing
        )

# ------------------
# Provided Functions
# 
# You may want to use some of the functions which
# you have already defined in the unit to write 
# your best_hand function.

def hand_rank(hand):
    "Return a value indicating the ranking of a hand."
    ranks = card_ranks(hand) 
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks)
    
def card_ranks(hand):
    "Return a list of the ranks, sorted with higher first."
    ranks = ['--23456789TJQKA'.index(r) for r, s in hand]
    ranks.sort(reverse = True)
    return [5, 4, 3, 2, 1] if (ranks == [14, 5, 4, 3, 2]) else ranks

def flush(hand):
    "Return True if all the cards have the same suit."
    suits = [s for r,s in hand]
    return len(set(suits)) == 1

def straight(ranks):
    """Return True if the ordered 
    ranks form a 5-card straight."""
    return (max(ranks)-min(ranks) == 4) and len(set(ranks)) == 5

def kind(n, ranks):
    """Return the first rank that this hand has 
    exactly n-of-a-kind of. Return None if there 
    is no n-of-a-kind in the hand."""
    for r in ranks:
        if ranks.count(r) == n: return r
    return None

def two_pair(ranks):
    """If there are two pair here, return the two 
    ranks of the two pairs, else None."""
    pair = kind(2, ranks)
    lowpair = kind(2, list(reversed(ranks)))
    if pair and lowpair != pair:
        return (pair, lowpair)
    else:
        return None 
    
def test_best_hand():
    assert (sorted(best_hand("6C 7C 8C 9C TC 5C JS".split()))
            == ['6C', '7C', '8C', '9C', 'TC'])
    assert (sorted(best_hand("AC 2D 3C 4S AC 5C AS".split()))
            == ['2D', '3C', '4S', '5C', 'AC'])
    assert (sorted(best_hand("TD TC TH 7C 7D 8C 8S".split()))
            == ['8C', '8S', 'TC', 'TD', 'TH'])
    assert (sorted(best_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    assert (sorted(best_hand("JD TC AH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'AH'])
    assert (sorted(best_hand("3H 7D AS 3D 3C TS KS".split()))
            == ['3C', '3D', '3H', 'AS', 'KS'])
    assert (sorted(best_hand("2H 7D AS 3D 3C TS KS".split()))
            == ['3C', '3D', 'AS', 'KS', 'TS'])
    assert (sorted(best_hand("2H 2D AS 3D 3C TS KS".split()))
            == ['2D', '2H', '3C', '3D', 'AS'])
    assert (sorted(best_hand("KD QC JH AC 7D 2S 3H".split()))
            == ['7D', 'AC', 'JH', 'KD', 'QC'])
    return 'test_best_hand passes'

print test_best_hand()
