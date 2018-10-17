import numpy as np

def middle_rectangles_method(f, a, b, n):
    x, h = np.linspace(a, b, n+1, retstep=True)
    y = []
    for i in range(1, n+1):
        y.append(f((x[i-1]+x[i])/2))
    y = np.array(y)
    return np.sum(h*y)
