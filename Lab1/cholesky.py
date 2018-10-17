import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon, QFont
from PyQt5 import QtCore, QtGui
import numpy as np


class MainWindow(QWidget):
    
    def __init__(self, parent=None):
        
        super().__init__(parent)
        self.dim = "2"
        self.secondWin = None
        self.initUI()

    def initUI(self):
        
        self.lbl = QLabel(self)
        self.lbl.move(10, 12)
        self.lbl.setFont(QFont("Arial", 11))
        self.lbl.setText("Виберіть розмірність матриці коефіцієнтів: ")
        
        self.combo = QComboBox(self)
        for i in range(5):
            self.combo.addItem(str(i+2), i)
        self.combo.move(320, 10)
        self.combo.activated.connect(self.setDim)
        
        self.okbutton = QPushButton("OK", self)
        self.okbutton.move(160, 60)
        self.okbutton.clicked.connect(self.openWin)

        self.setGeometry(150, 150, 400, 100)
        self.setWindowTitle('Метод Холецького')
        self.setWindowIcon(QIcon('icon.jpg'))

        self.show()
            
    def setDim(self, index):
        self.dim = self.combo.itemText(index)
        
    def openWin(self):
        if self.secondWin is not None:
            self.secondWin = None
            self.secondWin = SecondWindow(self.dim)
            self.secondWin.show()
        else:
            self.secondWin = SecondWindow(self.dim)
            self.secondWin.show()
    
class SecondWindow(QMainWindow):
    
    def __init__(self, dim, parent=None):
        
        super().__init__(parent, QtCore.Qt.Window)
        self.matrix_entry = []
        self.x_str = []
        self.dim = int(dim)
        self.initUI()
        
    def initUI(self):
        
        reg = QtCore.QRegExp("^[-]?[0-9]*\.?[0-9]+")
        validator = QtGui.QRegExpValidator(reg)
        
        for i in range(self.dim+1):
            self.matrix_entry.append([])
            self.x_str.append([])
            
            for j in range(self.dim):
                self.matrix_entry[i].append(QLineEdit(self))
                self.matrix_entry[i][j].resize(30, 20)
                
                if i == self.dim:
                    self.matrix_entry[i][j].move(120+70*(i-1), 12+30*j)
                else:
                    self.matrix_entry[i][j].move(10+70*i, 12+30*j)
                    self.x_str[i].append(QLabel("x"+str(i+1), self))
                    self.x_str[i][j].move(45+70*i, 10+30*j)
                    
                    equal_label = QLabel("=", self)
                    equal_label.move(85+70*(self.dim-1), 8+30*i)
                
                self.matrix_entry[i][j].setValidator(validator)
        
        
        but = QPushButton("Розв\'язати систему", self)
        but.resize(130, 30)
        but.move(225, 40+30*self.dim)
        but.clicked.connect(self.solve)
        
        self.setGeometry(150, 150, 600, 400)
        self.setWindowTitle('Метод Холецького')
        self.setWindowIcon(QIcon('icon.jpg'))
    
    def solve(self):
        
        b = False
        for i in range(self.dim+1):
            for j in range(self.dim):
                if self.matrix_entry[i][j].text() != "":
                    b = True
                    continue
                else:
                    QMessageBox.warning(self, "Message",
                                    "Всі поля мають бути заповнені")
                    b = False
                    break
            if b == False:
                break
        
        if b == True:
        
            A = np.zeros((self.dim, self.dim))
            b = np.zeros(self.dim)
        
            for i in range(self.dim+1):
                for j in range(self.dim):
                    if i == self.dim:
                        b[j] = float(self.matrix_entry[i][j].text())
                    else:
                        A[i][j] = float(self.matrix_entry[j][i].text())
        
            if self.isSymmetric(A) == False:
                QMessageBox.warning(self, "Message",
                                    "Матриця коефіцієнтів не симетрична")
            elif self.isPositive(A) == False:
                QMessageBox.warning(self, "Message",
                        "Матриця коефіцієнтів не задовольняє умовам методу")
            else:
                x, L = self.cholesky(A, b)
                QMessageBox.information(self, "Message", "X = "+str(x))
                
    def isSymmetric(self, A):
        
        if np.array_equal(A, A.T):
            return True
        else:
            return False
        
    def isPositive(self, A):
        
        L = np.zeros((self.dim, self.dim))
        flag = True

        for i in range(self.dim):
            for j in range(i+1):
                if i == j:
                    sq = A[i][j] - np.sum(L**2, axis=1)[i]
                    if sq <= 0:
                        flag = False
                        break
                    else:
                        L[i][j] = np.sqrt(sq)
                else:
                    s = np.sum(L[i][k]*L[j][k] for k in range(j+1))
                    L[i][j] = (A[i][j] - s)/L[j][j]
                    
            if flag == False:
                break
                    
        return flag

    def cholesky(self, A, b):
        
        L = np.zeros((self.dim, self.dim))

        for i in range(self.dim):
            for j in range(i+1):
                if i == j:
                    L[i][j] = np.sqrt(A[i][j] - np.sum(L**2, axis=1)[i])
                else:
                    s = np.sum(L[i][k]*L[j][k] for k in range(j+1))
                    L[i][j] = (A[i][j] - s)/L[j][j]
        
        U = L.T

        y = np.zeros(self.dim)

        for i in range(self.dim):
            s = 0
            for j in range(i+1):
                s += L[i][j-1]*y[j-1]
            y[i] = (b[i] - s)/L[i][i]
        
        x = np.zeros(self.dim)

        for i in range(self.dim-1, -1, -1):
            s = 0
            for j in range(self.dim-1, i-1, -1):
                s += U[i][j]*x[j]
            x[i] = (y[i] - s)/U[i][i]
            
        return x, L
 
