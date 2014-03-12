#------------------
# User Instructions
#
# Hopper, Kay, Liskov, Perlis, and Ritchie live on 
# different floors of a five-floor apartment building. 
#
# Hopper does not live on the top floor. 
# Kay does not live on the bottom floor. 
# Liskov does not live on either the top or the bottom floor. 
# Perlis lives on a higher floor than does Kay. 
# Ritchie does not live on a floor adjacent to Liskov's. 
# Liskov does not live on a floor adjacent to Kay's. 
# 
# Where does everyone live?  
# 
# Write a function floor_puzzle() that returns a list of
# five floor numbers denoting the floor of Hopper, Kay, 
# Liskov, Perlis, and Ritchie.

import itertools

def floor_puzzle():
    # Your code here
    def satisfied(h, k, l, p, r):
        return (
            h != 5
            and k != 1
            and (l != 1 and l!= 5)
            and p > k
            and (abs(r - l) != 1)
            and (abs(l - k) != 1)
            )
    return next([Hopper, Kay, Liskov, Perlis, Ritchie] \
                    for Hopper, Kay, Liskov, Perlis, Ritchie \
                    in itertools.permutations(range(1, 6)) \
                    if satisfied(Hopper, Kay, Liskov, Perlis, Ritchie))


if __name__ == '__main__':
    print floor_puzzle()
