"""
UNIT 2: Logic Puzzle

You will write code to solve the following logic puzzle:

1. The person who arrived on Wednesday bought the laptop.
2. The programmer is not Wilkes.
3. Of the programmer and the person who bought the droid,
   one is Wilkes and the other is Hamming. 
4. The writer is not Minsky.
5. Neither Knuth nor the person who bought the tablet is the manager.
6. Knuth arrived the day after Simon.
7. The person who arrived on Thursday is not the designer.
8. The person who arrived on Friday didn't buy the tablet.
9. The designer didn't buy the droid.
10. Knuth arrived the day after the manager.
11. Of the person who bought the laptop and Wilkes,
    one arrived on Monday and the other is the writer.
12. Either the person who bought the iphone or the person who bought the tablet
    arrived on Tuesday.

You will write the function logic_puzzle(), which should return a list of the
names of the people in the order in which they arrive. For example, if they
happen to arrive in alphabetical order, Hamming on Monday, Knuth on Tuesday, etc.,
then you would return:

['Hamming', 'Knuth', 'Minsky', 'Simon', 'Wilkes']

(You can assume that the days mentioned are all in the same week.)
"""

import itertools

persons_perm = lambda : itertools.permutations(['Hamming', 'Knuth', 'Minsky', 'Simon', 'Wilkes'])
gadgets_perm = lambda : itertools.permutations(['laptop', 'droid', 'tablet', 'iphone', '-'])
roles_perm = lambda : itertools.permutations(['programmer', 'manager', 'designer', 'writer', '-'])
days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

def logic_puzzle():
    "Return a list of the names of the people, in the order they arrive."
    ## your code here; you are free to define additional functions if needed
    results = set()
    for persons in persons_perm():
        # 6, 11 (with 1)
        if persons[0] == 'Wilkes' and \
                persons.index('Knuth') == persons.index('Simon') + 1:
            #print persons
            for gadgets in gadgets_perm():
                # 1, 3, 8, 12
                if gadgets[2] == 'laptop' \
                        and persons.index('Wilkes') == gadgets.index('droid') \
                        and gadgets[4] != 'tablet' \
                        and gadgets[1] in ['iphone', 'tablet']:
                    #print zip(persons, gadgets)
                    for roles in roles_perm():
                        # 2, 3, 4, 5, 7, 9, 10, 11
                        candidate = tuple((d, p, g, r) for d, p, g, r in
                                          itertools.izip(days_of_week, persons, gadgets, roles))
                        #print candidate
                        if persons.index('Wilkes') != roles.index('programmer') \
                                and persons.index('Hamming') == roles.index('programmer') \
                                and persons.index('Minsky') != roles.index('writer') \
                                and roles.index('manager') not in [persons.index('Knuth'), gadgets.index('tablet')] \
                                and roles[3] != 'designer' \
                                and roles.index('designer') != gadgets.index('droid') \
                                and persons.index('Knuth') == roles.index('manager') + 1  \
                                and roles.index('writer') == gadgets.index('laptop'):
                            results.add(candidate)
    print results
    return [t[1] for t in list(results)[0]]

print logic_puzzle()