def test_1():
    
    A = np.array([[ 6.25, -1,    0.5 ],
                  [-1,     5,    2.12],
                  [ 0.5,   2.12, 3.6 ]])
    
    assert(SecondWindow(3).isSymmetric(A) == True)
    assert(SecondWindow(3).isPositive(A) == True)
    
def test_2():
    
    A = np.array([[6.25, -1,    0.5 ],
                  [1,     5,    2.12],
                  [0.5,   2.15, 3.6 ]])
    
    assert(SecondWindow(3).isSymmetric(A) == False)

def test_3():
    
    A = np.array([[ 6.25, -1,    0.5 ],
                  [-1,    -5,    2.12],
                  [ 0.5,   2.12, 3.6 ]])
    
    assert(SecondWindow(3).isSymmetric(A) == True)
    assert(SecondWindow(3).isPositive(A) == False)
   
def test_4():
    
    A = np.array([[ 6.25, -1,    0.5,  -4.5 ],
                  [-1,     5,    2.12,  3   ],
                  [ 0.5,   2.12, 3.6,   1.63],
                  [-4.5,   3,    1.63,  2.56]])
    
    assert(SecondWindow(4).isSymmetric(A) == True)
    assert(SecondWindow(4).isPositive(A) == False)
    
def test_5():
    
    A = np.array([[ 6.25, -1,     0.5,  -4.5 ],
                  [1,      5,     2.12,  3   ],
                  [ 0.5,   2.15,  3.6,   1.63],
                  [-4.5,   3.57, -1.63,  2.56]])
    
    assert(SecondWindow(4).isSymmetric(A) == False)
    
def test_6():
    
    A = np.array([[ 6.25, -1,     0.5,   2.5 ],
                  [-1,     5,     2.12,  3   ],
                  [ 0.5,   2.12,  3.6,  -1.63],
                  [ 2.5,   3,    -1.63, 10.24]])
    
    assert(SecondWindow(4).isSymmetric(A) == True)
    assert(SecondWindow(4).isPositive(A) == True)

def test_7():
    
    A = np.array([[ 2, -1],
                  [-1,  1]])
    
    b = np.array([3, -2])
    
    x, L = SecondWindow(2).cholesky(A, b)
    expected = np.dot(np.linalg.inv(A), b)
    assert(np.linalg.norm(L - np.linalg.cholesky(A)) < 0.0001)
    assert(np.linalg.norm(x - expected) < 0.0001)
    
def test_8():
    
    A = np.array([[ 6.25, -1,    0.5 ],
                  [-1,     5,    2.12],
                  [ 0.5,   2.12, 3.6 ]])
    
    b = np.array([7.5, -8.68, -0.24])
    
    x, L = SecondWindow(3).cholesky(A, b)
    expected = np.dot(np.linalg.inv(A), b)
    assert(np.linalg.norm(L - np.linalg.cholesky(A)) < 0.0001)
    assert(np.linalg.norm(x - expected) < 0.0001)
    
def test_9():
    
    A = np.array([[ 6.25, -1,     0.5,   2.5 ],
                  [-1,     5,     2.12,  3   ],
                  [ 0.5,   2.12,  3.6,  -1.63],
                  [ 2.5,   3,    -1.63, 10.24]])
    
    b = np.array([10, 7, -5, 3])
    
    x, L = SecondWindow(4).cholesky(A, b)
    expected = np.dot(np.linalg.inv(A), b)
    assert(np.linalg.norm(L - np.linalg.cholesky(A)) < 0.0001)
    assert(np.linalg.norm(x - expected) < 0.0001)
    
def test_10():
    
    A = np.array([[ 3.4,  -2,    0.24,   5,     1   ],
                  [-2,     5.5,  2.12,  -4.3,  -0.4 ],
                  [ 0.24,  2.12, 4.67,   1.43,  3.28],
                  [ 5,    -4.3,  1.43,  12,     4   ],
                  [ 1,    -0.4,  3.28,   4,     6.25]])
    
    assert(SecondWindow(5).isSymmetric(A) == True)
    assert(SecondWindow(5).isPositive(A) == True)
    
    b = np.array([7.43, 5.12, -9.23, 4.68, -10.2])
    
    x, L = SecondWindow(5).cholesky(A, b)
    expected = np.dot(np.linalg.inv(A), b)
    assert(np.linalg.norm(L - np.linalg.cholesky(A)) < 0.0001)
    assert(np.linalg.norm(x - expected) < 0.0001)
            
if __name__ == '__main__':

    app = QApplication(sys.argv)
    test_1()
    print("Test 1 successfully passed")
    test_2()
    print("Test 2 successfully passed")
    test_3()
    print("Test 3 successfully passed")
    test_4()
    print("Test 4 successfully passed")
    test_5()
    print("Test 5 successfully passed")
    test_6()
    print("Test 6 successfully passed")
    test_7()
    print("Test 7 successfully passed")
    test_8()
    print("Test 8 successfully passed")
    test_9()
    print("Test 9 successfully passed")
    test_10()
    print("Test 10 successfully passed")
    w = MainWindow()
    sys.exit(app.exec_())