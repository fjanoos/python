# my implementation of FISTA
__author__ = 'fjanoos'

from  pylab import *
import numpy

def fista(x_o, f, g, grad_f, prox_g, bt_flg=True, L_0=None, eta = 1.1,
		  tol=1e-3, max_its=100, debug=None, verbose =True):
	"""
	Needed:
	x_o : starting point
	f : smooth function f(x)
	g : non-smooth function
	grad_f : gradient of f grad_f(x)
	prox_g : proximal operator prox_g(y, t)= argmin_x  g(x) + t/2 |x-y|^2
	bt_flg : (bool) backtracking or not.
	Optional:
	L_0 : lipschitz constant (if known) else the backtracking constant
	eta: backtracking multiplier
	tol :
	max_its
	debug: A list to store debug shit
	"""
	assert type(x_o) is ndarray
	if L_0 == None:
		if verbose: print( 'no lipschitz provided : will use L = 1 and backtracking')
		bt_flg = True
		L_0 = 1
	x , y = x_o, x_o
	t = 1.0
	if verbose: print( 'starting fista');
	for k in range(max_its):
		if bt_flg:	#determine correct L by backtracking.
			L = L_0 #which L should I start with ?
			bt_cnt = 0;
			while( True ):
				bt_cnt += 1;
				if verbose: print('\t\t backtracking it ', bt_cnt, 'L=', L)
				y_L = prox_grad(y, L, grad_f, prox_g)
				if f(y_L) + g(y_L) <=  Q(y_L, y, f,g, grad_f, L):
					break
				L = eta*L
		else:
			L = L_0
		x_ = prox_grad(y, L, grad_f, prox_g) # x_{k+1}
		chg = norm( x_ - x )/len(x)
		t_kp1 = 0.5*(1. + sqrt(1.+ 4.*t**2) )
		y = x_ + (t - 1.0)/t_kp1*(x_ - x); #Nesterov step
		if verbose: print( '\t it # %d : chg %g'%(k, chg) )
		if debug is not None:
			debug.append( dict(
				k=k, x=x, x_=x_ , y=y, L=L, t=t, t_kp1=t_kp1, chg=chg
			) )
		if chg < tol:
			break
		x, t = x_, t_kp1 #update
	return (x, k, chg)

def Q(x, y, f, g, grad_f, L ):
	""" evaluate the quadratic + non-smooth approximation around y"""
	gf_y = grad_f(y)
	assert shape(gf_y) == shape(y) and shape(x) == shape(y)
	return f(y) + (x-y).T@(gf_y) + 0.5*L*np.linalg.norm(x-y)**2 + g(x)

def prox_grad(y, L, grad_f, prox_g):
	"""
	Beck's pL proximal gradient operator
	p(y, L) = argmin_x{ g(x) + L/2 [x - (y-grad(y)/L) ] }
	"""
	grad_f_y = grad_f(y)
	assert shape(grad_f_y) == shape(y)
	y = y - grad_f_y/L # gradient step
	prox_grad_y =  prox_g(y, L)
	assert type(prox_grad_y) is  ndarray, type(prox_grad_y)
	return prox_grad_y# prox it.
