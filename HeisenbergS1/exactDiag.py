import netket as nk

def Lanczos(ha):
    exact_result = nk.exact.lanczos_ed(ha, first_n=1, compute_eigenvectors=False)
    exact_gs_energy = exact_result.eigenvalues[0]
    return exact_gs_energy