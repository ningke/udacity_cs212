# ---------------
# User Instructions
#
# Write a function, n_ary(f), that takes a binary function (a function
# that takes 2 inputs) as input and returns an n_ary function. 

def n_ary(f):
    """Given binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x."""
    def n_ary_f(x, *args):
        if len(args) == 0:
            return x
        elif len(args) == 1:
            return f(x, args[0])
        else:
            return f(x, n_ary_f(args[0], *args[1:]))
    return n_ary_f

add = lambda x, y: (x + y)
addn = n_ary(add)
print addn(1, 3, 5)
