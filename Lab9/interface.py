import numpy as np
import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtGui import QIcon, QFont
from PyQt5 import QtCore, QtGui

class MainWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.save_results = False
        self.route = None

    def initUI(self):
        
        reg_int = QtCore.QRegExp("[0-9]{1,8}")
        validator_int = QtGui.QRegExpValidator(reg_int)
        
        self.N_label = QLabel(self)
        self.N_label.move(10, 68)
        self.N_label.setFont(QFont("Arial", 11))
        self.N_label.setText("Введіть кількість точок    N: ")
        
        self.N = QLineEdit(self)
        self.N.move(337, 66)
        self.N.resize(80, 20)
        self.N.setValidator(validator_int)

        but1 = QPushButton("Ввести дані вручну", self)
        but1.move(150, 180)
        but1.resize(130, 40)
        but1.clicked.connect(self.manual_values)
        
        but2 = QPushButton("Згенерувати випадкові\nзначення", self)
        but2.move(300, 180)
        but2.resize(130, 40)
        but2.clicked.connect(self.random_values)

        self.setGeometry(150, 150, 680, 250)
        self.setWindowTitle("Експоненційна регресія")
        self.setWindowIcon(QIcon('icon.jpg'))
        self.show()
        
    def manual_values(self):
        
        if self.isEmpty():
            
            QMessageBox.warning(self, 'Warning',
                    '1) Всі поля мають бути заповнені\n'+
                    '2) Значення N має бути більшим, ніж 2\n')
        else:
            N = int(self.N.text())
            
            x = []
            y = []
            
            for i in range(N):
                
                value, ok = QInputDialog.getDouble(self, 'Input Dialog',
                    'Введіть точку x['+str(i)+']', decimals=5)
                if ok:
                    x.append(value)
                else:
                    break
                
                value, ok = QInputDialog.getDouble(self, 'Input Dialog',
                    'Введіть значення в точці x['+str(i)+'] = '+
                    str(round(x[i],3)), decimals=5)
                if ok:
                    y.append(value)
                else:
                    break
            
            x = np.array(x)
            y = np.array(y)
            
            if y.shape[0] == N:
                A, B, C = self.expon_fit(x, y)
                x_plot = np.linspace(np.min(x), np.max(x)+1, num=1001,
                                     endpoint=True)
                
                y_plot_1 = self.expon_predict(x, A, B, C)
                y_plot_2 = self.expon_predict(x_plot, A, B, C)
                
                error = np.linalg.norm(y - y_plot_1)/np.linalg.norm(y)
                
                self.plot_res(x, y, x_plot, y_plot_2, error, A, B, C)
                
    def random_values(self):
        
        if self.isEmpty():
            
            QMessageBox.warning(self, 'Warning',
                    '1) Всі поля мають бути заповнені\n'+
                    '2) Значення N має бути більшим, ніж 2\n')
        else:
            N = int(self.N.text())
            
            x = np.arange(N)
            y = np.random.exponential(2, (N, ))
            y.sort()
            
            A, B, C = self.expon_fit(x, y)
            x_plot = np.linspace(0, np.max(x)+1, num=1001, endpoint=True)
            y_plot_1 = self.expon_predict(x, A, B, C)
            y_plot_2 = self.expon_predict(x_plot, A, B, C)
            
            error = np.linalg.norm(y - y_plot_1)/np.linalg.norm(y)
                
            self.plot_res(x, y, x_plot, y_plot_2, error, A, B, C)
                
    def isEmpty(self):
        
        if self.N.text() == '':
            return True
        else:
            return False
        
    def positive_N(self):
        
        if int(self.N.text()) > 2:
            return True
        else:
            return False
        
    def expon_fit(self, x, y):
        x_prime = np.zeros(x.shape[0]-1)
        y_prime = np.zeros(y.shape[0]-1)
        
        for i in range(1, x_prime.shape[0]+1):
            x_prime[i-1] = (x[i] + x[i-1])/2
            y_prime[i-1] = (y[i] - y[i-1])/(x[i] - x[i-1])
            
        y_prime = np.log(y_prime)
        
        b = ((x_prime @ y_prime) - np.mean(x_prime)*np.sum(y_prime))/ \
            ((x_prime @ x_prime) - np.mean(x_prime)*np.sum(x_prime))
        
        a = np.mean(y_prime) - b*np.mean(x_prime)
        
        B = -b
        A = np.exp(a)/B
        C = np.mean(y - A*(1-np.exp(-B*x)))
        
        return A, B, C
    
    def expon_predict(self, x, A, B, C):
        y = A*(1-np.exp(-B*x))+C
        
        return y
    
    def plot_res(self, x, y, x_plot, y_plot, error, A, B, C):
        
        plt.figure()
        plt.plot(x_plot, y_plot)
        plt.scatter(x, y, c='r')
        plt.title('A = {}, B = {}, C = {}'.format(A.round(5), B.round(5), C.round(5)))
        plt.grid(True)
        plt.text(np.min(x), np.max(y_plot)-2, s='error = {}'.format(error.round(5)))
        plt.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())