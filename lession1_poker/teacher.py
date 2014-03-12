def search(partial, orig, rem, n, results):
    ''' Enumerates all possible outcome of the teacher's shuffling algorithm,
    which picks two random cards at a time and swap them until all cards have
    been swapped exactly once.
    'partial' is the partial result (some 'None's in the list).
    'orig' is the orignial deck with some cards invalidated ('None').
    'rem' is the number of remaining unswapped cards (count('None')).
    'n' is the total number of cards. (it doesn't change).
    'results' is the set of results so far accumulated. '''
    if rem == 0:
        #print partial
        results.add(tuple(partial))
        return
    for i in xrange(n):
        if orig[i] is not None:
            for j in xrange(n):
                if orig[j] is not None:
                    newpartial, neworig = partial[:], orig[:]
                    newpartial[j], newpartial[i] = orig[i], orig[j]
                    neworig[i], neworig[j] = None, None
                    search(newpartial, neworig, rem - (2 - int(i == j)), n, results)

if __name__ == "__main__":
    deck = raw_input("").split()
    n = len(deck)
    res = set([])
    search([None]*n, deck, n, n, res)
    print res
