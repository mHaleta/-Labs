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
from fringing_method import fringing_method
import numpy as np

class MainWindow(QWidget):
    
    def __init__(self, parent=None):
        
        super().__init__(parent)
        self.matrix_dimension = "3"
        self.secondWin = None
        self.initUI()

    def initUI(self):
        
        self.lbl = QLabel(self)
        self.lbl.move(10, 12)
        self.lbl.setFont(QFont("Arial", 11))
        self.lbl.setText("Виберіть розмірність квадратної матриці: ")
        
        self.combo = QComboBox(self)
        for i in range(9):
            self.combo.addItem(str(i+2), i)
        self.combo.move(320, 10)
        self.combo.setCurrentIndex(1)
        self.combo.activated.connect(self.set_matrix_dimension)
        
        self.okbutton = QPushButton("OK", self)
        self.okbutton.move(160, 60)
        self.okbutton.clicked.connect(self.openWin)

        self.setGeometry(150, 150, 400, 100)
        self.setWindowTitle('Метод окантування для оберненої матриці')
        self.setWindowIcon(QIcon('icon.jpg'))

        self.show()
            
    def set_matrix_dimension(self, index):
        self.matrix_dimension = self.combo.itemText(index)
        
    def openWin(self):
        if self.secondWin is not None:
            self.secondWin = None
        self.secondWin = SecondWindow(self.matrix_dimension)
        self.secondWin.show()
    
class SecondWindow(QWidget):
    
    def __init__(self, matrix_dimension, parent=None):
        
        super().__init__(parent)
        self.matrix_entry = []
        self.dim = int(matrix_dimension)
        self.initUI()
        
    def initUI(self):
        
        reg = QtCore.QRegExp("^[-]?[0-9]*\.?[0-9]+")
        validator = QtGui.QRegExpValidator(reg)
        
        for i in range(self.dim):
            self.matrix_entry.append([])
            
            for j in range(self.dim):
                self.matrix_entry[i].append(QLineEdit(self))
                self.matrix_entry[i][j].resize(30, 20)
                
                self.matrix_entry[i][j].move(10+70*i, 12+30*j)
                
                self.matrix_entry[i][j].setValidator(validator)
        
        
        but_1 = QPushButton("Обернена матриця", self)
        but_1.resize(130, 30)
        but_1.move(80, 40+30*self.dim)
        but_1.clicked.connect(self.invert)
        
        but_2 = QPushButton("Випадкові значення\nелементів", self)
        but_2.resize(130, 30)
        but_2.move(240, 40+30*self.dim)
        but_2.clicked.connect(self.generate_random)
        
        but_3 = QPushButton("Очистити всі поля", self)
        but_3.resize(130, 30)
        but_3.move(400, 40+30*self.dim)
        but_3.clicked.connect(self.clear)
        
        self.setGeometry(150, 150, 610, 400)
        self.setWindowTitle('Метод окантування для оберненої матриці')
        self.setWindowIcon(QIcon('icon.jpg'))
        
        self.show()
        
    def clear(self):
        for i in range(self.dim):
            for j in range(self.dim):
                self.matrix_entry[i][j].clear()
                
    def generate_random(self):
        A = np.random.randint(20, size=(self.dim, self.dim))
        
        for i in range(self.dim):
            for j in range(self.dim):
                self.matrix_entry[i][j].setText(str(A[j][i]))
            
    def isEmpty(self):
        empty = False
        for i in np.reshape(self.matrix_entry, self.dim*self.dim):
            if i.text() == "":
                empty = True
                break
            
        return empty
    
    def isDegenerate(self, A):
        determinant = np.linalg.det(A)
        if determinant == 0.:
            return True
        else:
            return False
    
    def invert(self):
        if self.isEmpty():
            QMessageBox.warning(self, "Message",
                                "Всі поля мають бути заповнені")
        else:
            A = np.zeros((self.dim, self.dim))
            
            for i in range(self.dim):
                for j in range(self.dim):
                    A[i][j] = float(self.matrix_entry[j][i].text())
                    
            if self.isDegenerate(A):
                QMessage.warning(self, "Message", "Вироджена матриця")
            else:
                inverted = fringing_method(A, self.dim)
                
                if isinstance(inverted, str):
                    QMessageBox.warning(self, "Message", inverted)
                else:
                    QMessageBox.information(self, "Message",
                                            str(inverted.round(3)))
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
