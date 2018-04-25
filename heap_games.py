## test the heap-games posted by appolo hogan


## game - n heaps of beans. Moves are :
# take 1 bean , may split heaps in 2
# take 2 beans, must split heaps in 2 (or null heap). Can't take 2 from 3
# misere game: player who plays last looses
# normal game: player who plays last wins


from pylab import *
from collections import defaultdict
from sympy.galgebra.precedence import sub_paren


def get_partitions( n):
    '''
    All possible unique partitions of totalling up to size n
    :param n:
    :return:
    '''
    if n == 0 :
        return [ [] ]
    if n == 1:
        return [[1]];

    parts = [];
    for ss in range(1,n):
        subparts = get_partitions(n -ss)
        for sp in subparts:
            newp = [ss] + sp;
            newp.sort();
            parts.append( newp  )

    __uniqueparts = set(tuple(pp) for pp in parts + [[n]] );
    __partitions = [list(elem) for elem in __uniqueparts ]
    __partitions.sort();

    return __partitions


def twoway_splits(n):
    '''
    Get all possible 2-way splits  of size n
    :param n:
    :return:
    '''
    split_set = [];
    for p in range(1,n//2+1):
        split_set.append( [ p, n-p ] )

    return split_set;


###############################################################################
# Tables misere septequinta-quinque ...

# track the next move --- makes sense only in case the countermove is a winning one.
countermove_dict = { ():None, (0,):None, (1,):(), (2,):(1,), (1,1):(1,), (3,):(1,1), (1,1,1):(1,1) };
winlose_dict = { (): False, (0,):False, (1,):True, (2,):False, (1,1):False, (3,):True, (1,1,1):True };

# determine if A -> B this configuration leads to win for A.
def sqq_misere(config, verbose = True):
    while 0 in config: config.remove(0);

    if tuple(config) == (0,) or len(config) == 0:
        return False;

    config.sort();

    try:
        # have we already computed this configuration ?
        return winlose_dict[ tuple(config) ]
    except KeyError as ke:
        if (verbose): print('computing results for config', config);

    # this is a winning configuration unless we can prove otherwise
    winlose_dict[tuple(config)] = True;
    countermove_dict[tuple(config)] = None;

    # test each heap in the configuration
    for hp in config:
        __config = config.copy()
        __config.remove(hp);
        __config.sort();

        # Test all two-splits (and one stack) after removing 1 bean and after removing 2 beans
        subpartitions = twoway_splits( hp-1) + [[hp-1]] + twoway_splits(hp-2) 
        if hp == 2:
            subpartitions.append( [0] );

        if verbose: print('all splits for heap ', hp, 'are', subpartitions);
        for __sp in subpartitions:
            # test this new configuration
            counterconfig = __config + __sp;
            while 0 in counterconfig: counterconfig.remove(0);
            counterconfig.sort();
            if (verbose): print('\t Testing ', counterconfig);

            ## store this in the counter move dictionary.
            countermove_dict[tuple(config)] = tuple(counterconfig);
            if sqq_misere( counterconfig ):
                winlose_dict[tuple(config)] = False;
                return False;

    return winlose_dict[tuple(config)]

#sqq_misere([1,1,4])




#def enumerate_sqq_misere( n = 1):

for n in range(12):
    heap_set = get_partitions(n)
    for config in heap_set:
        print( config, sqq_misere(config, False));

for k in winlose_dict:
    if winlose_dict[k] is True:
        print(k, countermove_dict[countermove_dict[k]])

if __name__ == '__main__':
    print('hello there')






























