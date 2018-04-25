# https://code.google.com/codejam/contest/3214486/dashboard
# Input
#
# The first line of the input gives the number of test cases, T. Each test case is a line containing an integer N
# which is the number of states Tom recorded and a list of the N states separated by spaces. Each state is encoded
# into a 7-character string represent the display of segment A-G, from the left to the right. Characters in the
# string can either be '1' or '0', denoting the corresponding segment is on or off, respectively.
#
# Output
#
# For each test case, output one line containing "Case #x: y", where x is the test case number (starting from 1). If
# the input unambiguously determines the next state of the display, y should be that next state (in the same format
# as the input). Otherwise, y should be "ERROR!".
#
# Limits
# 1  T  2000.
# Small dataset
#
# 1  N  5.
# Large dataset
#
# 1  N  100.
# Sample
#
#
# Input
#
# 4
# 1 1111111
# 2 0000000 0001010
# 3 0100000 0000111 0000011
# 5 1011011 1011111 1010000 1011111 1011011
#
#
# Output
#
# Case #1: 1110000
# Case #2: ERROR!
# Case #3: 0100011
# Case #4: 0010011

__author__ = 'fj'

from optparse import OptionParser
import sys
from copy import deepcopy

# the number table. this 2 shit is to avoid octal notation !
table =[ d- 21111110 for d in
		[ 20000000, #0
		  20110000, #1
		  20110000, #2
		  21111001, #3
		  20110011, #4
		  21011011, #5
		  21011111, #6
		  21110000, #7
		  21111111, #8
		  21110011, #9
	   ]
	  ]



def defective_table( seg, table ): # seg 0 corresponds to g, 6 to a
	dtab = []
	for d in range(len(table)):
		digit = table[d]
		if (digit / 10**seg)%2: # it has a one in the seg position
			digit = digit - 10**seg
		dtab.append(digit)
	return dtab

def solve_segments(n, states):
	global table

	#determine the defective pattern
	correct_si = -1

	for si in range(10): # test all start index
		tab = table
		sfsg = True # so far so good
		for seg in reversed(range(7)):
			dtab = defective_table(seg, table)
			pflg = False # is this segment defective ?

			def_flg = True # is this seg defective
			ok_flg = True # is this seg ok
			for t in range( n ):
				digit = table[(si - t) % 10]
				if states[t] / 10 ** seg != digit / 10 ** seg:
					ok_flg = False  # doesn't agree with the ok table


				digit = dtab[(si - t) % 10]
				if states[t] / 10 ** seg != digit / 10 ** seg:
					def_flg = False # doesn't agree with the def table'
				else: pflg = True # agrees with the defective table

			if (ok_flg or def_flg):	# this si agrees with an interpretation of the segments
				sfsg = True
				continue
			else:  # this si is inconsistent
				sfsg = False
				continue
		if pflg: # use defective table
				table = dtab

		if sfsg:
			correct_si = si


	last_state = n % 10
	next_state = table[ (last_state - 1)%10 ]
	return next_state




n = 1
states = [1111111]
solve_segments(n, states)




option_parser = OptionParser("input_filename op_fname")
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
		row = [ int(x)  for x in fp.readline( ).split( )]
		n = row[0]
		states = row[1:]
		if options.verbose:
			print 'Case# ' + str( case + 1 ) + ' n=' + str( n ) + ' states=' + str( states );

		sol = solve_segments(n, states)
#
#
# 		sol = solve_msp( a, b )
# 		outfile.write( 'Case #%d: %d\n' % (case + 1, sol) )
#
# outfile.close()


