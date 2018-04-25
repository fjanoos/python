# Problem Statement for ReflectiveRectangle: http://community.topcoder.com/stat?c=problem_statement&pm=13217
#
# Raymond has a rectangle with dimensions sideA times sideB. The sides of the rectangle are perfect mirrors.
# There is a directional light source in one corner of the rectangle.
# Raymond can point the light source in any direction. (I.e., he can choose any angle strictly between 0 and 90 degrees.
# The chosen angle does not have to be an integer.) When Raymond turns the light source on, it will shine a ray of light
# into the rectangle. The light follows the law of reflection: whenever it hits a mirror, the angle of incidence
# equals t
# he angle of reflection.
#
# Raymond's goal is to shine the ray of light in the following way:
# The light must bounce off the sides of the rectangle exactly bounces times, without hitting a corner of the rectangle.
# After exactly that many bounces, the light must reach the opposite corner.
#
#
# Raymond found all solutions to the above problem. In other words, he found all choices of the initial angle that lead
# to the desired outcome. He then took a sheet of paper. For each of the solutions, he computed the square of the
# distance the light traveled before hitting the opposite corner, and he wrote down the result. (Note that the squared
# distance is always an integer.)
#
# You are given the ints sideA, sideB, and bounces. Return the sum of all numbers on Raymond's paper, modulo 10^9 + 7.
#
# Definition
#
#
# Class: ReflectiveRectangle
# Method: findSum
# Parameters: int, int, int
# Returns: int
# Method signature: int findSum(int sideA, int sideB, int bounces)
# (be sure your method is public)
#
# Constraints
#
# - sizeA will be between 1 and 10^6, inclusive.
# - sizeB will be between 1 and 10^6, inclusive.
# - bounces will be between 0 and 10^9, inclusive.
#
# Examples
#
# 0)
# 3
# 4
# 0
# Returns: 25
# As there should be 0 bounces, Raymond has to point the light source directly at the opposite corner. The squared
# ength of that light beam will be 3^2 + 4^2 = 25.
#
#
# 1)
# 3
# 3
# 2
#
# Returns: 180
# There are two possible paths, each with squared length 90.
#
# 2)
# 13
# 17
# 1
# Returns: 0
# Sometimes, it is not possible to find any valid path that satisfies the conditions.
#
# 3)
# 59325
# 31785
# 262142
# Returns: 48032850
# Don't forget to take the answer modulo 10^9+7.
#
# 4)
# 1000000
# 1000000
# 1000000000
# Returns: 145972110
# Be careful with overflow.
#
# more tests at http://community.topcoder.com/stat?c=problem_solution&cr=14970299&rd=15859&pm=13217

""" My solution idea : rather than calculating reflections for different angles, a reflection is a modulo operations -
ie the rectangle flips across an edge and the ray continues straight on. See the careers page of onenote for diagram.
So basically, for each bounce flip the rectangles across their edges. For a final solution with n-bounces,
find a sequence
of flips, so that
a) the sink is an extreme point of the last flip (ie not an internal vertex of the rectangular mozaic)
b) there is path from source to sink that is entirely within the rectangle-mozaic and passes through every rectangle.
The length and breadth do not matter - we can replace rectangles with unit-squares and scale later.
This is actually a line drawing algorithm.
We want to draw a line through (left,bottom) moves with squares (replace rectangle) and make sure that we can a) with
n-flips (i.e. lines) make sure that the dest corner is bottom right at the end and
b) the line does not pass through vertices.
----------------------------------------------------------------------------------------------------------------------
This is even easier !! Consider the parquet of (N+1)x(N+1) rectangles tiled to each other.
Let N be an even number. Odd number of flips cause the BR corner to be an interal vertex, while even number of flips
causes the BR corner to be an external vertex in BR position
In N bounces, the rectangles that reachable by a straight line from (0,0) are
  (0,N)
  (1,N-1)  -> not valid (BR is not extreem point)
  (2,N-2) ->  valid
  ...
  (N/2, N/2)  ->> this one requires a corner only solution - not acceptable !!
  ...
  (N,0)

  Therefore the total length is
  (if N/2 odd) (the N/2, N/2 rectangle is not an issue)
  \sum_{i=0}^N/2 ((2i+1)h)^2 + \sum_{i=0}^N/2 ((2i+1)b)^2

   Let M = N/2
   Now \sum_{i=0}^M (2i+1)^2 =  \sum (4i^2 + 4i)  + (M+1)  =  4M(M+1)(2M+1)/6 + 4 M(M+1)/2 + M+1 ]

  (if N/2 even) (the N/2, N/2 rectangle shows up - but is invalid due to a corner only solution)
  \sum_{i=0}^N/2 ((2i+1)h)^2 + \sum_{i=0}^N/2 ((2i+1)b)^2 - ((N/2+1)h)^2 - ((N/2+1)b)^2

  Actually - corners are hit even more often than the above would suggest

  for a particular rectangle (m,n) the br corner is (m+1) and (n+1).
   Now if (m+1) = a(d) and n+1 = a(c) - then the ray will also pass through
   the corner (d,c) - and therefore it is invalid solution.
   Therefore, m and n must be relatively prime.
"""

