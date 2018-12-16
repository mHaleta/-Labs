import numpy as np

class Simplex:
    def __init__(self, X):
        self.unable_g_row = False
        self.isAdmissible = all((np.round(X.T[0][:-1], 5)) >= 0)
        self.isOptimal = all((np.round(X[-1][1:], 5)) <= 0)
        self.X = X
        self.free = {}
        self.basis = {}
        for i in range(self.X.shape[1]-1):
            self.free['x'+str(i+1)] = 0.
        for i in range(self.X.shape[1], self.X.shape[1]+self.X.shape[0]-1):
            self.basis['x'+str(i)] = self.X[i-self.X.shape[1]][0]
        
    def result(self):
        if self.isAdmissible and self.isOptimal:
            return (round(self.X[-1][0], 5),
                    [round(dict(self.free.items() | \
                                self.basis.items())['x'+str(i)], 5) \
                                for i in range(1, self.X.shape[1])])
        if self.isAdmissible and self.unable_g_row:
            return "Необмежений мінімум", None
        if not self.isAdmissible and self.unable_g_row:
            return "Система обмежень несумісна", None
        
    def use_appropriate_simplex_method(self):
        if self.isAdmissible:
            self.simplex_method_for_admissible_solution()
            return self.result()
        else:
            self.simplex_method_for_inadmissible_solution()
            return self.result()
    
    def swap(self, g_row, g_col):
        free_keys = []
        for i, j in zip(self.free.keys(), range(1, self.X.shape[1])):
            if j != g_col:
                free_keys.append(i)
            else:
                toDelete_free = i
        self.free.pop(toDelete_free)

        basis_keys = []
        for i, j in zip(self.basis.keys(), range(self.X.shape[0]-1)):
            if j != g_row:
                basis_keys.append(i)
            else:
                toDelete_basis = i
        self.basis.pop(toDelete_basis)

        free_keys = np.insert(free_keys, g_col-1, toDelete_basis)
        basis_keys = np.insert(basis_keys, g_row, toDelete_free)
    
        self.free.clear()
        self.basis.clear()
                
        for i in free_keys:
            self.free[i] = 0.
        for i, j in zip(basis_keys, range(self.X.shape[0]-1)):
            self.basis[i] = self.X[j][0]
        
    def simplex_method_for_admissible_solution(self):
        self.isOptimal = all((np.round(self.X[-1][1:], 5)) <= 0)
        while self.isOptimal == False:
            g_col = np.argmax(self.X[-1][1:]) + 1
            self.unable_g_row = all((np.round(self.X.T[g_col][:-1], 5)) <= 0)
            if self.unable_g_row:
                break
            g_row = np.argmin(np.array(
                [self.X[i][0]/self.X[i][g_col] \
                 if self.X[i][g_col] > 0 else np.inf \
                 for i in range(self.X.shape[0]-1)]
            ))
        
            X1 = np.zeros((self.X.shape[0], self.X.shape[1]))
        
            X1[g_row][g_col] = 1 / self.X[g_row][g_col]
            for j in range(self.X.shape[1]):
                if j == g_col:
                    continue
                X1[g_row][j] = self.X[g_row][j] / self.X[g_row][g_col]
            for i in range(self.X.shape[0]):
                if i == g_row:
                    continue
                X1[i][g_col] = (-1) * self.X[i][g_col] / self.X[g_row][g_col]
            
            for i in range(self.X.shape[0]):
                if i == g_row:
                    continue
                for j in range(self.X.shape[1]):
                    if j == g_col:
                        continue
                    X1[i][j] = self.X[i][j] + X1[i][g_col] * self.X[g_row][j]

            self.X = X1
            self.swap(g_row, g_col)
            self.isOptimal = all((np.round(self.X[-1][1:], 5)) <= 0)
    
    def simplex_method_for_inadmissible_solution(self):
        while self.isAdmissible == False:
            g_row = None
            for i in range(self.X.shape[0]-1):
                if self.X[i][0] < 0:
                    for j in range(1, self.X.shape[1]):
                        if self.X[i][j] < 0:
                            g_row = i
                            g_col = j
                            break
                    break
                    
            if g_row is None:
                self.unable_g_row = True
                break
            else: 
                X1 = np.zeros((self.X.shape[0], self.X.shape[1]))
        
                X1[g_row][g_col] = 1 / self.X[g_row][g_col]
                for j in range(self.X.shape[1]):
                    if j == g_col:
                        continue
                    X1[g_row][j] = self.X[g_row][j] / self.X[g_row][g_col]
                for i in range(self.X.shape[0]):
                    if i == g_row:
                        continue
                    X1[i][g_col] = (-1)*self.X[i][g_col]/self.X[g_row][g_col]
            
                for i in range(self.X.shape[0]):
                    if i == g_row:
                        continue
                    for j in range(self.X.shape[1]):
                        if j == g_col:
                            continue
                        X1[i][j] = self.X[i][j]+X1[i][g_col]*self.X[g_row][j]
                    
                self.X = X1
                self.swap(g_row, g_col)
                self.isAdmissible = all((np.round(self.X.T[0][:-1], 5)) >= 0)
            
        if not self.unable_g_row:
            self.simplex_method_for_admissible_solution()
            
