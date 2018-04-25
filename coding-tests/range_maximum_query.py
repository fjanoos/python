# Problem Statement
#
# The range maximum query (RMQ) problem looks as follows: You are given a permutation P of the numbers 1 through
#  n, and a sequence of queries. Each query is a pair of integers (L,R) such that 1 <= L <= R <= n. The answer to the
#  query is the maximum of the values that occur in P at (1-based) positions L through R, inclusive.
#
# For example, if P is the permutation (3,1,4,2,5), then:
# The answer to the query (1,2) is max(3,1)=3.
# The answer to the query (2,4) is max(1,4,2)=4.
# The answer to the query (4,5) is max(2,5)=5.
#
# In this problem, we ask you to solve the inverse problem. You are given the int n, and three int[]s A, B, and ans,
# each containing the same number of elements. We are looking for a permutation P of numbers 1 through n with the
# following property: For each valid i, the answer to the query (A[i], B[i]) must be ans[i]. Return "Possible" (
# quotes for clarity) if at least one such permutation P exists, and "Impossible" otherwise.
#
#
# Definition
#
#
# Class: InverseRMQ
# Method: possible
# Parameters: int, int[], int[], int[]
# Returns: String
# Method signature: String possible(int n, int[] A, int[] B, int[] ans)
# (be sure your method is public)
#
# Constraints
#
# - n will be between 1 and 1,000,000,000, inclusive.
# - A will contain between 1 and 50 elements, inclusive.
# - A, B, and ans will each contain the same number of elements.
# - Each element in A will be between 1 and n, inclusive.
# - Each element in B will be between 1 and n, inclusive.
# - For all i, A[i] will be less than or equal to B[i].
# - Each element in ans will be between 1 and n, inclusive.
#
#
# Examples
#
# 0)
# 5
# {1,2,4}
# {2,4,5}
# {3,4,5}
# Returns: "Possible"
#
#
# This is the example from the problem statement. One valid permutation is (3,1,4,2,5). There are also some other
# valid permutations.
#
# 1)
# 3
# {1,2,3}
# {1,2,3}
# {3,3,3}
#
#
# Returns: "Impossible"
#
#
# The only sequence that corresponds to these queries is (3,3,3), but that is not a permutation.
#
#
# 2)
# 600
# {1,101,201,301,401,501}
# {100,200,300,400,500,600}
# {100,200,300,400,500,600}
# Returns: "Possible"
#
#
# One valid permutation is the permutation (1,2,3,...,600).
#
#
# 3)
# 1000000000
# {1234,1234}
# {5678,5678}
# {10000,20000}
# Returns: "Impossible"
# There is no permutation such that two identical queries have different answers.
#
#
# 4)
# 8
# {1,2,3,4,5,6,7,8}
# {1,2,3,4,5,6,7,8}
# {4,8,2,5,6,3,7,1}
#
# Returns: "Possible"
#
#
# The only valid permutation is clearly (4,8,2,5,6,3,7,1).
#
#
# 5)
# 1000000000
# {1}
# {1000000000}
# {19911120}
# Returns: "Impossible"
# Obviously, for n=1,000,000,000 the maximum of the entire permutation must be 1,000,000,000.
#
#http://community.topcoder.com/stat?c=problem_statement&pm=13235

"""
The idea is two fold:

for each range of number - look at sequences of intersections and unions and examine for consistency. Also, do basic
checks (eg case 5)

SEEMS TO BE WORKING CORRECTLY
"""

__author__ = 'fjanoos'

from collections import deque

class myRangeException(Exception):
	pass

class myRange(object):
	def __init__(self, i=0, j=0, v=0, n=0):
		self.i = i # lower index
		self.j = j # upper index
		self.v = v # max value index
		self.n = n
		if v > n or v < 0:
			print 'Inconsistent '+str(self)
			self.possible = False
		else:
			self.possible = True

	def __repr__( self):
		if hasattr(self, 'p1') and hasattr(self, 'p2'):
			return ' (%d, %d ) = %d'%(self.i, self.j, self.v)+' ( from '+str(self.p1)+' + '+str(self.p2)+' )'
		else:
			return ' (%d, %d ) = %d'%(self.i, self.j, self.v)

	def check_intersection(self, r2):
		if ( r2.i < self.i and self.i < r2.j < self.j):
			# left intersection
			# create a new range
			new_range = myRange( r2.i, self.j, max(self.v, r2.v), self.n)
			new_range.p1 = self
			new_range.p2 = r2
			return new_range
		elif r2.j > self.j and self.i < r2.i < self.j:
			# right intersection - create a new range
			new_range = myRange( self.i, r2.j, max(self.v, r2.v), self.n)
			new_range.p1 = self
			new_range.p2 = r2
			return new_range
		else:
			return None

	def __eq__(self, other):
		if other.i == self.i and other.j == self.j:
			if (other.v != self.v) or (self.possible==False or other.possible==False) :
				self.possible = False
				other.possible = False
				print 'Inconsitent for range '+str(self)+' and '+str(other)
				raise myRangeException
			return True
		return False



	def check_consistency(self, r2):
		if type(r2) != myRange:
			raise TypeError

		if self.possible == False or r2.possible == False:
			return False

		if r2.i == self.i and r2.j == self.j:
			if r2.v != self.v:
				self.possible = False
				r2.possible = False
				print 'Inconsitent for range '+str(self)+'\n and '+str(r2)
				raise myRangeException
			else:
				r2 = self # drop r2.

		if r2.i >= self.i and r2.j <= self.j:
			# new range is properly contained
			if r2.v <= self.v:
				pass # consistent. do nothing.
			else:
				self.possible = False
				r2.possible = False
				print 'Inconsitent for range '+str(self)+'\n and '+str(r2)
				raise myRangeException
		elif r2.i <= self.i and r2.j >= self.j:
			# new range properly contains
			if r2.v >= self.v:
				# consistent
				pass
			else :
				self.possible = False
				r2.possible = False
				print 'Inconsitent for range '+str(self)+'\n and '+str(r2)
				raise myRangeException
		elif (r2.i < self.i and r2.j < self.i) or (r2.i > self.j and r2.j > self.j):
			# no intersection - values should not be identical
			if r2.v == self.v:
				self.possible = False
				r2.possible = False
				print 'Inconsistent for range '+str(self)+'\n and '+str(r2)
				raise myRangeException
		return self.possible


