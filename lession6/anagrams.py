# -----------------
# User Instructions
#
# This homework deals with anagrams. An anagram is a rearrangement
# of the letters in a word to form one or more new words.
#
# Your job is to write a function anagrams(), which takes as input
# a phrase and an optional argument, shortest, which is an integer
# that specifies the shortest acceptable word. Your function should
# return a set of all the possible combinations of anagrams.
#
# Your function should not return every permutation of a multi word
# anagram: only the permutation where the words are in alphabetical
# order. For example, for the input string 'ANAGRAMS' the set that
# your function returns should include 'AN ARM SAG', but should NOT
# include 'ARM SAG AN', or 'SAG AN ARM', etc...

import itertools

def anagrams(phrase, shortest=2):
    """Return a set of phrases with words from WORDS that form anagram
    of phrase. Spaces can be anywhere in phrase or anagram. All words
    have length >= shortest. Phrases in answer must have words in
    lexicographic order (not all permutations)."""
    letters = phrase.replace(' ', '')
    result = set([' '.join(gram_tp) for gram_tp in
                  anagrams_recur(letters, 2)])
    return result

def anagrams_recur(letters, shortest):
    length = len(letters)
    if length == 0:
        # Return a 1 element set so we don't have to special case it later
        return set([tuple()])
    elif length < shortest:
        return set()
    result = set()
    for n in range(shortest, length + 1):
        for alpha in set(''.join(sorted(c)) for c in
                         itertools.combinations(letters, n)):
            rest = removed(letters, alpha)
            words = find_whole_words('', alpha)
            if not words:
                continue
            subset = anagrams_recur(rest, shortest)
            if subset:
                for w, gram_tp in itertools.product(words, subset):
                    # make sure it is sorted
                    if len(gram_tp) == 0 or w <= gram_tp[0]:
                        result.add((w,) + gram_tp)
    return result

def find_whole_words(pre, letters):
    #print "'%s' '%s'" % (pre, letters)
    if not letters:
        return set([pre]) if pre in WORDS else set()
    if pre in PREFIXES:
        return reduce(lambda x,y: x | y,
                      (find_whole_words(pre+L, letters.replace(L, '', 1)) for
                       L in letters),
                      set())
    else:
        return set()

def find_words_slow(letters):
    sortedstr = lambda l: ''.join(sorted(l))
    letters = sortedstr(letters)
    return set([w for w in WORDS if sortedstr(w) == letters])

# ------------
# Helpful functions
#
# You may find the following functions useful. These functions
# are identical to those we defined in lecture.

def removed(letters, remove):
    "Return a str of letters, but with each letter in remove removed once."
    for L in remove:
        letters = letters.replace(L, '', 1)
    return letters

def extend_prefix(pre, letters, results):
    if pre in WORDS: results.add(pre)
    if pre in PREFIXES:
        for L in letters:
            extend_prefix(pre+L, letters.replace(L, '', 1), results)
    return results

def prefixes(word):
    "A list of the initial sequences of a word, not including the complete word."
    return [word[:i] for i in range(len(word))]

def readwordlist(filename):
    "Return a pair of sets: all the words in a file, and all the prefixes. (Uppercased.)"
    wordset = set(open(filename).read().upper().split())
    prefixset = set(p for word in wordset for p in prefixes(word))
    return wordset, prefixset

WORDS, PREFIXES = readwordlist('words4k.txt')

# ------------
# Testing
#
# Run the function test() to see if your function behaves as expected.

def test():
    assert 'DOCTOR WHO' in anagrams('TORCHWOOD')
    assert 'BOOK SEC TRY' in anagrams('OCTOBER SKY')
    assert 'SEE THEY' in anagrams('THE EYES')
    assert 'LIVES' in anagrams('ELVIS')
    assert anagrams('PYTHONIC') >= set([
        'NTH PIC YO', 'NTH OY PIC', 'ON PIC THY', 'NO PIC THY', 'COY IN PHT',
        'ICY NO PHT', 'ICY ON PHT', 'ICY NTH OP', 'COP IN THY', 'HYP ON TIC',
        'CON PI THY', 'HYP NO TIC', 'COY NTH PI', 'CON HYP IT', 'COT HYP IN',
        'CON HYP TI'])
    return 'tests pass'

print test()
