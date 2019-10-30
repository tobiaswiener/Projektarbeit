import netket as nk
import numpy as np
import time


def generateNN(length, coupling):
    print("hallo")
    J = [coupling,0]
    edge_colors = []
    for i in range(length):
        edge_colors.append([i, (i + 1) % length, 1])
        edge_colors.append([i, (i + 2) % length, 2])

    # Define the netket graph object
    g = nk.graph.CustomGraph(edge_colors)
    hi = nk.hilbert.Spin(graph=g, s=1)

    # matrices
    sigmax = np.sqrt(2) * np.array([[0, 1., 0], [1., 0, 1.], [0, 1., 0]])
    sigmay = np.sqrt(2) * np.array([[0, -1j, 0], [1j, 0, -1j], [0, 1j, 0]])
    sigmaz = np.array([[2, 0, 0], [0, 0, 0], [0, 0, -2]])

    interaction = np.kron(sigmax, sigmax) + np.kron(sigmay, sigmay) + np.kron(sigmaz, sigmaz)
    bond_operator = [(J[0] * interaction).tolist(),
                     (J[1] * interaction).tolist()]
    bond_color = [1, 2]

    # define operator
    op = nk.operator.GraphOperator(hi, bondops=bond_operator, bondops_colors=bond_color)

    return g, hi, op

