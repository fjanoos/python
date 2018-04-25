from pymc import MCMC, Bernoulli, Potential; 
from pylab import Inf; 
from networkx import cycle_graph

class IndepSetMC(MCMC):
	def __init__(self, G=cycle_graph(9), beta=0.0):
		self.G, self.beta = G, beta
		self.x   = [ Bernoulli(str(v), 0.5, value=0) for v in G.nodes_iter() ]
		self.psi = [ self.IndepSetPotential(v, G[v]) for v in G.nodes_iter() ]
		MCMC.__init__(self, [self.x,self.psi])

	def IndepSetPotential(self, v, N_v):
		def potential_logp(v, N_v):
			if v + max(N_v) > 1:
				return -Inf
			else:
				return self.beta*v
		return Potential(logp = potential_logp, name = "N_%d" % v, parents = {'v': self.x[v], 'N_v': [self.x[w] for w in N_v]}, doc = 'vertex potential term')

M = IndepSetMC()
M.sample(1000) 
