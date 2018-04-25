__author__ = 'fj'

from heapq import *


class UnionFindSet( object ):
	"""
	a union find data structure - with rank balancing.
	"""
	def __init__(self):
		self.parent = self
		self.rank = 0

	def Find(self):
		""" find the parent of the current set. also do path compression
		"""
		if self != self.parent:
			self.parent =self.parent.Find()
		return self.parent

	def Union(self, other):
		"""
		Union two sets. root the shallower one with the deeper one.
		:return False if they are already the same. else return true
		"""
		r1 = self.Find()
		r2 = other.Find()
		if r1 == r2 :
			return False
		else:
			if r1.rank < r2.rank:
				r1.parent = r2
			elif  r1.rank > r2.rank:
				r2.parent = r1
			else: # add one to the other - and increase tree depth.
				r2.parent = r1
				r1.rank += 1
		return True

def MinSpanTree(N, edge_heap ):
	"""
	computes the minimum spanning tree
	:N : number of nodes
	:param edge_heap:  a heapq of all edges. The item must support comparison
	operators and [] to get node indices. Also must have cost property
	:return:
	"""
	nodes = [ UnionFindSet() for i in range(N)] # individual forests for each node
	nf = N  # number of independent forests
	cost = 0;

	edge_list = []

	for cnt in range(len(edge_heap)):
		me = heappop(edge_heap) # lowest cost edge
		if  nodes[me[0]].Union( nodes[me[1]] ) :
			# the two are distinct forests.
			cost += me.cost
			edge_list.append(me)
			nf -= 1
		else:
			# the two nodes are in the same tree.
			pass
	if nf > 1:
		print "fuckup in counting"

	return (cost, edge_list)
