__author__ = 'fj'
# Problem Statement
#
# Hero is preparing a party for his friends. He has a round table with N seats. The seats are numbered 0 through N-1,
#  in order. In other words, seats with consecutive numbers are adjacent, and seat N-1 is adjacent to seat 0.
#
# Hero knows that exactly K friends will attend the party, and that each of them will arrive at a different time.
# Each time a new friend arrives, Hero has to assign him (or her) one of the empty seats at the table. The friend
# then sits there for the rest of the party. Hero is not sitting at the table.
#
# For the purpose of this problem, a cluster is a maximal group of people that occupy consecutive chairs. For
# example, if there are people on chairs 3, 4, 5, and 6, while chairs 2 and 7 are empty, then these four people form
# a cluster.
#
# At a party, clusters are good: people who sit in a cluster can talk to each other and have fun. A party with too
# many clusters is bad. Therefore, Hero wants to make sure that at no point in time are there more than G clusters at
#  his table.
#
# For example, let N = 4 and K = 3. That is, we have a table with four seats, and three friends are going to arrive.
# We will use A, B, and C to denote the three friends (in the order in which they arrive) and a period ('.') to
# denote an empty chair. So, for example, "ABC." denotes that A got seat 0, B seat 1, C seat 2, and seat 3 remained
# empty. The configurations ".ABC" and "C.AB" are considered different from "ABC." and from each other: the friends
# sit in the same order but on different seats.
#
# Continuing our example, let G = 1. That is, we must never have more than one cluster. This constraint restricts the
#  set of possible final configurations. For example, "ABC.", "C.AB", "B.CA", and ".BAC" are all possible,
# but "A.BC" and ".ACB" are not. (Note that if the final configuration were "A.BC", then the configuration before C
# arrived was "A.B.", which means that there was more than one cluster at that point in time.)
#
# You are given the ints N, K, and G. Count the number of possible final configurations. Return that count modulo 1,
# 000,000,007.
#
#
# Definition
#
# Class:	Seatfriends
# Method:	countseatnumb
# Parameters:	int, int, int
# Returns:	int
# Method signature:	int countseatnumb(int N, int K, int G)
# (be sure your method is public)
#
#
# Constraints
# -
# N will be between 2 and 2000, inclusive.
# K will be between 1 and N, inclusive.
# G will be between 1 and K, inclusive.
#
#
# Examples
# 0)
# 3
# 2
# 1
# Returns: 6
# There are 6 ways how to seat your 2 friends: "AB.", "A.B", "BA.", "B.A", ".AB", and ".BA". All 6 are valid.
#
# 1)
# 4
# 2
# 1
# Returns: 8
# The first friend can take any of the four seats. The second one must then sit next to him (on either side). Thus,
# there are 4*2=8 valid final configurations.
#
# 2)
# 2
# 2
# 1
# Returns: 2
#
# 3)
# 5
# 4
# 2
# Returns: 120
#
# 4)
# 42
# 23
# 7
# Returns: 917668006

"""
For one cluster - sit the first guy in 1 of N chairs. Then the second guy has 2 options, 3rd has two options...
= N * 2^(K-1). Except if N = K. Then the last guy doesn't have a choice. So in that case N*2^(K-2).

For two clusters:
Split K folks into two groups in 2^K/2 ways (divide by 2! for symmetric solution) with sizes
  (0,K), (1,K-1) .... (K/2,K/2) .... (K,0) partitions.
The first group is unconditional seating ... (solution for 1 group with size i, N chairs) = N* 2^(i-1)
The second group has unconditional seating on (N-i-2) chairs = (N-i)
For (i,j) group slip, partition the table as (i, N-i) upto (N-j, j) ways.


Alternative logic:
For one group:
Select seat for A in N ways.
Select group to (left,right) of A of size (0,K-1) , (1,K-2) ... (K-1,0) : (K-1) partitions.
For each left partition of size i : select member in (K-1)C(i) ways. The ordering is fixed.
Therefore, total number of solutions:
N x \sum_i=0^(K-1) K-1 ! / i! (K-1-i)!  = N x (1+1)^(K-1) = Nx2^(K-1).


For two groups:
Split K folks into two groups with sizes (0,K), (1,K-1) .... (K/2,K/2) .... (K,0) partitions.
Group 1 of size i is chosen in K_C_i ways.

Seat first group unconditionally:  (solution for 1 group with size i, N chairs) = N* 2^(i-1)
For second group of size (K-1) we have (N-i-2) free spots to seat them. Select position for A from p = 1 to (N-i-2).
Select left group of size j= 0 to p-1 in  sum_j=0^(p-1) (K-i)_C_j ways.
So total options for group 2 are : sum_p=1^(N-i-2) sum_j=0^(p-1) (K-i)_C_j ways.
And total answer is  \sum_i=0^[K/2] K_C_i sum_p=1^(N-i-2) sum_j=0^(p-1) (K-i)_C_j


DID NOT WORK AS YET
"""

