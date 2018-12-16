import numpy as np

def exploring_search(f, z, delta):
    
    xvar = z[0]
    yvar = z[1]
    if f(xvar+delta, yvar) < f(xvar, yvar):
        xvar += delta
    elif f(xvar-delta, yvar) < f(xvar, yvar):
        xvar -= delta
    if f(xvar, yvar+delta) < f(xvar, yvar):
        yvar += delta
    elif f(xvar, yvar-delta) < f(xvar, yvar):
        yvar -= delta
        
    return np.array([xvar, yvar])

def pattern_search(f, x, x_prev):
    
    x_next = 2*x - x_prev
    if f(x_next[0], x_next[1]) < f(x[0], x[1]):
        return x_next
    else:
        return x
    
def hooke_jeeves(f, x0, y0, delta, eps):
    
    x_current = np.array([x0, y0])
    count = 1
    while True:
        x_next = exploring_search(f, x_current, delta)
        if (x_next == x_current).all():
            if delta < eps:
                break
            else:
                delta = delta/2
        elif (np.linalg.norm(x_next - x_current)/np.linalg.norm(x_next) < eps and
            np.abs((f(x_next[0], x_next[1]) - f(x_current[0], x_current[1]))/f(x_next[0], x_next[1])) < eps):
            break
        else:
            x_current = pattern_search(f, x_next, x_current)
        count += 1
            
    return x_current, count