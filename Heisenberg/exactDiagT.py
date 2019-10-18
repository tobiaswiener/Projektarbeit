import netket as nk
import time
import matplotlib.pyplot as plt

def deltat(L):
    g = nk.graph.Hypercube(length=L, n_dim=1, pbc=True)

    # Define the Hilbert space based on this graph
    # We impose to have a fixed total magnetization of zero
    hi = nk.hilbert.Spin(s=0.5, graph=g, total_sz=0)

    # calling the Heisenberg Hamiltonian
    ha = nk.operator.Heisenberg(hilbert=hi)

    #determine DeltaT
    start = time.time()
    nk.exact.lanczos_ed(ha, first_n=1, compute_eigenvectors=False)
    ende = time.time()
    return ende - start

def deltatlist(min, max):
    lengthlist = []
    list = []
    for l in range(min, max, 2):
        lengthlist.append(l)
        list.append(deltat(l))

    plt.plot(lengthlist,list , 'ro')
    plt.yscale('log')
    plt.show()

    return lengthlist, list

print(deltatlist(4,28))











