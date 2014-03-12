# -----------------
# User Instructions
# 
# This problem deals with the one-player game foxes_and_hens. This 
# game is played with a deck of cards in which each card is labelled
# as a hen 'H', or a fox 'F'. 
# 
# A player will flip over a random card. If that card is a hen, it is
# added to the yard. If it is a fox, all of the hens currently in the
# yard are removed.
#
# Before drawing a card, the player has the choice of two actions, 
# 'gather' or 'wait'. If the player gathers, she collects all the hens
# in the yard and adds them to her score. The drawn card is discarded.
# If the player waits, she sees the next card. 
#
# Your job is to define two functions. The first is do(action, state), 
# where action is either 'gather' or 'wait' and state is a tuple of 
# (score, yard, cards). This function should return a new state with 
# one less card and the yard and score properly updated.
#
# The second function you define, strategy(state), should return an 
# action based on the state. This strategy should average at least 
# 1.5 more points than the take5 strategy.

import random

def foxes_and_hens(strategy, foxes=7, hens=45):
    """Play the game of foxes and hens."""
    # A state is a tuple of (score-so-far, number-of-hens-in-yard, deck-of-cards)
    state = (score, yard, cards) = (0, 0, 'F'*foxes + 'H'*hens)
    while cards:
        action = strategy(state)
        state = (score, yard, cards) = do(action, state)
        #print "%s => %s" % (action, state)
    return score + yard

def do(action, state):
    "Apply action to state, returning a new state."
    # Make sure you always use up one card.
    score, yard, cards = state
    cidx = random.randint(0, len(cards) - 1)
    c, cards = cards[cidx], cards[:cidx] + cards[cidx+1:]
    if action == 'gather':
        return (score + yard, 0, cards)
    else:
        return (score, 0, cards) if c == 'F' else (score, yard + 1, cards)

def take5(state):
    "A strategy that waits until there are 5 hens in yard, then gathers."
    (score, yard, cards) = state
    if yard < 5:
        return 'wait'
    else:
        return 'gather'

def average_score(strategy, N=1000):
    return sum(foxes_and_hens(strategy) for _ in range(N)) / float(N)

def superior(A, B=take5):
    "Does strategy A have a higher average score than B, by more than 1.5 point?"
    sA, sB = average_score(A), average_score(B)
    print "Yours %.2f, take5 %.2f" % (sA, sB)
    return sA - sB > 1.5

def strategy(state):
    (score, yard, cards) = state
    # your code here
    return optimal_play(state)[0]

def memo(f):
    cache = {}
    def wrap(*args):
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]
    return wrap

def pick_one(c, cards):
    f, h = cards.count('F'), cards.count('H')
    remaining = lambda cur: (cur - 1) if cur else 0
    if c == 'F':
        return remaining(f) * 'F' + h * 'H'
    else:
        return f * 'F' + remaining(h) * 'H'

@memo
def optimal_play(state):
    ''' The optimal strategy. '''
    score, yard, cards = state
    if not cards:
        return ('gather', score + yard)
    prob_fox = cards.count('F') / float(len(cards))
    def score_with_probability(probs, states_with_probs):
        return sum([p * optimal_play(state)[1] if p else 0
                    for p, state in zip(probs, states_with_probs)])
    cards_when_fox_picked = pick_one('F', cards)
    cards_when_hen_picked = pick_one('H', cards)
    def wait_score(score, yard, cards):
        state_fox = (score, 0, cards_when_fox_picked)
        state_hen = (score, yard + 1, cards_when_hen_picked)
        return score_with_probability((prob_fox, 1 - prob_fox), (state_fox, state_hen))
    def gather_score(score, yard, cards):
        state_fox = (score + yard, 0, cards_when_fox_picked)
        state_hen = (score + yard, 0, cards_when_hen_picked)
        return score_with_probability((prob_fox, 1 - prob_fox), (state_fox, state_hen))
    ws = wait_score(score, yard, cards)
    gs = gather_score(score, yard, cards)
    #print "ws %.2f gs %.2f" % (ws, gs),
    if ws > gs:
        #print "%s => %.2f (%s)" % (state, ws, 'wait')
        return ('wait', ws)
    elif gs > ws:
        #print "%s => %.2f (%s)" % (state, gs, 'gather')
        return ('gather', gs)
    else:
        choice = 'wait'
        #print "%s=> %.2f equal chance:(%s)" % (state, gs, choice)
        return (choice, ws)

def test():
    gather = do('gather', (4, 5, 'F'*4 + 'H'*10))
    assert (gather == (9, 0, 'F'*3 + 'H'*10) or 
            gather == (9, 0, 'F'*4 + 'H'*9))

    wait = do('wait', (10, 3, 'FFHH'))
    assert (wait == (10, 4, 'FFH') or
            wait == (10, 0, 'FHH'))

    cards = "FFHHHH"
    assert(pick_one('F', cards) == "FHHHH")
    assert(pick_one('H', cards) == "FFHHH")
    assert(pick_one('F', "HH") == "HH")
    assert(pick_one('H', "FFF") == "FFF")
    assert(pick_one('H', "FH") == "F")
    #foxes_and_hens(strategy)
    assert superior(strategy)
    return 'tests pass'

print test()   
