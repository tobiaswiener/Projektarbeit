import netket as nk

def Lanczos(ha):
    exact_result = nk.exact.lanczos_ed(ha, first_n=1, compute_eigenvectors=False)
    exact_gs_energy = exact_result.eigenvalues[0]
    with open("exactSol.txt", "w") as reader:
        reader.write(str(exact_gs_energy))
    return exact_gs_energy
