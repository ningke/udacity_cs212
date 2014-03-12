def poker(hands):
    "Return a list of winning hands: poker([hand,...]) => [hand,...]"
    return allmax(hands, key=hand_rank)

def allmax(iterable, key=(lambda x: x)):
    "Return a list of all items equal to the max of the iterable."
    slist = sorted(iterable, key=key, reverse=True)
    res = [slist[0]]
    for i in slist[1:]:
        if key(i) == key(res[0]):
            res.append(i)
    return res

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
    "Return True if the ordered ranks form a 5-card straight."
    return (max(ranks)-min(ranks) == 4) and len(set(ranks)) == 5

def two_pair(ranks):
    """If there are two pair, return the two ranks as a
    tuple: (highest, lowest); otherwise return None."""
    comp = ranks[0]
    match = 1
    res = []
    for r in ranks[1:]:
        if comp == r:
            match += 1
        else: # No match
            if match == 2:
                res.append(comp)
            # reset search
            match = 1
            comp = r
    if match == 2:
        res.append(comp)
    return tuples(res) if len(res) == 2 else None

def my_card_ranks(cards):
    "Return a list of the ranks, sorted with higher first."
    ranksmap = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    ranks = [r for r,s in cards]
    fixed_ranks = []
    for r in ranks:
        try:
            r = int(r)
        except ValueError:
            r = ranksmap[r]
        fixed_ranks.append(r)
    ranks = fixed_ranks
    ranks.sort(reverse=True)
    return ranks

def kind(n, ranks):
    """Return the first rank that this hand has exactly n of.
    Return None if there is no n-of-a-kind in the hand."""
    comp = ranks[0]
    match = 1
    for r in ranks[1:]:
        if r == comp:
            match += 1
            continue
        # Not a match and exactly n kinds
        if match == n:
            break
        # Reset state and continue searching
        comp = r
        match = 1
    return comp if (match == n) else None

def test():
    "Test cases for the functions in poker program."
    sf = "6C 7C 8C 9C TC".split() # Straight Flush
    fk = "9D 9H 9S 9C 7D".split() # Four of a Kind
    fh = "TD TC TH 7C 7D".split() # Full House
    tp = "8S JH 8C 4H JD".split() # Two pairs
    fkranks = card_ranks(fk)
    tpranks = card_ranks(tp)
    assert two_pair(tpranks) == (11, 8)
    assert kind(4, fkranks) == 9
    assert kind(3, fkranks) == None
    assert kind(2, fkranks) == None
    assert kind(1, fkranks) == 7
    return 'tests pass'
    
if __name__ == "__main__":
    print test()
