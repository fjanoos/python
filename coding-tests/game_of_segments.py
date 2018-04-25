# Problem Statement for GameOfSegments
# http://community.topcoder.com/stat?c=problem_solution&cr=23023058&rd=15857&pm=13204
#
# Initially, there is a polygon with N vertices drawn in the plane. The polygon is strictly convex, i.e.,
# each internal angle is strictly smaller than 180 degrees. The vertices of the polygon are numbered 1 through N,
# in clockwise order.
#
# Two players play the game on this polygon. The players take alternating turns. In each turn, the current player
# chooses a diagonal or a side of the polygon and draws it as a straight line segment. (A diagonal of the polygon is
# a line segment that connects any two non-adjacent vertices of the polygon.) The player is only allowed to choose a
# diagonal or a side that does not intersect any of the previously drawn segments (it must not share endpoints with
# any of them either). The player who cannot draw a diagonal or a side according to the above rules loses the game.

# You are given the int N.
# We assume that both players play the game optimally. Return 1 if the first player wins and 2 otherwise.
#
#
# Definition
#
# Class:	GameOfSegments
# Method:	winner
# Parameters:	int
# Returns:	int
# Method signature:	int winner(int N)
# (be sure your method is public)
#
#
# Constraints
# -	N will be between 3 and 1,000, inclusive.
#
# Examples
# 0)
# 3
# Returns: 1
# This polygon has zero diagonals and three sides. The first player will always win no matter which side he picks.
#
# 1)
# 4
# Returns: 1
# This polygon has four sides and two diagonals. The first player wins the game if he takes one of the diagonals,
# because he will leave no choice for the second player.
#
# 2)
# 15
# Returns: 2

# 3)
# 191
# Returns: 2
#

"""
It comes down to counting the total number of non-intersecting diagonals possible. Due to symmetry, we can start with
any side. I conjecture that the total number of diagonals possible is a function of the number of vertices, not the
drawing strategy.

Therefore count total number of triangles.

Take a non-adjacent set of vetices, draw a triangle. drop the edge -

NOTE: this is wrong - because the edge must NOT share endpoints with previously drawn edges.

This requires a tree search. Player one starts by drawing edge (1,i), i = 2... N. This paritions the problem into 2
convex polygons involving points on either side of the partition, modulo the edge itself.

DOES NOT MATCH EXPECTED RESULTS FOR ALL CASES - ONLY FOR  A FEW !
"""
__author__ = 'fj'

from math import ceil


# turn_list = {};
# def explore_game_tree(N, start_idx, player, turn_count):
#
# 	if player==1:
# 		move_flg = False;
# 		for i in range(2,N):
# 			if (i == 2 or i == 3):			# no LHS polygon - only examine the rhs polygon.
# 				if not find_odd_edge_solution( N - i ) : move_flg = True;
# 			if (N - i <= 1):				# no RHS poly - only examine LHS poly
# 				if not find_odd_edge_solution(i-2): move_flg = True;
# 			elif ( not ( find_odd_edge_solution( i-2 ) and find_even_edge_solution( N - i ) ) ) \
# 				and ( not( find_even_edge_solution( i-2 ) and find_odd_edge_solution( N - i ) ) ):
# 				move_flg = True;
#
# 				turn_list[turn_count] = (start_idx, )


def find_odd_edge_solution(N):
	"""
	find an an odd solution solution from an N-vertex polygon
	"""
	if N < 1:
		return False
	try:
		find_odd_edge_solution.table[N]
	except KeyError:
		find_odd_edge_solution.table[N] = False
		for i in range(2, N) : #int(ceil(N/2.0)+2)) :
			# if I draw edge (1,i) - can my opponent find an odd edge count solution to the remaining 2 polygons ?
			# If he cannot, then this move will give me an odd number of edges.
			if (i == 2 or i == 3):			# no LHS polygon - only examine the rhs polygon.
				if not find_odd_edge_solution( N - i ) : find_odd_edge_solution.table[N] = True; break
			elif (N - i <= 1):				# no RHS poly - only examine LHS poly
				if not find_odd_edge_solution(i-2): find_odd_edge_solution.table[N] = True; break
			elif ( not ( find_odd_edge_solution( i-2 ) and find_even_edge_solution( N - i ) ) ) \
				and ( not( find_even_edge_solution( i-2 ) and find_odd_edge_solution( N - i ) ) ):
				# examine both sides of the split.
				find_odd_edge_solution.table[N] = True
				break

	return find_odd_edge_solution.table[N]


find_odd_edge_solution.table = {1:False, 2:True, 3:True}

def find_even_edge_solution(N):
	"""
	find an an even solution solution from an N-vertex polygon
	"""
	if N < 1:
		return False

	try:
		find_even_edge_solution.table[N]
	except KeyError:
		find_even_edge_solution.table[N] = False
		for i in range(2, N): # int(ceil(N/2.0)+2)):
			# if I draw edge (1,i) - can my opponent find an even edge count solution to the remaining 2 polygons ?
			# If he cannot, then this move will give me an even number of edges.
			if (i == 2 or i == 3):  # no LHS polygon - only examine the rhs polygon.
				if not find_even_edge_solution( N - i ) : find_even_edge_solution.table[N] = True; break
			elif (N - i <= 1):				# no RHS poly - only examine LHS poly
				if not find_even_edge_solution(i-2): find_even_edge_solution.table[N] = True; break
			elif ( not ( find_even_edge_solution( i-2 ) and find_even_edge_solution( N - i ) ) ) \
				and ( not( find_odd_edge_solution( i-2 ) and find_odd_edge_solution( N - i ) ) ):
				# examine both sides of the split.
				find_even_edge_solution.table[N] = True
				break

	return find_even_edge_solution.table[N]

find_even_edge_solution.table = {1:False, 2:False, 3:False}



if __name__=='__main__':
	N = 15;
	find_odd_edge_solution(N)



def count_edges(N):
	if N == 3:
		return 3
	else:
		return 2 + count_edges(N-1)


count_edges(3)



