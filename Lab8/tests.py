import numpy as np

A = np.array([
        [3, 2, 1],
        [1, 3, 2],
        [2, 2, 3],
        [4, 2, 1]
])

B = np.array([6, 7, 8, 6])

eigen_values, V = np.linalg.eig(A.T @ A)
S = np.sqrt(eigen_values)*np.eye((A.T @ A).shape[0])
U = A @ V @ np.linalg.inv(S)

current_X = V @ np.linalg.inv(S) @ U.T @ B

expected_X = np.linalg.lstsq(A, B, rcond=None)[0]

assert(np.linalg.norm(current_X - expected_X) < 0.1)

print("Test passed")
