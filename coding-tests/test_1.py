__author__ = 'fj'
from pylab import *

# Problem Statement
# @url http://community.topcoder.com/stat?c=problem_statement&pm=13239
#
# Alice and Bob are playing a game. Alice rolls a identical b-sided dice. Bob rolls c identical d-sided dice. The sides of an n-sided die have numbers 1 through n written on them.
#
# A player's score is the sum of the numbers they rolled on their dice. The player with a strictly higher score wins. It is possible that neither player wins.
#
# You are given the ints a, b, c, and d. The players already rolled their dice. If it's not possible for Alice to win, return -1. Otherwise, assume that you don't know what numbers Alice and Bob rolled, but that you know that Alice won the game. Return the expected value of Alice's score (given the above assumption).
#
#
# Definition
#
# Class:	FixedDiceGameDiv1
# Method:	getExpectation
# Parameters:	int, int, int, int
# Returns:	double
# Method signature:	double getExpectation(int a, int b, int c, int d)
# (be sure your method is public)
#
#
# Notes
# -	Your return value must have an absolute or relative error smaller than 1e-3.
#
# Constraints
# -	a, b, c, d will each be between 1 and 50, inclusive.
#
# Examples
# 0)
#
# 1
# 2
# 1
# 5
# Returns: 2.0
# The only way Alice can win is if she rolls a 2. Thus, if we know Alice wins, we know she rolled a 2.
# 1)
#
# 3
# 1
# 1
# 3
# Returns: 3.0
# Alice will always roll a 3.
# 2)
#
# 1
# 5
# 1
# 1
# Returns: 3.4999999999999996
# Alice will not win if she rolls a 1. Thus, if we know she wins, her expected score is (2+3+4+5)/4=7/2.
# 3)
#
# 2
# 6
# 50
# 30
# Returns: -1.0
# No matter what Alice rolls, she will lose.
# 4)
#
# 50
# 11
# 50
# 50
# Returns: 369.8865999182022

# X = \sum_i=1^a B_i
# Y = \sum_i=1^c D_i
# E[B] = (b-1)/2, E[D] = (d-1)/2
# E[X | X > Y ] = E[ E[X| X > Z, Y=Z, Y < a*b] ] (by smoothing)
#                = \sum_{z=c}^{c*d} E[X| X > z, Y=z | Y < a*b] P[Y=z | Y < a*b]
#                = \sum_{z=c}^{c*d} E[X| X > z] P[Y=z|Y<a*b]


def getExpectation(a, b, c, d):

    if a*b < c: #alice cannot win
        return(-1)

    # initialize caches
    P.table[b] = {}
    P.table[d] = {}

    # cumulative expectation E[X | X > z]
    E_X = zeros( a*b + 1 )
    # cumulative probability P[X > z]
    P_X = zeros( a*b + 1 )

    # compute cumulative expectations for x
    for x in reversed( range(a, a*b+1) ):
        p_x = P(x, a, b )
        e_x = x*p_x
        for z in range(1, x+1 ):
            P_X[z] += p_x
            E_X[z] += e_x


    # the winning expectation
    E_w = 0;
    p_y_ab = 0; # keep track that P[Y < a*b]

    n_tot = 0
    for y in range(c, c*d+1):
        if y >= a*b:
            break
        p_ycd = P(y,c,d);
        p_y_ab += p_ycd;
        E_w += E_X[y+1]/P_X[y+1] #*p_ycd
        n_tot += 1

    return E_w /p_y_ab #n_tot



#recursively compute P[a] for sum a of M die from (1...N)
# initialize the cache before using
# try:
#     P.table[N]
# except err: # create the cache if it doesn't exist
#     P.table[N] = {} ; #python hashmap - efficient O(1) search.
def P(a, M, N ):
    if a < 1 or a > M*N:
        return 0
    try:
        P.table[N][ (M, a) ]
    except KeyError:
        # not in cache compute ...
        if M == 1:
            P.table[N][ (M, a) ] = 1.0/N;
        else:
            P.table[N][ (M, a) ] = 0;
            for aa in range(1,N+1):
               P.table[N][ (M, a) ] += 1.0/N * P( a-aa, M-1, N ) ;

    return P.table[N][ (M, a) ];

# cache computations
P.table = {};

# generate the pascals triangle for the case of (M die of N each)
def pascalsTriangle ( M, N ):

    if M == 1:
        return range(1, N+1)

    if M / 2 > 0:
        tP_t = pascalsTriangle ( floor( M/2 ), N )
        tP = sort( [ i+j for i in tP_t for j in tP_t ] );

        if mod(M,2):
            tP = sort( [ i+j for i in tP for j in range(1, N+1) ] );

    return tP

P.table[3] = {};
print P(1, 2,3)





