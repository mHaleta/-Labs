import numpy as np
import math

def runge_kutta_3_order(f, u_0, x, h):
    try:
        y = [u_0]
        for i in range(x.shape[0]-1):
            if f(y[i], x[i]) == math.inf or f(y[i], x[i]) == -math.inf:
                raise ArithmeticError
                break
                
            k1 = h*f(y[i], x[i])
            k2 = h*f(y[i]+k1/2, x[i]+h/2)
            k3 = h*f(y[i]+2*k2-k1, x[i]+h)
        
            y.append(y[i]+(k1+4*k2+k3)/6)
    
        u = np.array(y)
    except ArithmeticError:
        return None
    except ValueError:
        return None
    else:
        return u