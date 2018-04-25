from numpy import linalg, transpose, random, dot

def rsvd(A, k):
	l = k+1;
	m, n =  A.shape;
	minindex = min(m,n);
	if(k>minindex):
		return linalg.svd(A);

	H = transpose(dot(random.randn(l,m),A));
	Q,R = linalg.qr(H);
	(U, S, V2) = linalg.svd(dot(A,Q));
	V = transpose( dot( Q,transpose(V2) ) );
	U = U[:,:k]; V = V[:k,:]; S = S[:k];
	return (U,S,V);
	pass

