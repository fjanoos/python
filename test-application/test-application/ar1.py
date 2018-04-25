# specify an AR(1) type process
import pymc
from pymc import MCMC, Bernoulli, Potential, Normal; 
from pylab import Inf; 
import networkx.generators.classic as ngc;
from numpy import array, matrix, zeros;

N = 5;
Sigma_Y = 1

class MarkovLattice(MCMC):

    def __init__(self, lattice=ngc.grid_graph( dim=[N,N] ), 
                 data=zeros((N,N)), tau_x = 1, tau_y = 1, phi = 0.1):
        
        # sanity test
        if lattice.number_of_nodes() != data.size:
            raise Exception('data and lattice sizes do not match', 
                            '%d vs %d' % (data.size, lattice.number_of_nodes()) );

        self.num_nodes = lattice.number_of_nodes();
        self.phi = phi;
        self.tau_x = 1;
        self.tau_y = 1;

        #just in case the input decides to give us weights
        for e in lattice.edges_iter():
            if not lattice.get_edge_data(e[0],e[1]) :
                 #setting lattice
                 lattice.edge[e[0]][e[1]] = {'weight':phi};
                 lattice.edge[e[1]][e[0]] = {'weight':phi};
            else:
                #keep the data
                pass;
        self.lattice , self.data = lattice, data;
                
        # convert the lattice into a GMRF precision matrix
        self.Lambda = zeros(self.num_nodes,self.num_nodes);
       
        #set up the grid and the data
        #@stochastic(dtype=float)
        #@def X

        # this v is a tuple index of the grid
        self.Y  = [ Normal('Y_'+str(v), mu=0.5, tau=Sigma_Y**-1, 
                                value=data[v], observed = True ) 
                                for v in lattice.nodes_iter() ];
        MCMC.__init__(self, [self.Y])  

    def prior_logp