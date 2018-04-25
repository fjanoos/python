# Problem Statement http://community.topcoder.com/stat?c=problem_statement&pm=13339
#
# Alice likes eating candies. Her favorite type of candy are the Surprise Candies. Surprise Candies come in N
# different flavors and in N different shapes. You know the following facts about the shapes and flavors of Surprise
# Candies:
#
# The shapes are numbered 0 through N-1.
# The flavors are numbered 0 through N-1.
# You can tell the shape of a candy before buying it. (Thus, you can do stuff like "buy exactly 47 candies of shape 3".)
# You can only tell the flavor of a candy when eating it. (Thus, you do not know the flavor when you are buying the
# candy.)
# For each shape of Surprise Candies, there are exactly two flavors that can have that shape.
# For each flavor of Surprise Candies, there are exactly two shapes that can have that flavor.
# In Alice's street there is a store that sells Surprise Candies. Alice knows the exact inventory of this store. You
# are given this information in int[]s Type1, Number1, Type2, and Number2. Each of these int[]s has exactly N
# elements. For each i, their elements at index i correspond to the shape number i, as follows:
#
# The store contains exactly Number1[i] candies with shape i and flavor Type1[i].
# The store contains exactly Number2[i] candies with shape i and flavor Type2[i].
# Alice wants to eat candies of all N flavors today. However, she is lazy to go to the store, so she sent Kirito to
# do the shopping for her. Kirito must buy a set of candies that is guaranteed to contain all N flavors. Return the
# smallest number of candies Kirito may buy.
#
#
# Definition
#
# Class:	CandyCollection
# Method:	solve
# Parameters:	int[], int[], int[], int[]
# Returns:	int
# Method signature:	int solve(int[] Type1, int[] Number1, int[] Type2, int[] Number2)
# (be sure your method is public)
#
#
# Constraints
# -	N will between 1 and 1000, inclusive.
# -	Type1, Number1, Type2, Number2 will each contain exactly N elements.
# -	For each i, Type1[i] and Types2[i] will be different.
# -	Each element of Type1 and Type2 will be between 0 and N-1, inclusive.
# -	Each element of Number1 and Number2 will be between 1 and 1000, inclusive.
# -	Each of the values 0 through N-1 will appear exactly twice in Type1 and Type2 together.
#
# Examples
# 0)
#
# {0,0}
# {1,1}
# {1,1}
# {1,1}
# Returns: 2
# In this test case we have N=2. Thus, there are two shapes and two flavors. The store has exactly one candy for each
# combination (shape,flavor). Kirito can simply buy two candies with the same shape, their flavors must be different.
# 1)
#
# {0,0}
# {2,5}
# {1,1}
# {2,5}
# Returns: 3
# In this test case we have N=2 again, but now the supply of candies in the store is larger. There are 2+2 = 4
# candies of shape 0, and 5+5 = 10 candies of shape 1. The optimal strategy for Kirito is to buy 3 candies of shape
# 0. Both flavors have to be present in those three candies.
# 2)
#
# {0,0,2,3}
# {1,1,2,2}
# {1,1,3,2}
# {1,1,2,2}
# Returns: 5
# One optimal solution is to buy two candies of shape 0 and three candies of shape 2.
# 3)
#
# {0,1,2,3}
# {5,5,10,13}
# {1,2,3,0}
# {8,8,10,15}
# Returns: 20
# 4)
#
# {12,9,0,16,9,18,12,3,6,0,8,2,10,6,5,2,14,10,5,13}
# {895,704,812,323,334,674,665,142,712,254,869,548,645,663,758,38,860,724,742,530}
# {1,4,7,11,15,8,18,13,17,17,19,14,7,11,4,1,15,19,3,16}
# {779,317,36,191,843,289,107,41,943,265,649,447,806,891,730,371,351,7,102,394}
# Returns: 5101

""" Logic : construct a graph where each node is a flavor. Two flavors share an edge if there is a shape that has these
two flavors. i.e. shapes correspond to edges.
 The cost of the edge is max(m,n)+1 where m,n are the number of candies of the flavors for that shape. This is the minimum
 number of that shape needed to guarantee one of each type.
    The solution is finiding the min-cost tree.

WRONG !!

the 2x2 requirement creates loops in the graph. i.e. you have sub-graphs which are completely closed and can be solve
independently

each loop is to be solved using dp.

"""

__author__ = 'fj'

from pylab import *
from collections import deque


class LoopyNode( object ):
	""" nodes in a graph that closes in loops. each vertex is a flavor.
	"""

	def __init__( self, id = -1 ):
		self.id = id
		self.nbs = [self, self]

	def __repr__( self ):
		return "Node %d with nbs (%d, %d)" % (self.id, self.nbs[0].id, self.nbs[1].id)

	def add_nbr( self, nbr ):
		if self.nbs[0] == self:
			self.nbs[0] = nbr
		elif self.nbs[1] == self:
			self.nbs[1] = nbr
		else:
			print "error in loopy asssumption"
			raise Exception( )

	def is_nbr( self, node ):
		if (node is self.nbs[0]) or (node is self.nbs[1]):
			return True
		else:
			return False

	def get_other_nbr( self, prev ):
		"""
		:param prev: the node who's other nbr i want
		:return:
		"""
		if not ( self.is_nbr( prev ) and prev.is_nbr( self ) ):
			print "error in nbd calculation"
			raise Exception( )
		return self.nbs[1] if self.nbs[0] == prev else self.nbs[0]

	def get_chain( self ):
		"""
		:return the chain starting from this node (not inclusive)
		"""
		chain = [self.id]
		nn = self.nbs[0]
		nn_prev = self
		while nn is not self:
			chain.append( nn.id )
			nn_next = nn.get_other_nbr( nn_prev )
			nn_prev = nn
			nn = nn_next
		return chain


