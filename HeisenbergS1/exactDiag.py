import netket as nk

def Lanczos(graph, ha):
    L = graph.n_sites
    exact_result = nk.exact.lanczos_ed(ha, first_n=1, compute_eigenvectors=False)
    exact_gs_energy = exact_result.eigenvalues[0]
    filename = str(0) + str(L) + "_" + "exact" + ".txt"
    with open(filename, "w") as reader:
        reader.write(str(exact_gs_energy))
    return exact_gs_energy
