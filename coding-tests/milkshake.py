#!/usr/bin/python
# coding=utf-8
#
# http://code.google.com/codejam/contest/dashboard?c=32016#s=p1
# Problem
#
# You own a milkshake shop. There are N different flavors that you can prepare, and each flavor can be prepared
# "malted" or "unmalted". So, you can make 2N different types of milkshakes.
#
# Each of your customers has a set of milkshake types that they like, and they will be satisfied if you have at least
#  one of those types prepared. At most one of the types a customer likes will be a "malted" flavor.
#
# You want to make N batches of milkshakes, so that:
# •There is exactly one batch for each flavor of milkshake, and it is either malted or unmalted.
# •For each customer, you make at least one milkshake type that they like.
# •The minimum possible number of batches are malted.
# Find whether it is possible to satisfy all your customers given these constraints, and if it is, what milkshake
# types you should make.
# If it is possible to satisfy all your customers, there will be only one answer which minimizes the number of malted
#  batches.
#
#
#
# Input
# One line containing an integer C, the number of test cases in the input file.
# For each test case, there will be:
# One line containing the integer N, the number of milkshake flavors.
# One line containing the integer M, the number of customers.
# M lines, one for each customer, each containing:
#   An integer T >= 1, the number of milkshake types the customer likes, followed by
#   T pairs of integers "X Y", one for each type the customer likes, where X is the milkshake flavor between 1 and N
#   inclusive, and Y is either 0 to indicate unmalted, or 1 to indicated malted.
# Note that:
# No pair will occur more than once for a single customer.
# Each customer will have at least one flavor that they like (T >= 1).
# Each customer will like at most one malted flavor. (At most one pair for each customer has Y = 1).
#
# All of these numbers are separated by single spaces.
#
# Output
#
# C lines, one for each test case in the order they occur in the input file, each containing the string "Case #X: "
# where X is the number of the test case, starting from 1, followed by: ◦The string "IMPOSSIBLE", if the customers'
# preferences cannot be satisfied; OR
# ◦N space-separated integers, one for each flavor from 1 to N, which are 0 if the corresponding flavor should be
# prepared unmalted, and 1 if it should be malted.
#
# Limits
#
# Small dataset
# C = 100
#  1 <= N <= 10
#  1 <= M <= 100
#
# Large dataset
# C = 5
#  1 <= N <= 2000
#  1 <= M <= 2000
#
# The sum of all the T values for the customers in a test case will not exceed 3000
#
# Input
#
#  2
#  5
#  3
#  1 1 1
#  2 1 0 2 0
#  1 5 0
#  1
#  2
#  1 1 0
#  1 1 1
#
# Output
#
# Case #1: 1 0 0 0 0
#  Case #2: IMPOSSIBLE


__author__ = 'fjanoos'

from optparse import OptionParser
import sys
from collections import defaultdict


""" iterate through each flavor and find one that absolutely needs to be malted. because there is a customer who only
 drinks that flavor malted. If so, mark it malted and remove it and all satisfied customers from the matrix.
 repeat until no unsatisfied customers
 """

def solve_milkshake( N, M, cust_list ):
	"""
	sol: solution so far -1 -> this guy is still available
	cust_avail: this customer needs to be satisfied
	cust_list: preferences for each customer
	"""

	sol = [-1]*N
	c_unsat = [True]*M

	while True in c_unsat:
		chng_flg = False  # test if the loop has changed something

		for ci in [ i for i in range(M) if c_unsat[i] ]: # iterate through unsatisifed customers
			cust_needs = cust_list[ci]
			# see if we can satisfy him with assigned flavors
			for nd_fl in cust_needs.keys():
				if sol[nd_fl] == cust_needs[nd_fl]:
					c_unsat[ci] = False # he's satisfied
					chng_flg = True
					break

			if 	c_unsat[ci]: # still unsatisfied
				# can we satisfy him with an available flavor
				avail_flvs = [flv for flv in  set(cust_needs.keys()) & set( [i for i in range(N) if sol[i]==-1] ) ]
				if len(avail_flvs) == 0:
					return None
				if len(avail_flvs)==1: #the customer can only be satified with this one flavor
					sol[avail_flvs[0]] = cust_needs[avail_flvs[0]] # select this flavor
					c_unsat[ci] = False
					chng_flg = True

		if not chng_flg : #nothing changed - why is that ?
			if True in c_unsat:
				print 'fuckup'

				# test for solution consistency !
				sol2 = [0 if sol[i]==-1 else sol[i] for i in range(N)]
				c_unsat2 = [True]*M
				for flv in range(N):
					for c in [ i for i in range(M) if c_unsat2[i] ]: # all unsatisfied customers
						if sol2[flv] == cust_list[c][flv]:
							c_unsat2[c] = False
				if True in c_unsat2: # no consistent solution !
					return None
				else :
					break
			else:
				# all customers satisfied
				break

	return [0 if sol[i]==-1 else sol[i] for i in range(N)] # convert any unassigned guy to 0



if __name__ == "__main__":
	usage = \
		'''  %prog [options] input_filename out_filename
				   runs the milkshake problem via constraint satisfiability ''';
	option_parser = OptionParser( usage )
	option_parser.add_option( "-v", "--verbose", action = "store_true", dest = "verbose", default = False );

	(options, args) = option_parser.parse_args( )

	if len( args ) < 1:
		#option_parser.error("incorrect number of arguments")
		option_parser.print_help( );
		sys.exit( );

	if options.verbose:
		print 'solving file ' + args[0]

	if len( args ) == 2:
		outfile = open( args[1], 'w' )
		if options.verbose:
			print 'writing to ' + args[1]
	else:
		outfile = sys.stdout

	#fp = open('milkshake_small.in','r')

	with open( args[0], 'r' ) as fp:
		n_cases = int( fp.readline( ) )
		for case in range( n_cases ):
			if options.verbose: print case

			N = int( fp.readline( ) )
			M = int( fp.readline( ) )

			# flavour by customer matrix - -1 is no-choice, 0 is unmalted, 1 is malted
			cust_list = {}

			for cust in range(M):

				row = [int( x ) for x in fp.readline( ).split( )]
				T = row[0]
				cust_list[cust]= defaultdict( lambda : -2 )
				for fc in range(T):
					f = row[2*fc+1]-1; t =  row[2*fc+2];
					cust_list[cust][f] = t

				# if options.verbose:
				# 	print 'Case #:'+str(case+1)+' cust_list ' + str( cust_list ) ;

			sol = solve_milkshake( N,M, cust_list )
			if sol:
				sol_str = ' '.join(map(str, sol) )
			else:
				sol_str = 'IMPOSSIBLE'

			outfile.write( 'Case #%d: %s\n' %(case + 1,sol_str)  )

	if outfile != sys.stdout:
		outfile.close()
