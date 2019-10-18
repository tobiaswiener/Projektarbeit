# Import netket library
import netket as nk
# Import Json, this will be needed to examine log files
import json
# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
import time




# Define a 1d chain
L = 4
g = nk.graph.Hypercube(length=L, n_dim=1, pbc=True)


# Define the Hilbert space based on this graph
# We impose to have a fixed total magnetization of zero
hi = nk.hilbert.Spin(s=0.5, graph=g, total_sz=0)

# calling the Heisenberg Hamiltonian
ha = nk.operator.Heisenberg(hilbert=hi)


# compute the ground-state energy (here we only need the lowest energy, and do not need the eigenstate)
exact_result = nk.exact.lanczos_ed(ha, first_n=1, compute_eigenvectors=False)
exact_gs_energy = exact_result.eigenvalues[0]
print('The exact ground-state energy is E0=',exact_gs_energy)