def simplex_method_fictitious_basis(X, ficts, initial_shape):
    
    free = {}
    basis = {}
    for i in range(X.shape[1]-1):
        free['x'+str(i+1)] = 0.
    for i in range(X.shape[1], X.shape[1]+X.shape[0]-2):
        basis['x'+str(i)] = X[i-X.shape[1]][0]
        
    unable_g_col = False
    unable_g_row = False
    
    while round(X[-1][0], 5) != 0:
        
        if all(np.round(X[-1][1:], 5) <= 0):
            unable_g_col = True
            break
        
        X1 = np.zeros((X.shape[0], X.shape[1]))
        
        g_col = np.argmax(X[-1][1:])+1
        g_row = np.argmin(np.array([X[i][0]/X[i][g_col] \
                                    if X[i][g_col] > 0 else np.inf \
                                    for i in range(X.shape[0]-2)]))
        
        for j in range(X.shape[1]):
            if j == g_col:
                continue
            X1[g_row][j] = X[g_row][j] / X[g_row][g_col]

        for i in range(X.shape[0]):
            if i == g_row:
                continue
            X1[i][g_col] = (-1) * X[i][g_col] / X[g_row][g_col]
            
        for i in range(X.shape[0]):
            if i == g_row:
                continue
            for j in range(X.shape[1]):
                if j == g_col:
                    continue
                X1[i][j] = X[i][j] + X1[i][g_col] * X[g_row][j]
                
        X = X1
        
        free_keys = []
        for i, j in zip(free.keys(), range(1, X.shape[1])):
            if j != g_col:
                free_keys.append(i)
            else:
                toDelete_free = i
        free.pop(toDelete_free)

        basis_keys = []
        for i, j in zip(basis.keys(), range(X.shape[0]-2)):
            if j != g_row:
                basis_keys.append(i)
            else:
                toDelete_basis = i
        basis.pop(toDelete_basis)
        
        if g_row not in ficts:
            free_keys = np.insert(free_keys, g_col-1, toDelete_basis)
        basis_keys = np.insert(basis_keys, g_row, toDelete_free)
    
        free.clear()
        basis.clear()
                
        for i in free_keys:
            free[i] = 0.
        for i, j in zip(basis_keys, range(X.shape[0]-1)):
            basis[i] = X[j][0]
                
        if g_row in ficts:
            X = np.delete(X, g_col, 1)
            ficts = np.delete(ficts, np.where(ficts == g_row)[0], 0)
            
    if unable_g_col:
        return "Система обмежень несумісна", None
        
    X = np.delete(X, -1, 0)
    
    isOptimal = all((np.round(X[-1][1:], 5)) <= 0)
    while isOptimal == False:
        g_col = np.argmax(X[-1][1:]) + 1
        unable_g_row = all((np.round(X.T[g_col][:-1], 5)) <= 0)
        if unable_g_row:
            break
        g_row = np.argmin(np.array(
            [X[i][0]/X[i][g_col] \
             if X[i][g_col] > 0 else np.inf \
             for i in range(X.shape[0]-1)]
        ))
        
        X1 = np.zeros((X.shape[0], X.shape[1]))
        
        X1[g_row][g_col] = 1 / X[g_row][g_col]
        for j in range(X.shape[1]):
            if j == g_col:
                continue
            X1[g_row][j] = X[g_row][j] / X[g_row][g_col]
        for i in range(X.shape[0]):
            if i == g_row:
                continue
            X1[i][g_col] = (-1) * X[i][g_col] / X[g_row][g_col]
            
        for i in range(X.shape[0]):
            if i == g_row:
                continue
            for j in range(X.shape[1]):
                if j == g_col:
                    continue
                X1[i][j] = X[i][j] + X1[i][g_col] * X[g_row][j]

        X = X1
        
        free_keys = []
        for i, j in zip(free.keys(), range(1, X.shape[1])):
            if j != g_col:
                free_keys.append(i)
            else:
                toDelete_free = i
        free.pop(toDelete_free)

        basis_keys = []
        for i, j in zip(basis.keys(), range(X.shape[0]-1)):
            if j != g_row:
                basis_keys.append(i)
            else:
                toDelete_basis = i
        basis.pop(toDelete_basis)
        
        free_keys = np.insert(free_keys, g_col-1, toDelete_basis)
        basis_keys = np.insert(basis_keys, g_row, toDelete_free)
    
        free.clear()
        basis.clear()
                
        for i in free_keys:
            free[i] = 0.
        for i, j in zip(basis_keys, range(X.shape[0]-1)):
            basis[i] = X[j][0]
        
        isOptimal = all((np.round(X[-1][1:], 5)) <= 0)
        
    if unable_g_row:
        return "Необмежений мінімум", None
    
    d = dict(free.items() | basis.items())
        
    return round(X[-1][0], 5), [round(d['x'+str(i)], 5) \
                                for i in range(1, initial_shape)]