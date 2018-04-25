# !/usr/bin/python

__author__ = 'fjanoos'

from optparse import OptionParser
from pylab import *
from numpy import linalg

# acceptable error
eps = 1e-4  #finfo(float).eps

def test_model( num_list, verb_flg):
	lhs_matrix =  matrix( [num_list[:-1], [double(1) for x in num_list[:-1]] ] ).transpose();

	rhs_matrix = matrix( num_list[1:]).transpose();

	# do a least squares solve
	coeffs = linalg.solve( lhs_matrix.transpose()*lhs_matrix, lhs_matrix.transpose()*rhs_matrix)

	if coeffs[0] > 1 and verb_flg:
		print( 'warning: This is not a well conditioned recursion (K > 1) -- might fail giving a result.' )

	# compute residuals
	r = rhs_matrix - lhs_matrix*coeffs

	sse = ( r.transpose()*r ) / len(r)

	if  verb_flg:
		print ( coeffs, sse)

	if sse < eps :
		return coeffs
	else:
		return None


if __name__ == "__main__":
	usage = \
		'''  %prog [options] [0,1] num_1 ... num_n
				   Prints K,L for a_i = K a_{i-1} + L ''';
	option_parser = OptionParser( usage )
	option_parser.add_option( "-v", "--verbose", action = "store_true", dest = "verbose", default = False );
	(options, args) = option_parser.parse_args( )

	verb_flg = options.verbose;

	if len( args ) <= 1 or (int(args[0]) !=1 and int(args[0]) !=2 ):
		option_parser.error( "incorrect arguments" )
		option_parser.print_help( )
		sys.exit( )

	type = int(args[0])
	num_list = [];
	for ii in range( 1, len( args ) ):
		num_list.append( double(args[ii]) )

	if  verb_flg:
		print 'processing '+str( num_list)


	try:
		coefs = test_model(num_list, verb_flg)
		if coefs != None:
			if type == 1:
				print '%.2f %.2f'%(coefs[0], coefs[1])
			else:
				print 'true'
		else:
			print 'false'
	except LinAlgError:
		print 'false'



# else:
# 	type = 1
# 	a0 = 4;
# 	K = 0.5;
# 	L = 2.77
# 	num_list = [a0]
# 	a_i = a0;
# 	for i in range( 1, 1000 ):
# 		a_i = a_i * K + L
# 		num_list.append( a_i )