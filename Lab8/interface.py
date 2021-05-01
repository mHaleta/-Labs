import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QComboBox
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
        self.n = "4"
        self.m = "3"
        self.secondWin = None
        self.initUI()

    def initUI(self):
        
        self.lbl_1 = QLabel(self)
        self.lbl_1.move(10, 12)
        self.lbl_1.setFont(QFont("Arial", 11))
        self.lbl_1.setText("Виберіть кількість рядків матриці коефіцієнтів: ")
        
        self.combo_1 = QComboBox(self)
        for i in range(9):
            self.combo_1.addItem(str(i+2), i)
        self.combo_1.move(355, 10)
        self.combo_1.setCurrentIndex(2)
        self.combo_1.activated.connect(self.set_n)
        
        self.lbl_2 = QLabel(self)
        self.lbl_2.move(10, 40)
        self.lbl_2.setFont(QFont("Arial", 11))
        self.lbl_2.setText("Виберіть кількість стовпців матриці коефіцієнтів: ")
        
        self.combo_2 = QComboBox(self)
        for i in range(9):
            self.combo_2.addItem(str(i+2), i)
        self.combo_2.move(355, 40)
        self.combo_2.setCurrentIndex(1)
        self.combo_2.activated.connect(self.set_m)
        
        self.okbutton = QPushButton("OK", self)
        self.okbutton.move(160, 90)
        self.okbutton.clicked.connect(self.openWin)

        self.setGeometry(150, 150, 400, 140)
        self.setWindowTitle('Розв\'язання системи за допомогою сингулярного розкладення')
        self.setWindowIcon(QIcon('icon.jpg'))

        self.show()
            
    def set_n(self, index):
        self.n = self.combo_1.itemText(index)
        
    def set_m(self, index):
        self.m = self.combo_2.itemText(index)
        
    def openWin(self):
        if self.secondWin is not None:
            self.secondWin = None
        self.secondWin = SecondWindow(self.n, self.m)
        self.secondWin.show()
        
        
class SecondWindow(QWidget):
    
    def __init__(self, n, m, parent=None):
        
        super().__init__(parent, QtCore.Qt.Window)
        self.matrix_entry = []
        self.x_str = []
        self.rows = int(n)
        self.cols = int(m)
        self.initUI()
        
    def initUI(self):
        
        reg = QtCore.QRegExp("^[-]?[0-9]*\.?[0-9]+")
        validator = QtGui.QRegExpValidator(reg)
        
        for i in range(self.cols+1):
            self.matrix_entry.append([])
            self.x_str.append([])
            
            for j in range(self.rows):
                self.matrix_entry[i].append(QLineEdit(self))
                self.matrix_entry[i][j].resize(30, 20)
                
                if i == self.cols:
                    self.matrix_entry[i][j].move(120+70*(i-1), 12+30*j)
                else:
                    self.matrix_entry[i][j].move(10+70*i, 12+30*j)
                    self.x_str[i].append(QLabel("x"+str(i+1), self))
                    self.x_str[i][j].move(45+70*i, 15+30*j)
                
                self.matrix_entry[i][j].setValidator(validator)
                
        for i in range(self.rows):
            equal_label = QLabel("=", self)
            equal_label.move(85+70*(self.cols-1), 15+30*i)
                
        but_1 = QPushButton("Розв\'язати систему", self)
        but_1.resize(130, 30)
        but_1.move(80, 40+30*self.rows)
        but_1.clicked.connect(self.solve)
        
        but_3 = QPushButton("Очистити всі поля", self)
        but_3.resize(130, 30)
        but_3.move(400, 40+30*self.rows)
        but_3.clicked.connect(self.clear)
        
        self.setGeometry(150, 150, 610, 400)
        self.setWindowTitle('Розв\'язання системи за допомогою сингулярного розкладення')
        self.setWindowIcon(QIcon('icon.jpg'))
        
        self.show()
        
    def clear(self):
        for i in range(self.cols+1):
            for j in range(self.rows):
                self.matrix_entry[i][j].clear()
                
    def isEmpty(self):
        empty = False
        for i in np.reshape(self.matrix_entry, self.rows*(self.cols+1)):
            if i.text() == "":
                empty = True
                break
            
        return empty
                
    def solve(self):
        if self.isEmpty():
            QMessageBox.warning(self, "Message",
                                "Всі поля мають бути заповнені")
        else:
            A = np.zeros((self.rows, self.cols))
            B = np.zeros(self.rows)
            
            for i in range(self.rows):
                for j in range(self.cols):
                    A[i][j] = float(self.matrix_entry[j][i].text())
                    
            for i in range(self.rows):
                B[i] = float(self.matrix_entry[self.cols][i].text())
                        
            
            eigen_values, V = np.linalg.eig(A.T @ A)
            S = np.sqrt(eigen_values)*np.eye((A.T @ A).shape[0])
            U = A @ V @ np.linalg.inv(S)
            X = V @ np.linalg.inv(S) @ U.T @ B
            error = np.linalg.norm(B - A @ X)/np.linalg.norm(B)
            QMessageBox.information(self, "Message",
                                    "X = {}\n\n".format(X) + \
                                    "error = {}".format(error))
                
                
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