def loopsolve( start_node, edges ):
	# solve each loop independently - nodes is the list of nodes in order.
	# N nodes, N edges. edges 1 to N

	# satisfy first node in forward order
	chain = start_node.get_chain( ) #this forces edge 1
	recursive_solve.tab_nf = {-1:  edges[chain[-1], chain[0]][1]+1 } # wrap around cost ...
	recursive_solve.tab_dnf = {-1: 0  } # wrap around cost ...
	t1 = recursive_solve( chain, edges, True )

	# satisfy first node in backward order
	chain.append(chain[0])
	del chain[0]
	chain.reverse() # reverse chain direction
	recursive_solve.tab_nf = {-1:  edges[chain[-1], chain[0]][1]+1 } # wrap around cost ...
	recursive_solve.tab_dnf = {-1: 0  } # wrap around cost ...
	t2 = recursive_solve( chain[1:], edges, True )
	return (t2, t1)

def recursive_solve( chain, edges, nf=True):
	"""
	:param chain: chain of remaining nodes to satisfy
	:param edges: the list of all edges
	:param nf: do we need the first node on the chain ?
	:return:
	"""
	if nf: tab = recursive_solve.tab_nf
	else : tab = recursive_solve.tab_dnf

	if len(chain) == 0:
		return 0
	if len( chain ) == 1 :
		# in case we're down to the last node in the chain,  wrap around the loop
		return tab[-1]

	try:
		tab[chain[0]]
	except KeyError:
		# the cost of the edge (left, right) depends on whether we need the first one or
		# not.
		nl = edges[(chain[0], chain[1])][0]
		nr = edges[(chain[0], chain[1])][1]
		if nf == True:
			# If we need the first one - then cost = nr + 1. This also determines if we need the second one ...
			# (if nl > nf)
			if nr >= nl:
				# the right one is also guaranteed
				recursive_solve.tab_nf[chain[0]] = nr + 1 +  recursive_solve( chain[1:], edges, False ) # don't need this one
			else: # right one is not guaranteed
				c1 = nr + 1 +  recursive_solve( chain[1:], edges, True ) # still need the second one
				c2 = nl + 1 +  recursive_solve( chain[1:], edges, False ) # don't need second one
				recursive_solve.tab_nf[chain[0]] = min(c1, c2)
		else:
			# do not really need the first node
			# satisfy the second node
			c1 = nl+1 + recursive_solve( chain[1:], edges, False ) # don't need the second node henceforth
			c2 = recursive_solve( chain[1:], edges, True ) # we haven't satisfied the second node as yet.
			recursive_solve.tab_dnf[chain[0]] = min( c1, c2)
	return tab[chain[0]]

recursive_solve.tab_nf = {} # need first. -1: first_count + 1 ---corresponds to the wrap around cost (last_node, first_node). cost is
recursive_solve.tab_dnf = {} # do not need first. -1: first_count + 0 ---corresponds to the wrap around cost (last_node, first_node). cost is

if __name__ == '__main__':
	T1 = [1, 28, 17, 13, 8, 32, 16, 41, 9, 24, 16, 15, 2, 18, 39, 15, 25, 33, 12, 34, 35, 10, 13, 41, 5, 31, 19, 21, 42, 42, 28, 33, 3, 26, 38, 37, 22, 37, 6, 27, 14, 31, 0]
	N1 = [377, 309, 440, 324, 539, 83, 542, 116, 659, 931, 307, 387, 746, 73, 830, 574, 513, 291, 637, 768, 575, 53, 151, 725, 431, 192, 338, 288, 384, 910, 759, 589, 947, 31, 169, 592, 656, 360, 538, 484, 42, 351, 837]
	T2 = [9, 20, 14, 23, 11, 7, 34, 11, 27, 0, 7, 10, 3, 40, 24, 23, 26, 29, 8, 20, 17, 12, 35, 25, 36, 2, 22, 30, 38, 30, 39, 19, 4, 1, 36, 21, 6, 18, 40, 32, 4, 5, 29]
	N2 = [967, 932, 945, 627, 538, 119, 930, 834, 640, 705, 978, 674, 22, 925, 271, 778, 98, 987, 162, 356, 656, 32, 351, 942, 967, 108, 8, 458, 754, 946, 210, 222, 423, 507, 414, 901, 763, 411, 625, 549, 596, 603, 292]


	N = len( T1 )
	nodes = [LoopyNode( i ) for i in range( N )]
	node_used = [0 ]*N
	edges = { }
	for (t1, n1, t2, n2) in zip( T1, N1, T2, N2 ):
		edges[(t1, t2)] = (n1,n2)
		edges[(t2, t1)] = (n2,n1)
		nodes[t1].add_nbr( nodes[t2] )
		nodes[t2].add_nbr( nodes[t1] )

	tot_cost = 0

	while 0 in  node_used:
		un = node_used.index(0)
		for ni in nodes[un].get_chain():
			node_used[ni] = 1
		print loopsolve( nodes[un], edges )


