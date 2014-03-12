# --------------
# User Instructions
#
# Write a function, inverse, which takes as input a monotonically
# increasing (always increasing) function that is defined on the 
# non-negative numbers. The runtime of your program should be 
# proportional to the LOGARITHM of the input. You may want to 
# do some research into binary search and Newton's method to 
# help you out.
#
# This function should return another function which computes the
# inverse of the input function. 
#
# Your inverse function should also take an optional parameter, 
# delta, as input so that the computed value of the inverse will
# be within delta of the true value.

# -------------
# Grading Notes
#
# Your function will be called with three test cases. The 
# input numbers will be large enough that your submission
# will only terminate in the allotted time if it is 
# efficient enough. 

def slow_inverse(f, delta=1/128.):
    """Given a function y = f(x) that is a monotonically increasing function on
    non-negatve numbers, return the function x = f_1(y) that is an approximate
    inverse, picking the closest value to the inverse, within delta."""
    def f_1(y):
        x = 0
        while f(x) < y:
            x += delta
        # Now x is too big, x-delta is too small; pick the closest to y
        return x if (f(x)-y < y-f(x-delta)) else x-delta
    return f_1 

def inverse(f, delta = 1/128.):
    """Given a function y = f(x) that is a monotonically increasing function on
    non-negatve numbers, return the function x = f_1(y) that is an approximate
    inverse, picking the closest value to the inverse, within delta."""
    def invf(y):
        # first find upper bound for x in form of 2 exp m
        def upper_bound(x, prev_x):
            return (x, prev_x) if f(x) >= y else upper_bound(2*x, x)
        upper, lower = upper_bound(1, 0)
        # Now keep refining it by taking averages of upper and lower
        def refine(x, upper):
            assert(x < upper)
            if (y - f(x)) <= delta:
                return x
            avg = (x + upper) / 2.0
            return refine(avg, upper) if f(avg) < y else refine(x, avg)
        return refine(lower, upper)
    return invf
    
def square(x): return x*x
sqrt = inverse(square)

print sqrt(1000000000)
