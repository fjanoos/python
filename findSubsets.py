#!/usr/bin/env python


from copy import deepcopy
from optparse import OptionParser
from math import factorial

def enumerateElements(N,n, bv_, X, count):
    ''' generate all possible T/F combinations for 
        bits at positions N-1 ... 0, totalling to n T's
    '''
    bv = deepcopy(bv_);
    if n > N:
        raise Exception('error here');
    elif n == 0:                
        # reached the bottom of the recursion - enumerate the set
        count+=1;
        print str(count) + ':\t' + str( [X[p] for p in xrange(len(bv)) if  bv[p] == True])
        return;
    elif n == N:
        # no more elements lefts to play with - end recursion
        bv[0:N] = [True]*N;
        enumerateElements(0,0, bv, X,count);
        return;
    else:
        bv[N-1] = True;
        enumerateElements(N-1,n-1, bv, X,count);
        bv[N-1] = False;
        enumerateElements(N-1,n, bv, X,count);
        return

def startEnumeration(X, n):
    N = len(X);       
    bv = [False]*(N-n)+[True]*n;
    count = 0;
    enumerateElements(N,n, bv, X, count);
    print 'Total count = ' + str( factorial(N)/factorial(N-n)/factorial(n));    


if __name__ == "__main__":
    usage = \
''' %prog N n 
    Plot vtk files'''
    
    option_parser = OptionParser(usage)
    option_parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=True) 
       
    (options, args) = option_parser.parse_args()
    
    if len(args) != 2:
        option_parser.print_help()
        sys.exit();

    startEnumeration(xrange(int(args[0])), int(args[1]));