__author__ = 'fjanoos'

from pylab import *
import numpy as np
import math
from collections import deque
from itertools import combinations

# compute sum of suqares
sos = lambda n:n * (n + 1) * (2 * n + 1) / 6


def get_prime_factors( N ):
	n = int( N ** 0.5 ) + 1
	primes = []

	for i in xrange( 2, n ):
		if not mod( N, i ):
			primes.append( i )
			while not mod( N, i ):
				N /= i
	if N > 1:
		primes.append( N )
	return primes


def get_power_set( S ):
	pset = []
	for l in range( 0, len( S )+1 ):
		pset.extend( combinations( S, l ) )
	return pset


def faster_solution( H = 1, B = 1, nb = 0 ):
	"""
	 handles the relatively prime case usign the logic as follows

	Define N = nbounces + 2
	(m,n) = br corner coordinates
	therefore all possible solutions are m+n = N
	If (m,n) are not coprime - ie. there exist (p,q) such that (m,n) = alpha.(p,q), then the ray will pass through
	 corner (p,q) also.
	But if (m,n) = a (p,q) then a must be a factor of N - because ap + aq = N ==> N/a = integer !!
	Therefore, we iterate through all (m,n) and the subtract out the contribution due to all prime factors of N !

	Nope !! we cannot subtract out all primes - because of double coutning. (i.e. if 6 is a common factor, then we
	double subtract out 2 and 3. Instead we need to apply an inclusion exclusion prinicple here - subtract out 2,3,5
	but add back 6, 10, 15, but then subtract out 30

	"""
	if nb % 2:
		return -1
	N = nb + 2;
	m_factor = (H ** 2 + B ** 2);
	total_len =  0 # sos( N )
	for primes in get_power_set( get_prime_factors( N ) ):
		val = long(prod( primes ))
		total_len += val**2 * sos(N/val)*(-1 if len(primes)%2 else 1)
	return long(m_factor*total_len)%(10 ** 9 + 7)


def is_coprime( a, b ):
	if a < b:
		c = a;
		a = b;
		b = c;

	while b != 0:
		t = b;
		b = mod( a, b );
		a = t;

	return a == 1;


def fast_solution( H = 1, B = 1, nb = 0 ):
	"""
	 handles the relatively prime case. but doesn'twork for large cases.
	"""
	if mod( nb, 2 ) > 0:  # no solution for odd bounces
		return 0
	M = nb / 2
	total_len = 0
	for i in xrange( 0, int( floor( M / 2 ) ) + 1 ):
		m = (2 * i + 1)
		n = 2 * (M - i) + 1
		if is_coprime( m, n ):
			total_len = mod( total_len + (H * m) ** 2 + (B * n) ** 2 + (H * n) ** 2 + (B * m) ** 2, 10 ** 9 + 7 )
	return total_len


def fast_solution_v1( H = 1, B = 1, nb = 0 ):
	if mod( nb, 2 ) > 0:  # no solution for odd bounces
		return 0

	M = nb / 2
	total_len = (H ** 2 + B ** 2) * ( 2 * M * (M + 1) * (2 * M + 1) / 3 + 2 * M * (M + 1) + M + 1 )

	if mod( M, 2 ) == 0:
		total_len = total_len - (M + 1) * 2 * (H ** 2 + B ** 2);

	return mod( total_len, 10 ** 9 + 7 )


