# -----------------
# User Instructions
# 
# In this problem, you will use a faster version of Pwin, which we will call
# Pwin2, that takes a state as input but ignores whether it is player 1 or 
# player 2 who starts. This will reduce the number of computations to about 
# half. You will define a function, Pwin3, which will be called by Pwin2.
#
# Pwin3 will only take me, you, and pending as input and will return the 
# probability of winning. 
#
# Keep in mind that the probability that I win from a position is always
# (1 - probability that my opponent wins).


from functools import update_wrapper

def decorator(d):
    "Make function d a decorator: d wraps a function fn."
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d

@decorator
def memo(f):
    """Decorator that caches the return value for each call to f(args).
    Then when called again with same args, we can just look it up."""
    cache = {}
    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            # some element of args refuses to be a dict key
            return f(args)
    _f.cache = cache
    return _f

goal = 40

def Pwin2(state):
   """The utility of a state; here just the probability that an optimal player
   whose turn it is to move can win from the current state."""
   _, me, you, pending = state
   return Pwin3(me, you, pending)

@memo
def Pwin3(me, you, pending):
    ## your code here
    if me + pending >= goal:
        return 1
    elif you >= goal:
        return 0
    if pending:
        return max(Pwin_hold(me, you, pending),
                   Pwin_roll(me, you, pending))
    else:
        return Pwin_roll(me, you, pending)

def Pwin_hold(me, you, pending):
#    print "hold: (%d %d %d) => %d" % (me, you, pending, 1 - Pwin3(you, me + pending, 0))
    return 1 - Pwin3(you, me + pending, 0)

def Pwin_roll(me, you, pending):
    P_pigout = 1 - Pwin3(you, me + 1, 0)
    P_other = lambda dv: Pwin3(me, you, pending + dv)
#    print "roll: (%d %d %d) => [%d], %s" % (me, you, pending, P_pigout,
#                                            [P_other(i) for i in range(2,7)])
                                                
    return (P_pigout + sum(P_other(i) for i in range(2, 7))) / 6.0


def test():
    epsilon = 0.0001 # used to make sure that floating point errors don't cause test() to fail
    assert goal == 40
    assert len(Pwin3.cache) <= 50000
    assert Pwin2((0, 42, 25, 0)) == 1
    assert Pwin2((1, 12, 43, 0)) == 0
    assert Pwin2((0, 34, 42, 1)) == 0
    assert abs(Pwin2((0, 25, 32, 8)) - 0.736357188272) <= epsilon
    assert abs(Pwin2((0, 19, 35, 4)) - 0.493173612834) <= epsilon
    return 'tests pass'

print test()

