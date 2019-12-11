# confTool.py

import itertools as its

def allAssRul(freqSet, item):
    for r in range(1, len(item)):
        for a in its.combinations(item, r):
            print(set(a), '=>', item-set(a), freqSet[frozenset(a)]/freqSet[frozenset(item-set(a))])

# allAssRul(fset, {'A', 'C', 'B','D'})