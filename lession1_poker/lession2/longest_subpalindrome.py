# --------------
# User Instructions
#
# Write a function, longest_subpalindrome_slice(text) that takes 
# a string as input and returns the i and j indices that 
# correspond to the beginning and end indices of the longest 
# palindrome in the string. 
#
# Grading Notes:
# 
# You will only be marked correct if your function runs 
# efficiently enough. We will be measuring efficency by counting
# the number of times you access each string. That count must be
# below a certain threshold to be marked correct.
#
# Please do not use regular expressions to solve this quiz!

import itertools

def longest_subpalindrome_slice(text):
    "Return (i, j) such that text[i:j] is the longest palindrome in text."
    ''' Since a palindrome has a center and characters around the center are
    symmetric. We search all the centers in ''text'' and keep track of the
    longest palindrome so far. '''
    text = text.lower()
    txtlen = len(text)
    max_paln = null_paln = (0, -1)
    for cpos in xrange(0, txtlen):
        # Odd number has the center text[cpos]
        res = list(itertools.takewhile(
                lambda x: text[x[0]] == text[x[1]],
                ((i, j) for i, j in itertools.izip(
                        range(cpos, -1, -1), range(cpos, txtlen)))))
        odd_paln = res[-1]
        res = list(itertools.takewhile(
                lambda x: text[x[0]] == text[x[1]],
                ((i, j) for i, j in itertools.izip(
                        range(cpos-1, -1, -1), range(cpos, txtlen)))))
        even_paln = res[-1] if res else null_paln
        max_paln = max((max_paln, odd_paln, even_paln), key=lambda x: (x[1] - x[0]))
    # Returns a Python Style range
    max_paln =  (max_paln[0], max_paln[1] + 1)
    print max_paln
    return max_paln
 
def test():
    L = longest_subpalindrome_slice
    assert L('racecar') == (0, 7)
    assert L('Racecar') == (0, 7)
    assert L('RacecarX') == (0, 7)
    assert L('Race carr') == (7, 9)
    assert L('') == (0, 0)
    assert L('something rac e car going') == (8,21)
    assert L('xxxxx') == (0, 5)
    assert L('Mad am I ma dam.') == (0, 15)
    return 'tests pass'

print test()
