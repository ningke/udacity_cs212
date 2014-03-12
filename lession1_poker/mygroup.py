def group(items, curr, result):
    ''' Groups ''items'', which is assumed to be sorted, into a list of tuples
    in the form: (count(x), x). curr is the current partial result for an
    item x, ''result'' is the result so far. '''
    if len(items) == 0:
        return result + [curr] if curr[0] else result
    if items[0] == curr[1]:
        return group(items[1:], (curr[0] + 1, curr[1]), result)
    elif curr[0] == 0:
        return group(items[1:], (1, items[0]), result)
    else:
        return group(items[1:], (1, items[0]), result + [curr])


if __name__ == "__main__":
    items = raw_input().split()
    items.sort()
    print group(items, [0, None], [])
