"""
Test my fista implementation on LASSO
"""
from pylab import *
from sklearn import linear_model
from sklearn.linear_model import Lasso
import numpy as np
from sklearn.metrics import r2_score
import fista

###############################################################################
# generate some sparse data to play with
np.random.seed(42)

n_samples, n_features = 50, 200
X = np.random.randn(n_samples, n_features)
coef = 3 * np.random.randn(n_features)
inds = np.arange(n_features)
np.random.shuffle(inds)
coef[inds[10:]] = 0  # sparsify coef
y = np.dot(X, coef)
# add noise
y += 0.01 * np.random.normal((n_samples,))

# Split data in train set and test set
n_samples = X.shape[0]
X_train, y_train = X[:n_samples / 2], y[:n_samples / 2]
X_test, y_test = X[n_samples / 2:], y[n_samples / 2:]

###############################################################################
# The optimization objective for Lasso is:
# (1 / (2 * n_samples)) * ||y - Xw||^2_2 + alpha * ||w||_1
alpha = 0.1

lasso = Lasso(alpha=alpha)
y_pred_lasso = lasso.fit(X_train, y_train).predict(X_test)
r2_score_lasso = r2_score(y_test, y_pred_lasso)
print(lasso)
print("r^2 on test data : %f" % r2_score_lasso)


# solve using FISTA

u,s,v = svd(X)
L = 2*s[0]**2 # the lipschitz constant for the problem

def f( x ):
	global X, y
	(n,p) = shape(X)
	assert type(x) is ndarray and shape(x)[0] == p
	return 0.5*linalg.norm(y - dot(X,x))**2/n

def g(x):
	global X, alpha
	(n,p) = shape(X)
	assert type(x) is ndarray and shape(x)[0] == p
	return alpha*reduce(lambda x,y : x+abs(y), x, 0 )

def grad_f(x):
	global X
	(n,p) = shape(X)
	return  -dot(y - dot(X,x), X)/n

def prox_g(x, t):
	"""
	argmin_y  alpha|x|_1 + t/2 |x-y|^2_2
	"""
	global alpha
	m = alpha/t
	return  array( [sign(xi)*( abs(xi) - m ) if abs(xi) > m else 0   for xi in x ] )

sol = fista.fista( zeros(shape(coef)), f, g, grad_f, prox_g, bt_flg=True, L_0=400, eta=1.2 , max_its = 1000 )
plot(lasso.coef_, label='Lasso coefficients')
plot(coef, '--', label='original coefficients')
plot(sol[0], '.-', label='fista coefficients')
legend(loc='best')
title("Lasso R^2: %f"
          % (r2_score_lasso, ))
show()

print( sol )