from pylab import *

def factorial(n):return reduce(lambda x,y:x*y,[1]+range(1,n+1))

def combinations(M,N) :
	if (M-N) < N:
		N = M-N  # make N the smaller of the two.
	return reduce( lambda x,y: x*y, [1]+range(M-N+1, M+1) )/factorial(N)


def group_ways( K, N ):
	"""
	For a group of size gs, with N chairs to sit in (without circularity) - compute the number of options.
	p - position of first guy. Consider options for the left solution. the right solution is symmetric.
	j - left group size.
	= sum_p=1^[N/2] \sum j=0^min(p-1,K-1) (K-1)_C_j

	Here [] is the floor operation.
	Therefore, if [N/2] < K
	= sum_p=1^[N/2] \sum j=0^(p-1)     (K-1)_C_j
	= sum_j=0^( [N/2]-1 ) sum_p={j+1}^[N/2] (K-1)_C_j =
	= sum_j=0^( [N/2]-1 ) ( [N/2]-j ) (K-1)_C_j
	handle the odd N case indepentely	with sum_j=0^[N/2] (K-1)_C_j

	If [N/2] >= K
	= sum_p=1^(K-1) \sum j=0^(p-1) (K-1)_C_j + ([N/2]-K+1) \sum_j=0^(K-1) (K-1)_C_j
	= \sum j=0^(K-2) \sum_p=(j+1)^(K-1)  (K-1)_C_j + ([N/2]-K+1) 2^(K-1)
	= \sum j=0^(K-2) (K-1-j)(K-1)_C_j + ([N/2]-K+1) 2^(K-1)
	And for the odd N case: add another 2^(K-1) !
	"""
	if N < K:
		return 0
	try:
		group_ways.precompute[ (K, N) ]
	except KeyError:
		group_ways.precompute[ (K, N) ] = 0

		if K == 1:
			group_ways.precompute[ (K, N) ] = N
		elif K == 2:
			group_ways.precompute[ (K, N) ] = (N-2)*2 + 2
		elif ceil(N/2.0) < K:
			for j in range(0, int(N/2) ):
					group_ways.precompute[ (K, N) ] += (int(N/2)-j)*combinations( K-1, j)
			group_ways.precompute[ (K, N) ] *= 2 # double the solution
			if N%2: # handle the odd case
				for j in range(0, int(N/2)+1 ):
					group_ways.precompute[ (K, N) ] += combinations( K-1, j)
		else:  # N/2 > K
			for j in range(0, K-1 ):
					group_ways.precompute[ (K, N) ] += (K-1-j)*combinations( K-1, j)
			# add in the residual positions where there are enough seats to the left to accomodate all members
			group_ways.precompute[ (K, N) ] += ( int(N/2)-K+1 )*2**(K-1)
			group_ways.precompute[ (K, N) ] *= 2 # double the solution
			if N%2: # handle the odd case
				group_ways.precompute[ (K, N) ] += 2**(K-1)

	return group_ways.precompute[ (K, N) ]

group_ways.precompute = {}


# this needs a recursive solution. K people can be divided into G clusters in G^K/ G! unique ways. Let the cluster
# containng individual 1 be cluster 1. This cluster can be seated in N ways and has size strictly greater than one

def recursive_count( N, K, G ):
	"""
	recursively count how K people can be subdivided into G clusters and be seated in N seats.
	"""

	if K <= 1:
		return 1
	elif N < K:
		return 0
	try:
		recursive_count.precompute[ (N, K, G) ]
	except KeyError:
		if G == 1:
			recursive_count.precompute[ (N, K, G) ] = 2**(K-1)
		else:
			recursive_count.precompute[ (N, K, G) ] = 0L
			for k in range(K+1):  # sizes of currrent group
				temp = 0L
				for gap in range(0, N-K+1 ):
					# gap to next group - must be atleast 1 but so large as to exhaust seats left
					# i.e. N-(k+gap) >= K - k ==> gap <= N - K
					temp += recursive_count( N-(k+gap), K-k, G-1 )
				# also handle the zero gap case - we need to ensure that one combination : the  member a of
				# current group in last position is not sequential to member a of adjoining group !
				recursive_count.precompute[ (N, K, G) ] += combinations(K,k)*(2**(k-1))*temp
	return recursive_count.precompute[ (N, K, G) ]
recursive_count.precompute = {}





def countseatnumb( N, K, G):
	"""
	seat the first group circularly. Seat every subsequent group using the partitioning formula.
	:param N:
	:param K:
	:param G:
	:return:
	"""

	# if N == K:
	# 	return 2**(K-1)
	# else:
	return mod( N * recursive_count( N, K, G ) , 1000000007)

print countseatnumb( 4,4,4)