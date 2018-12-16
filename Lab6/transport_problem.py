import numpy as np

class TransportProblem:
    def __init__(self, C, supply, demand, n, m, isMax=False):
        self.C = C
        self.supply = supply
        self.demand = demand
        self.n = n
        self.m = m
        self.isMax = isMax
        self.cycle = None
        
    def __call__(self):
        opened_1 = False
        opened_2 = False
        
        if not self.isClosed(self.supply, self.demand):
            delta = np.sum(self.supply) - np.sum(self.demand)
            if delta > 0:
                opened_1 = True
                self.demand = np.append(self.demand, delta)
                self.C = np.append(self.C, np.zeros((self.n, 1)), axis=1)
                self.m += 1
            else:
                opened_2 = True
                self.supply = np.append(self.supply, -delta)
                self.C = np.append(self.C, np.zeros((1, self.m)), axis=0)
                self.n += 1
            
        X = self.north_west_conner_method(self.n, self.m,
                                          self.supply, self.demand)
        
        X_initial = np.copy(X)
        res_initial = np.sum(X*self.C)
        
        for i in range(self.n):
            for j in range(self.m):
                if X[i][j] == 0:
                    X[i][j] = np.nan
        
        while True:
            
            if self.isDegenerate(X, self.n, self.m):
                X = self.make_nondegenerate(X, self.n, self.m)
                
            alpha, beta = self.potentials_calculation(self.C, X)
            est = self.cells_estimation(self.C, self.n, self.m, alpha, beta)
            
            if self.isOptimal(est, self.isMax):
                for i in range(self.n):
                    for j in range(self.m):
                        if np.isnan(X[i][j]):
                            X[i][j] = 0
                break
                
            row, col = self.max_estimation_coords(est, self.isMax)
            self.find_cycle(X, self.n, self.m, row, col)
            X = self.recalculation(X, self.cycle, self.n, self.m)
                    
        if opened_1:
            return ((X_initial.T[:-1]).T, res_initial,
                    (X.T[:-1]).T, np.sum(X*self.C))
        if opened_2:
            return X_initial[:-1], res_initial, X[:-1], np.sum(X*self.C)
        
        return X_initial, res_initial, X, np.sum(X*self.C)
        
    def isClosed(self, supply, demand):
        if np.sum(supply) == np.sum(demand):
            return True
        else:
            return False
        
    def north_west_conner_method(self, n, m, supply, demand):
        X = np.zeros((n, m))
        for i in range(n):
            for j in range(m):
                X[i][j] = min(supply[i] - np.sum(X, axis=1)[i],
                              demand[j] - np.sum(X, axis=0)[j])
                
        return X
    
    def isDegenerate(self, X, n, m):
        if np.count_nonzero(np.isfinite(X)) != n+m-1:
            return True
        else:
            return False
        
    def make_nondegenerate(self, X, n, m):
        delta = n + m - 1 - np.count_nonzero(np.isfinite(X))
        while delta > 0:
            b = False
            for i in range(n):
                for j in range(m):
                    if np.isnan(X[i][j]):
                        if not self.find_cycle(X, n, m, i, j):
                            X[i][j] = 0
                            b = True
                            break
                if b:
                    break
            delta -= 1
        
        return X
        
    def potentials_calculation(self, C, X):
        alpha = [None] * C.shape[0]
        beta = [None] * C.shape[1]
        
        alpha[0] = 0.
        for j in range(C.shape[1]):
            if np.isfinite(X[0][j]):
                beta[j] = C[0][j] - alpha[0]
                
        while (any(u is None for u in alpha[1:]) or
               any(v is None for v in beta)):
            for i in range(1, C.shape[0]):
                for j in range(C.shape[1]):
                    if (np.isfinite(X[i][j]) and beta[j] is None
                        and alpha[i] is None):
                        continue
                    elif np.isfinite(X[i][j]) and beta[j] is None:
                        beta[j] = C[i][j] - alpha[i]
                    elif np.isfinite(X[i][j]) and alpha[i] is None:
                        alpha[i] = C[i][j] - beta[j]
                
        return np.array(alpha), np.array(beta)
    
    def cells_estimation(self, C, n, m, alpha, beta):
        est = np.zeros((n, m))
        for i in range(n):
            for j in range(m):
                est[i][j] = alpha[i] + beta[j] - C[i][j]
                
        return est
    
    def isOptimal(self, est, isMax):
        if isMax:
            if (est >= 0).all():
                return True
            else:
                return False
        else:
            if (est <= 0).all():
                return True
            else:
                return False
    
    def max_estimation_coords(self, est, isMax):
        if isMax:
            row, col = np.unravel_index(np.argmin(est), est.shape)
        else:
            row, col = np.unravel_index(np.argmax(est), est.shape)
        return row, col
    
    def find_cycle(self, X, n, m, row, col):
        self.cycle = [[row, col]]
        if not self.look_horizontally(X, self.cycle, n, m, row, col, row, col):
            return False
        else:
            return True
        
    def look_horizontally(self, X, cycle, n, m, row, col, row_next, col_next):
        for j in range(m):
            if j != col and np.isfinite(X[row][j]):
                if j == col_next:
                    cycle.append([row, j])
                    return True
                if self.look_vertically(X, cycle, n, m, row, j,
                                        row_next, col_next):
                    cycle.append([row, j])
                    return True
        return False
    
    def look_vertically(self, X, cycle, n, m, row, col, row_next, col_next):
        for i in range(n):
            if i != row and np.isfinite(X[i][col]):
                if i == row_next:
                    cycle.append([i, col])
                    return True
                if self.look_horizontally(X, cycle, n, m, i, col,
                                          row_next, col_next):
                    cycle.append([i, col])
                    return True
        return False
    
    def recalculation(self, X, cycle, n, m):
        min_elem = np.min([X[i][j] for i, j in cycle[1::2]])
        
        k = cycle[0][0]
        l = cycle[0][1]
        
        X[k][l] = min_elem
        cycle_len = len(cycle)

        for i in range(1, cycle_len):
            k = cycle[i][0]
            l = cycle[i][1]
            if i%2 == 0:
                X[k][l] += min_elem
            else:
                X[k][l] -= min_elem
                if X[k][l] == 0.:
                    X[k][l] = np.nan
                
        return X