"""
Various types of histograms. Might also want to do non-parameteric tests (independence)
"""

__author__ = 'fj'



from pylab import *
from numpy import random
import scipy.ndimage.filters as snf


def joint_hist( x, y, nbins = (20,20), w = None, **kwargs):
	"""
	Compute a joint weighted histogram as an image between x and y.
	:param x:
	:param y:
	:param nbins: number of bins
	:param w: weights

	## Keyword arguments
	:param lims: limits of the histogram as tuple ( min_x, max_x, min_y, max_y )
	:param sigma:  if smoothing / interpolation is required, the bandwidth
	:param hist: hist structure from a previous call containing.
				Required when building a histogram in a windowed fashion.
				Note for this - limits and nbins should be provided.

	:returns:  histograms along x, y, z, along with smooth versions and the figure
	"""


	if "hist" in kwargs.keys():
		# populate from the given histogram
		hist = kwargs["hist"];
		nbins =  hist["nbins"]
		dx, dy = hist["deltas"]
		lims = hist["lims"]
		jhist = hist["jhist"];
		xhist = hist["xhist"];
		yhist = hist["yhist"]
		fig = hist["fig"];
		axs = hist["axs"]

	else: # histogram not provided
		assert shape(nbins)[0] == 2
		jhist = zeros( nbins )
		xhist = zeros( nbins[0] )
		yhist = zeros( nbins[1] )

		if "lims" in kwargs.keys() and len(kwargs["lims"]) == 4:
			lims = kwargs["lims"]
		else:
			lims = ( min(x), max(x), min(y), max(y))

		dx = (lims[1]-lims[0])/(nbins[0]-1); assert dx > 0
		dy = (lims[3]-lims[2])/(nbins[1]-1); assert dx > 0

		fig, axs = subplots(2,2)

	# clip data to limits
	x[ x < lims[0]] = lims[1]; x[ x > lims[1]] = lims[1];
	y[ y < lims[2]] = lims[3]; y[ y > lims[3]] = lims[3];

	# build the histogram
	w = ones(shape(x)) if w is None else w
	xi  =  list(map( int, floor( (x-lims[0]) / dx) ))
	yi  =  list(map( int, floor( (y-lims[2]) / dy) )) # list needed for python3

	for _x, _y , _w in zip(xi, yi, w):
		jhist[_x,_y] += _w
		xhist[_x] += _w
		yhist[_y] += _w

	if "sigma" in kwargs.keys():
		jhist_s = snf.gaussian_filter(jhist, kwargs["sigma"] )
		xhist_s = snf.gaussian_filter(xhist, kwargs["sigma"] )
		yhist_s = snf.gaussian_filter(yhist, kwargs["sigma"])
	else:
		jhist_s = jhist;		xhist_s = xhist;		yhist_s = yhist;

	# build the figure
	xa,ya = meshgrid( linspace(lims[0],lims[1], nbins[0]),  linspace(lims[2],lims[3], nbins[1]) )

	axs[0][0].axis('off')
	axs[0][1].plot(xa[0], xhist_s);
	axs[0][1].set_xlim( (lims[0],lims[1])); axs[0][1].set_title("x histogram")
	axs[1][0].plot( yhist_s, ya.T[0]);
	axs[1][0].set_ylim( (lims[2],lims[3])); axs[1][0].set_title("y histogram")
	axs[1][1].pcolor(xa,ya, jhist_s);
	axs[1][1].set_xlim( (lims[0],lims[1])); axs[1][1].set_ylim( (lims[2],lims[3]))
	axs[1][1].set_title("joint histogram")
	fig.tight_layout()

	return {"xhist":xhist, "yhist":yhist, "jhist":jhist,
	        "xhist_s":xhist, "yhist_s":yhist, "jhist_s":jhist_s,
	        "fig":fig, "lims":lims, "nbins":nbins, "xa":xa[0], "ya":ya.T[0],
			"deltas":(dx,dy), "axs":axs }



if __name__ == "__main__":
.
	x = np.random.normal( 1, 10, 100 )
	y = x*0.5 + np.random.normal( 0, 10, 100 )
	hist  = joint_hist( x, y, nbins=(50,50) , sigma = 3, hist=hist);

	show()


	H, xa , ya = np.histogram2d(y, x, bins=[50, 50])

	imshow(H, interpolation='nearest', origin='low', extent=[xa[0], xa[-1], ya[0], ya[-1]])
