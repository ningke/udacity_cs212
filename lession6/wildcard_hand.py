import itertools

def hands_with_wc(hand):
    all_letters = lambda : (l for l in "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    num = hand.count('_')
    if num == 0:
        return set([hand])
    else:
        non_wc = hand.replace('_', '')
        wc_hand = (''.join(c) for c in itertools.product(all_letters(), repeat=num))
        return set(''.join([c, non_wc]) for c in wc_hand)


print sorted(list(hands_with_wc("__ABC")))