# propose all feasible flips so that at least one line passes through all unit-squares - except for only through the
# vertices
def propose_valid_flips( last_flip, H = 1, B = 1 ):
	"""
	last_flip : {flip: [0,1],  TL: (top,left), dst:('bl', 'br', 'tl', 'tr'), angles:(min,max) ,
				 n_ref:int, n_bef:int,
				 nb: number of bounces left}
	here flip=0 => flip right, flip=1 => flip down
	dst keeps track of the destination vertex
	angles: keeps track of the min-feasible and max-feasible angle for this flip sequence. (downward angle wrt
	horizontal axis)
	n_ref: number of rigth edge flips so far
	n_bef: number of bottom edge flips so far
	H: height
	B: breadth
	"""

	min_ang = last_flip['angles'][0]
	max_ang = last_flip['angles'][1]
	if min_ang >= max_ang:
		# not a good solution. equality implies that the ray passes through an extreme point.
		return []

	feasbile_flips = [];

	# test the right edge flip
	TL = ( last_flip['TL'][0], last_flip['TL'][1] + B )
	new_dst = 'r' if last_flip['dst'][1] == 'l' else 'l'
	dst = last_flip['dst'][0] + new_dst
	new_max_ang = math.atan2( TL[0] + H, TL[1] )  # defined by BL corner
	new_min_ang = math.atan2( TL[0], TL[1] + B )  # defined by TR corner
	new_max_ang = min( new_max_ang, max_ang )
	new_min_ang = max( new_min_ang, min_ang )
	if new_max_ang >= new_min_ang:
		# feasible !!
		feasbile_flips.append( { 'flip':0, 'TL':TL, 'dst':dst, 'angles':(new_min_ang, new_max_ang),
		                         'n_ref':last_flip['n_ref'] + 1, 'n_bef':last_flip['n_bef'],
		                         'nb':last_flip['nb'] - 1 } )

	# test the bottom edge flip
	TL = ( last_flip['TL'][0] + H, last_flip['TL'][1])
	new_dst = 't' if last_flip['dst'][0] == 'b' else 'b'
	dst = new_dst + last_flip['dst'][1]
	new_max_ang = math.atan2( TL[0] + H, TL[1] )  # defined by BL corner
	new_min_ang = math.atan2( TL[0], TL[1] + B )  # defined by TR corner
	new_max_ang = min( new_max_ang, max_ang )
	new_min_ang = max( new_min_ang, min_ang )
	if new_max_ang >= new_min_ang:
		# feasible !!
		feasbile_flips.append( { 'flip':1, 'TL':TL, 'dst':dst, 'angles':(new_min_ang, new_max_ang),
		                         'n_ref':last_flip['n_ref'], 'n_bef':last_flip['n_bef'] + 1,
		                         'nb':last_flip['nb'] - 1 } )
	return feasbile_flips


def explore_flip_sequence( nb, curr_flip, H = 1, B = 1 ):
	"""
	bfs through the tree of flip sequences
	nb : number of bounces left
	"""
	# at the end of the recursion
	if nb == 0:
		return [] if curr_flip['dst'] != 'br' or curr_flip['angles'][0] > curr_flip['angles'][1] else [curr_flip]

	flp_seq = []
	if nb >= 1:
		ff = propose_valid_flips( curr_flip, H, B )  # get next level of valid flips
		for flp in ff:
			# explore pendant tree to
			pend_tree = explore_flip_sequence( nb - 1, flp, H, B )
			for lf in pend_tree:
				flp_seq.append( lf )
	return flp_seq


def iterate_flip_sequence( nb, start, H = 1, B = 1 ):
	"""
	go through the tree of flip sequences using bfs
	nb : number of bounces left
	"""

	solutions = []

	flp_q = deque( )
	flp_q.append( start )

	try:
		while True:
			curr_flp = flp_q.pop( )
			# get all the valid sub-flips from the curr flip
			valid_flps = propose_valid_flips( curr_flp, H, B )
			for ff in valid_flps:
				if ff['nb'] == 0:  # is the end of the tree,
					ray_ang = math.atan2( ff['TL'][0] + H, ff['TL'][1] + B )  #angle of ray to BR corner
					if ff['dst'] != 'br':
						#  dest vertex not in correct position
						pass
					elif ff['angles'][0] > ff['angles'][1]:
						# angle min < angle max is not hold
						pass
					elif ff['TL'][0] == ff['TL'][1]:
						# diagonal solution
						pass
					elif ray_ang > ff['angles'][1] or ray_ang < ff['angles'][0]:
						# the ray to BR corner does not pass through rect
						pass
					else:
						yield ff  #solutions.append(ff)
				else:
					# internal flip - add to the tree
					flp_q.append( ff )
	except IndexError:
		# end of the stack
		return


if __name__ == "__main__":

	faster_solution( 1000000, 1000000, 1000000000 )

	H = 59325;
	B = 31785;
	nb = 262142
	start = { 'flip':0, 'TL':(0, 0), 'dst':'br', 'angles':(0, pi / 2), 'n_ref':0, 'n_bef':0, 'nb':nb }
	# there is a symmetry of solutions - so go only one way
	first_flps = propose_valid_flips( start, H, B )

	sols = iterate_flip_sequence( nb, start, H = 1, B = 1 )

	total_sq_dist = 0;
	for s in sols:
		curr_len = ((s['n_bef'] + 1) * H) ** 2 + ((s['n_ref'] + 1) * B) ** 2
		total_sq_dist = mod( total_sq_dist + curr_len, 10 ** 9 + 7 )
		print 'len= %g' + 'for ' + repr( s ) % curr_len

	print 'solution is %g' % (total_sq_dist)