def insert_in_range(range_list, elem):
	'''
	 check for intersections only with top level insertions. next level insertions should be consistent.
	'''
	for ii in range(len(range_list)):
		if range_list[ii] == elem: #this element is a duplicate - skip futher processing
			return

	range_list.append(elem)
	for ii in range(len(range_list)-1):
		r_int = elem.check_intersection(range_list[ii])
		if r_int:
			insert_in_range(range_list, r_int  )


def possible(n, A, B, ans):
	"""
	determine impossibility through exceptions
	"""
	try:
		range_list = []
		for (i,j,v) in zip( A, B, ans):
			rr = myRange(i,j,v, n)
			insert_in_range(range_list,rr)
		print 'done inserting'
		for i1 in range(len(range_list)-1):
			for i2 in range(i1+1, len(range_list)):
				range_list[i1].check_consistency(range_list[i2])

	except myRangeException:
		return "impossible"

	return 'possible'




	# for i1 in range(len(range_list)-1):
	# 	for i2 in range(i1+1, len(range_list)):



# possible
n=2738523;
A=[1541800, 988504, 1528727, 696836, 454177, 1066571, 424272, 73695, 1598121, 1219402, 1675969, 192318, 1814014, 63105, 538232, 1468384, 363201, 1276898, 558156, 257580, 384430, 966310, 1169171, 1717026, 934537, 132633, 416351, 500053, 1275104, 1078298, 39365, 494612, 1919394, 154489, 1034676, 31716, 1243034, 1242819, 179898, 327590, 18199, 669192, 547512, 1168398, 624303, 1086188, 1158414, 1139636, 357531, 1449062];
B =[2531801, 1085659, 2728738, 1856399, 911207, 2023446, 1883209, 2521782, 1845559, 2065943, 2310352, 631683, 2233280, 1670089, 2327887, 2391573, 2464567, 1367801, 756128, 2478515, 1113951, 1127846, 2167291, 2334493, 2609148, 2531774, 547698, 1260463, 2577562, 1642588, 784606, 758127, 2259619, 2316590, 1276119, 2346378, 2506225, 2462810, 1338830, 510108, 859650, 1539994, 2105727, 1924045, 978603, 1099568, 1570926, 2332162, 2205942, 1943762];
ans=[2738518, 2738488, 2738521, 2738522, 2738520, 2738522, 2738522, 2738523, 2738510, 2738522, 2738518, 2738523, 2738518, 2738523, 2738522, 2738518, 2738523, 2738519, 2738520, 2738523, 2738523, 2738515, 2738522, 2738518, 2738522, 2738523, 2738509, 2738520, 2738519, 2738522, 2738523, 2738520, 2738518, 2738523, 2738522, 2738523, 2738522, 2738522, 2738523, 2738523, 2738523, 2738522, 2738522, 2738522, 2738520, 2738515, 2738522, 2738522, 2738523, 2738510];

# imossible
n=967715196;
A=[88070817, 230926206, 325402891, 67438878, 414854212, 448608777, 447411302, 402701633, 63920122, 547251201, 405530066, 295499865, 266043774, 178565581, 282043734, 492107493, 124769257, 243274001, 235763969, 14915406, 447228966, 620019792, 428164980, 160021290, 638706136, 353466671, 4907257, 441453820, 150837720, 376584229, 359180965, 52059307, 209535746, 108731952, 145730299, 444188696, 707616768, 531377038, 168990140, 474793237, 400291809, 403401309, 23246747, 18323046];
B=[784667553, 945222384, 344321543, 169186998, 704157886, 629669912, 869861032, 445202858, 278103831, 891465176, 528072310, 465912208, 531388485, 304837533, 566836681, 728490581, 962975148, 386722625, 284279148, 961190226, 800554693, 847878146, 930610331, 712383532, 889293681, 863268951, 952811684, 553925766, 682720671, 582286731, 753458796, 908175081, 273153630, 947454081, 888339002, 841763443, 751783011, 896815164, 364175759, 823004808, 601828205, 807419443, 81212787, 46483440];
ans =[263681972, 364068241, 832281850, 600207943, 696434195, 547008745, 147563697, 538545428, 339726098, 743568392, 717028317, 351201058, 425937728, 136228805, 396220216, 432463590, 635987514, 26901202, 759119627, 753128332, 461248758, 966211051, 890198656, 85452424, 111074511, 266064476, 837627775, 86773324, 735849006, 184384425, 535302811, 75970174, 473599425, 181641516, 535617984, 713228337, 873640192, 754985815, 823877489, 847513731, 937230638, 815789756, 19416317, 854555658]

possible(n, A, B, ans)
