#!/usr/bin/python
# coding=utf-8

# Problem http://code.google.com/codejam/contest/dashboard?c=32016#s=p1
#
# You are given two vectors v1=(x1,x2,...,xn) and v2=(y1,y2,...,yn). The scalar product of these vectors is a single
# number, calculated as x1y1+x2y2+...+xnyn.
#
# Suppose you are allowed to permute the coordinates of each vector as you wish. Choose two permutations such that
# the scalar product of your two new vectors is the smallest possible, and output that minimum scalar product.
#
# Input
# The first line of the input file contains integer number T - the number of test cases. For each test case,
# the first line contains integer number n. The next two lines contain n integers each, giving the coordinates of v1
# and v2 respectively.
#
# Output
#
# For each test case, output a line
# Case #X: Y
# where X is the test case number, starting from 1, and Y is the minimum scalar product of all permutations of the
# two given vectors.
#
# Limits
# Small dataset
# T = 1000
#  1 ≤ n ≤ 8
#  -1000 ≤ xi, yi ≤ 1000
#
# Large dataset
# T = 10
#  100 ≤ n ≤ 800
#  -100000 ≤ xi, yi ≤ 100000
#
#
# Input
#  2
#  3
#  1 3 -5
#  -2 4 1
#  5
#  1 2 3 4 5
#  1 0 1 0 1
#
# Output
# Case #1: -25
#  Case #2: 6
"""
Solved using DP
"""

__author__ = 'fjanoos'

from optparse import OptionParser
import sys


def solve_msp( a, b ):
	assert type( a ) is list and type( b ) is list and len( a ) == len( b )
	a.sort( );
	a.reverse( );
	b.sort( )
	return reduce( lambda tot, abi:tot + abi[0] * abi[1], zip( a, b ), 0 )


if __name__ == "__main__":
	usage = \
		'''  %prog [options] input_filename out_filename
				   runs the minimum scalar problem using DP ''';
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

	with open( args[0], 'r' ) as fp:
		n_cases = int( fp.readline( ) )
		for case in range( n_cases ):
			d = int( fp.readline( ) )
			a = [int( x ) for x in fp.readline( ).split( )]
			b = [int( x ) for x in fp.readline( ).split( )]
			if options.verbose:
				print 'Case # ' + str( case + 1 ) + ' a=' + str( a ) + ' b=' + str( b );

			if len( a ) != d or len( b ) != d:
				print 'Case ' + str( case + 1 ) + 'incorrect vector size '
				continue

			sol = solve_msp( a, b )
			outfile.write( 'Case #%d: %d\n' % (case + 1, sol) )

	outfile.close()




