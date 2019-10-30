import netket as nk
import numpy as np


# J1-J2 Model Parameters
J = [8,0]
L = 8

g = nk.graph.Hypercube(length=L, n_dim=1, pbc=True)

# Define custom graph
edge_colors = []
for i in range(L):
    edge_colors.append([i, (i+1)%L, 1])
    edge_colors.append([i, (i+2)%L, 2])

# Define the netket graph object
g1 = nk.graph.CustomGraph(edge_colors)

hi1 = nk.hilbert.CustomHilbert(graph=g1, local_states=[-1,0,1])


hi = nk.hilbert.CustomHilbert(graph=g,local_states=[-1,0,1])


#matrices
sigmax = np.sqrt(2)*np.array([[0,1.,0],[1.,0,1.],[0,1.,0]])
sigmay =  np.sqrt(2)*np.array([[0,-1j,0],[1j,0,-1j],[0,1j,0]])
sigmaz = np.array([[2,0,0],[0,0,0],[0,0,-2]])

interaction = np.kron(sigmax,sigmax) + np.kron(sigmay,sigmay) + np.kron(sigmaz, sigmaz)
bond_operator = [(J[0]*interaction).tolist(),
                 (J[1]*interaction).tolist()]
bond_color = [1,2]


#define operator
op = nk.operator.GraphOperator(hi1, bondops=bond_operator, bondops_colors=bond_color)

#exact results
res = nk.exact.lanczos_ed(op, first_n=1, compute_eigenvectors=False)
print((res.eigenvalues[0]))

