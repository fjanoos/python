__author__ = 'fj'
# Problem Statement
#
# Nancy has a directed graph with N vertices and E edges. The vertices are numbered 1 through N. Each edge of the graph has a positive integer weight. This graph is described by three int[]s with E elements each: s, t, and weight. For each valid i, the graph contains an edge from s[i] to t[i], and its weight is weight[i]. Note that Nancy's graph may contain multiple edges with the same start and end. It may also contain self-loops.
#
# Nancy is currently standing in the vertex 1. She can reach other vertices by moving along the edges. The cost of using an edge is equal to its weight. Nancy's goal is to reach the vertex N and to minimize the total cost of doing so.
#
# Nancy has a special power she can use to make her travels cheaper. Whenever she traverses an edge, she can use that special power to make the weight of that edge temporarily negative. You are given an int charges: the number of times Nancy can use her special power. Each use of the special power only works for one traversal of an edge. Nancy can traverse each edge arbitrarily many times. Each time she traverses an edge, she may use her special power, if she still has some charges left.
#
# Compute and return the minimal total cost of Nancy's journey.
#
#
# Definition
#
# Class:	NegativeGraphDiv2
# Method:	findMin
# Parameters:	int, int[], int[], int[], int
# Returns:	long
# Method signature:	long findMin(int N, int[] s, int[] t, int[] weight, int charges)
# (be sure your method is public)
#
#
# Constraints
# -	N will be between 1 and 50, inclusive.
# -	E will be between 1 and 2500, inclusive.
# -	s, t, weight will each contain exactly E elements.
# -	s and t will only contain numbers between 1 and N, inclusive.
# -	There will be a path from node 1 to node N.
# -	weight will contain numbers between 0 and 100,000, inclusive.
# -	charges will be between 0 and 1,000, inclusive.
#
# Examples
# 0)
#
# 3
# {1,1,2,2,3,3}
# {2,3,1,3,1,2}
# {1,5,1,10,1,1}
# 1
# Returns: -9
# The optimal path for Nancy is 1->2->3, and using her single charge on the last edge.
# 1)
#
# 1
# {1}
# {1}
# {100}
# 1000
# Returns: -100000
# The graph may contain self-loops. Here, the optimal solution is that Nancy uses the self-loop 1,000 times, each time using her special power to change its cost from 100 to -100.
# 2)
#
# 2
# {1,1,2}
# {2,2,1}
# {6,1,4}
# 2
# Returns: -9
# There can be multiple edges between vertices.
# 3)
#
# 2
# {1}
# {2}
# {98765}
# 100
# Returns: -98765
# Nancy may not be able to use all her charges.
# Solve using a version of Dijkstra with a charge choice at each stage


def recursivePathFind(s,t, S, T, W , C):
    """
    :param s: source node
    :param t: dest node
    :param S: source indices
    :param T: dest indices
    :param W: weights
    :param C: num charges
    :return: minimum path and weight
    """


    for nbr in [ nn for ss,nn in zip(S,T) if ss == s]:
        # iterate over all dests for this source
        try:
            recursivePathFind.cost_mtx[ (nbr, t, C ) ]
        except KeyError:


        if dst == t:






recursivePathFind.cost_mtx = {};
recursivePathFind.pth_mtx = {};

