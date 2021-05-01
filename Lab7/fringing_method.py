import numpy as np

np.seterr(divide = 'raise')

def fringing_method(A, dim):
    if dim == 1:
        try:
            inv = 1/A
        except ArithmeticError:
            return "Не можна знайти обернену матрицю даним методом"
        else:
            return inv
    
    u_n = np.vstack(A.T[-1][:-1])
    v_n = np.array([A[-1][:-1]])
    a_nn = A[-1][-1]
    try:
        A_1 = fringing_method(A[:-1].T[:-1].T, dim-1)
        a_n = a_nn - (v_n @ A_1 @ u_n)
    except ValueError:
        return A_1
    except TypeError:
        return A_1
    else:
        try:
            inverted = np.block([
                [A_1 + (A_1 @ u_n @ v_n @ A_1)/a_n, -(A_1 @ u_n)/a_n],
                [-(v_n @ A_1)/a_n, 1/a_n]
            ])
        except ArithmeticError:
            return "Не можна знайти обернену матрицю даним методом"
        else:
            return inverted
