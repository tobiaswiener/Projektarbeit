# Import netket library
import netket as nk
# Import Json, this will be needed to examine log files
import json
# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
import time

# Define a 1d chain
L = 20
g = nk.graph.Hypercube(length=L, n_dim=1, pbc=True)

# Define the Hilbert space based on this graph
# We impose to have a fixed total magnetization of zero
hi = nk.hilbert.Spin(s=0.5, graph=g, total_sz=0)

# calling the Heisenberg Hamiltonian
ha = nk.operator.Heisenberg(hilbert=hi)

############## exact Diagonalize


# compute the ground-state energy (here we only need the lowest energy, and do not need the eigenstate)
startl = time.time()
exact_result = nk.exact.lanczos_ed(ha, first_n=1, compute_eigenvectors=False)
endel = time.time()
exact_gs_energy = exact_result.eigenvalues[0]
print("lanczos took",endel - startl, "seconds" )
print('The exact ground-state energy is E0=',exact_gs_energy)

################ Jastrow Ansatz

ma = nk.machine.Jastrow(hilbert=hi)
ma.init_random_parameters(seed=1234, sigma=0.01)
# optimizer
op = nk.optimizer.Sgd(learning_rate=0.1)
# sampler
sa = nk.sampler.MetropolisExchange(graph=g, machine=ma)
# stochastic reconfiguration
gs = nk.variational.Vmc(hamiltonian=ha, sampler=sa, optimizer=op, n_samples=1000, diag_shift=0.1, method="Sr")
# run
start = time.time()
gs.run(output_prefix="Jastrow",n_iter=300,)
end = time.time()
#print statements
print('### Jastrow calculation')
print('Has',ma.n_par,'parameters')
print('The Jastrow calculation took',end-start,'seconds')