# Unit 6: Fun with Words

"""
A portmanteau word is a blend of two or more words, like 'mathelete',
which comes from 'math' and 'athelete'.  You will write a function to
find the 'best' portmanteau word from a list of dictionary words.
Because 'portmanteau' is so easy to misspell, we will call our
function 'natalie' instead:

    natalie(['word', ...]) == 'portmanteauword'

In this exercise the rules are: a portmanteau must be composed of
three non-empty pieces, start+mid+end, where both start+mid and
mid+end are among the list of words passed in.  For example,
'adolescented' comes from 'adolescent' and 'scented', with
start+mid+end='adole'+'scent'+'ed'. A portmanteau must be composed
of two different words (not the same word twice).

That defines an allowable combination, but which is best? Intuitively,
a longer word is better, and a word is well-balanced if the mid is
about half the total length while start and end are about 1/4 each.
To make that specific, the score for a word w is the number of letters
in w minus the difference between the actual and ideal lengths of
start, mid, and end. (For the example word w='adole'+'scent'+'ed', the
start,mid,end lengths are 5,5,2 and the total length is 12.  The ideal
start,mid,end lengths are 12/4,12/2,12/4 = 3,6,3. So the final score
is

    12 - abs(5-3) - abs(5-6) - abs(2-3) = 8.

yielding a score of 12 - abs(5-(12/4)) - abs(5-(12/2)) -
abs(2-(12/4)) = 8.

The output of natalie(words) should be the best portmanteau, or None
if there is none.

Note (1): I got the idea for this question from
Darius Bacon.  Note (2): In real life, many portmanteaux omit letters,
for example 'smoke' + 'fog' = 'smog'; we aren't considering those.
Note (3): The word 'portmanteau' is itself a portmanteau; it comes
from the French "porter" (to carry) + "manteau" (cloak), and in
English meant "suitcase" in 1871 when Lewis Carroll used it in
'Through the Looking Glass' to mean two words packed into one. Note
(4): the rules for 'best' are certainly subjective, and certainly
should depend on more things than just letter length.  In addition to
programming the solution described here, you are welcome to explore
your own definition of best, and use your own word lists to come up
with interesting new results.  Post your best ones in the discussion
forum. Note (5) The test examples will involve no more than a dozen or so
input words. But you could implement a method that is efficient with a
larger list of words.
"""

from itertools import *

def prefixesof(word):
    ''' list of prefixes in ''word'' not including the whole word. '''
    return (word[:i] for i in range(1, len(word) - 1))

def suffixesof(word):
    ''' list of suffixes in ''word'' not including the whole word. '''
    return (word[i:] for i in range(1, len(word)))

def natalie(words):
    "Find the best Portmanteau word formed from any two of the list of words."
    presuffixes = {}
    def addto(psfix, word, what):
        if psfix not in presuffixes:
            presuffixes[psfix] = ([], [])
        i = 1 if what == 'prefix' else 0
        presuffixes[psfix][i].append(word)
        pass
    for w in words:
        for px in prefixesof(w):
            addto(px, w, 'prefix')
        for sx in suffixesof(w):
            addto(sx, w, 'suffix')
    #for x in sorted(presuffixes.keys()):
        #print "%s: %s" % (x, presuffixes[x])
    highscore = (0, None)
    for psfix in presuffixes:
        firsts, seconds = presuffixes[psfix]
        midlen = len(psfix)
        for first, second in product(firsts, seconds):
            if first != second:
                front = first[:(len(first)-midlen)]
                mid = psfix
                back = second[midlen:]
                scr = pscore(front, mid, back)
                #print "%s + %s + %s = %f" % (front, mid, back, scr)
                if scr > highscore[0]:
                    highscore = (scr, front+mid+back)
    return highscore[1]

def pscore(front, mid, back):
    ''' Return score of a portmanteau. The score for a word w is the number of letters
    in w minus the difference between the actual and ideal lengths of start, mid
    and end. '''
    frontlen, midlen, backlen = len(front), len(mid), len(back)
    wlen = frontlen + midlen + backlen
    return wlen - (abs(frontlen - wlen/4.0) + abs(midlen - wlen/2.0) +
                   abs(backlen - wlen/4.0))

def test_natalie():
    "Some test cases for natalie"
    assert natalie(['adolescent', 'scented', 'centennial', 'always', 'ado']) in ('adolescented','adolescentennial')
    assert natalie(['eskimo', 'escort', 'kimchee', 'kimono', 'cheese']) == 'eskimono'
    assert natalie(['kimono', 'kimchee', 'cheese', 'serious', 'us', 'usage']) == 'kimcheese'
    assert natalie(['circus', 'elephant', 'lion', 'opera', 'phantom']) == 'elephantom'
    assert natalie(['programmer', 'coder', 'partying', 'merrymaking']) == 'programmerrymaking'
    assert natalie(['int', 'intimate', 'hinter', 'hint', 'winter']) == 'hintimate'
    assert natalie(['morass', 'moral', 'assassination']) == 'morassassination'
    assert natalie(['entrepreneur', 'academic', 'doctor', 'neuropsychologist', 'neurotoxin', 'scientist', 'gist']) in ('entrepreneuropsychologist', 'entrepreneurotoxin')
    assert natalie(['perspicacity', 'cityslicker', 'capability', 'capable']) == 'perspicacityslicker'
    assert natalie(['backfire', 'fireproof', 'backflow', 'flowchart', 'background', 'groundhog']) == 'backgroundhog'
    assert natalie(['streaker', 'nudist', 'hippie', 'protestor', 'disturbance', 'cops']) == 'nudisturbance'
    assert natalie(['night', 'day']) == None
    assert natalie(['dog', 'dogs']) == None
    assert natalie(['test']) == None
    assert natalie(['']) ==  None
    assert natalie(['ABC', '123']) == None
    assert natalie([]) == None
    return 'tests pass'

print test_natalie()
