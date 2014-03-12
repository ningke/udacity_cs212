# -----------------
# User Instructions
# 
# Write a function, csuccessors, that takes a state (as defined below) 
# as input and returns a dictionary of {state:action} pairs. 
#
# A state is a tuple with six entries: (M1, C1, B1, M2, C2, B2), where 
# M1 means 'number of missionaries on the left side.'
#
# An action is one of the following ten strings: 
#
# 'MM->', 'MC->', 'CC->', 'M->', 'C->', '<-MM', '<-MC', '<-M', '<-C'
# where 'MM->' means two missionaries travel to the right side.
# 
# We should generate successor states that include more cannibals than
# missionaries, but such a state should generate no successors.

def csuccessors(state):
    """Find successors (including those that result in dining) to this
    state. But a state where the cannibals can dine has no successors."""
    M1, C1, B1, M2, C2, B2 = state
    def _succ(m, c, tot):
        ''' Returns a list of actions resulted from departing persons, given
        the max number of persons allowed (''tot''). Each action is a
        2-tuple of (dm, dc), where ''dm'' is the number of missionaries and
        ''dc'' is the number of cannibals.'''
        if c > m:
            return []
        res = []
        for dm in range(0, min(m, tot) + 1):
            for dc in range(0, min(c, tot - dm) + 1):
                if dm + dc != 0:
                    res.append((dm, dc))
        return res
        
    def actionstr(m, c, direction):
        pre = post = ''
        if direction == '->':
            post = direction
        elif direction == '<-':
            pre = direction
        else:
            assert(False)
        act = 'M' * m + 'C' *c
        return pre + act + post
    res = {}
    left, right = (M1, C1, B1), (M2, C2, B2)
    dst, src = sorted((left, right), key=lambda t: t[2])
    direction = '->' if src is left else '<-'
    M1, C1, B1 = src
    M2, C2, B2 = dst
    actions = _succ(M1, C1, B1 * 2)
    for dm, dc in actions:
        m1, c1 = M1 - dm, C1 - dc
        m2, c2 = M2 + dm, C2 + dc
        # number boats needed is total-persons + 1 / 2
        numboats = (dm + dc + 1) / 2
        if direction == '->':
            st = (m1, c1, B1 - numboats , m2, c2, B2 + numboats)
        else:
            st = (m2, c2, B2 + numboats, m1, c1, B1 - numboats)
        if st not in res:
            res[st] = actionstr(dm, dc, direction)
    print res
    return res

def test():
    assert csuccessors((2, 2, 1, 0, 0, 0)) == {(2, 1, 0, 0, 1, 1): 'C->', 
                                               (1, 2, 0, 1, 0, 1): 'M->', 
                                               (0, 2, 0, 2, 0, 1): 'MM->', 
                                               (1, 1, 0, 1, 1, 1): 'MC->', 
                                               (2, 0, 0, 0, 2, 1): 'CC->'}
    assert csuccessors((1, 1, 0, 4, 3, 1)) == {(1, 2, 1, 4, 2, 0): '<-C', 
                                               (2, 1, 1, 3, 3, 0): '<-M', 
                                               (3, 1, 1, 2, 3, 0): '<-MM', 
                                               (1, 3, 1, 4, 1, 0): '<-CC', 
                                               (2, 2, 1, 3, 2, 0): '<-MC'}
    assert csuccessors((1, 4, 1, 2, 2, 0)) == {}
    return 'tests pass'

print test()
