
import numpy as np


def power_iteration(A, num_simulations):
    # Ideally choose a random vector
    # To decrease the chance that our vector
    # Is orthogonal to the eigenvector
    b_k = np.random.rand(A.shape[1])

    for _ in range(num_simulations):
        # calculate the matrix-by-vector product Ab
        b_k1 = np.dot(A, b_k)

        # calculate the norm
        b_k1_norm = np.linalg.norm(b_k1)

        # re normalize the vector
        b_k = b_k1 / b_k1_norm
    y = np.dot(A, b_k)
    eigenvalue = y[1]/b_k[1]
    return b_k, eigenvalue


x = power_iteration(np.array([[-2, -2, 3], [-10 , -1, 6], [10, -2, -9]]), 10)

print(x)