import numpy as np
import sys
import os
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QCheckBox
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
        reg = QtCore.QRegExp("^[-]?[0-9]{1,4}(\.[0-9]{1,5})?")
        validator = QtGui.QRegExpValidator(reg)
        
        self.t_0_label = QLabel(self)
        self.t_0_label.move(10, 12)
        self.t_0_label.setFont(QFont("Arial", 11))
        self.t_0_label.setText("Введіть початок відрізку розбиття         "+
                               "t_0: ")
        
        self.t_0 = QLineEdit(self)
        self.t_0.move(337, 10)
        self.t_0.resize(80, 20)
        self.t_0.setValidator(validator)
        
        self.t_n_label = QLabel(self)
        self.t_n_label.move(10, 40)
        self.t_n_label.setFont(QFont("Arial", 11))
        self.t_n_label.setText("Введіть кінець відрізку розбиття          "+
                               "t_n: ")
        
        self.t_n = QLineEdit(self)
        self.t_n.move(337, 38)
        self.t_n.resize(80, 20)
        self.t_n.setValidator(validator)
        
        self.N_label = QLabel(self)
        self.N_label.move(10, 68)
        self.N_label.setFont(QFont("Arial", 11))
        self.N_label.setText("Введіть кількість розбиттів    N: ")
        
        self.N = QLineEdit(self)
        self.N.move(337, 66)
        self.N.resize(80, 20)
        self.N.setValidator(validator_int)
        
        self.K_label = QLabel(self)
        self.K_label.move(10, 96)
        self.K_label.setFont(QFont("Arial", 11))
        self.K_label.setText("Введіть кількість гармонік    K: ")
        
        self.K = QLineEdit(self)
        self.K.move(337, 94)
        self.K.resize(80, 20)
        self.K.setValidator(validator_int)
        
        self.cb = QCheckBox('Зберегти результати у файли', self)
        self.cb.move(10, 135)
        self.cb.setFont(QFont("Arial", 11))
        self.cb.stateChanged.connect(self.save)

        but1 = QPushButton("Ввести значення\nв точках розбиття", self)
        but1.move(150, 180)
        but1.resize(130, 40)
        but1.clicked.connect(self.manual_values)
        
        but2 = QPushButton("Згенерувати випадкові\nзначення", self)
        but2.move(300, 180)
        but2.resize(130, 40)
        but2.clicked.connect(self.random_values)
        
        self.text_label = QLabel(self)
        self.text_label.move(450, 20)
        self.text_label.setFont(QFont("Arial", 11))
        self.text_label.setText("Довідка:")
        
        self.text_label = QLabel(self)
        self.text_label.move(450, 50)
        self.text_label.setFont(QFont("Arial", 11))
        self.text_label.setText("1) Період T = t_n - t_0")
        
        self.text_label = QLabel(self)
        self.text_label.move(450, 80)
        self.text_label.setFont(QFont("Arial", 11))
        self.text_label.setText("2) Для більш точного результату")
        
        self.text_label = QLabel(self)
        self.text_label.move(466, 100)
        self.text_label.setFont(QFont("Arial", 11))
        self.text_label.setText("варто обрати N = 2K+1")

        self.setGeometry(150, 150, 680, 250)
        self.setWindowTitle("Апроксимація періодичного сигналу рядами Фур\'є")
        self.setWindowIcon(QIcon('icon.jpg'))
        self.show()
        
    def save(self, state):
        
        if state == QtCore.Qt.Checked:
            self.save_results = True
            if self.route is None:
                self.route = str(QFileDialog.getExistingDirectory(self,
                        "Виберіть робочу директорію для збереження",
                        "/", QFileDialog.ShowDirsOnly))
                if self.route != "":
                    self.route = self.route+"/"
        else:
            self.save_results = False
        
    def manual_values(self):
        
        if (not self.isEmpty() or not self.t_0_less_than_t_n() or 
            not self.N_more_than_2K_1() or not self.positive_N() or
            not self.positive_K()):
            
            QMessageBox.warning(self, 'Warning',
                    '1) Всі поля мають бути заповнені\n'+
                    '2) Значення t_0 має бути меншим, ніж значення t_n\n'+
                    '3) Значення N має бути більшим, ніж 2\n'+
                    '4) Значення N має бути не меншим, ніж 2K+1\n'+
                    '5) Значення K має бути більшим, ніж 0')
        else:
            N = int(self.N.text())
            t_0 = float(self.t_0.text())
            t_n = float(self.t_n.text())
            K = int(self.K.text())
            T = t_n - t_0
            L = T/2
            t = np.arange(t_0, t_n+T/(2*N), T/N)
            y = []
            
            for i in range(N):
                value, ok = QInputDialog.getDouble(self, 'Input Dialog',
                    'Введіть значення в точці t['+str(i)+'] = '+
                    str(round(t[i],3)), decimals=5)
                if ok:
                    y.append(value)
                else:
                    break
            
            y = np.array(y)
            if y.shape[0] == N:
                a, b = self.fourier_coeffs(y, t[:N], K, L)
                t_f = np.arange(t_0, t_n+0.0005, 0.001)
                f_approx = self.fourier_approximation(a, b, t_f, K, L)
                
                y = np.append(y, y[0])
                
                if self.save_results == True:
                    
                    dir_name = 'manual/'
                
                    self.save_results_function(dir_name, a, b, t_f, f_approx)
                
                self.plot_res(t, y, t_f, f_approx)
                
    def random_values(self):
        
        if (not self.isEmpty() or not self.t_0_less_than_t_n() or 
            not self.N_more_than_2K_1() or not self.positive_N() or
            not self.positive_K()):
            
            QMessageBox.warning(self, 'Warning',
                    '1) Всі поля мають бути заповнені\n'+
                    '2) Значення t_0 має бути меншим, ніж значення t_n\n'+
                    '3) Значення N має бути більшим, ніж 2\n'+
                    '4) Значення N має бути не меншим, ніж 2K+1\n'+
                    '5) Значення K має бути більшим, ніж 0')
        else:
            N = int(self.N.text())
            t_0 = float(self.t_0.text())
            t_n = float(self.t_n.text())
            K = int(self.K.text())
            
            T = t_n - t_0
            L = T/2
            
            t = np.arange(t_0, t_n+T/(2*N), T/N)
            y = np.random.randn(N)
            
            a, b = self.fourier_coeffs(y, t[:N], K, L)
            t_f = np.arange(t_0, t_n+0.0005, 0.001)
            f_approx = self.fourier_approximation(a, b, t_f, K, L)
            
            y = np.append(y, y[0])
            
            if self.save_results:
                
                dir_name = 'random/'
                
                self.save_results_function(dir_name, a, b, t_f, f_approx)
                
            self.plot_res(t, y, t_f, f_approx)
            
    def save_results_function(self, dir_name, a, b, t_f, f_approx):
                
        i = 1
        while os.path.exists(self.route+dir_name+'model_'+str(i)+'/') == True:
            i += 1
        
        dir_name = self.route+dir_name+'model_'+str(i)+'/'
        os.makedirs(os.path.dirname(dir_name))
            
        with open(dir_name+'result.txt', 'w') as file:
            
            file.write('Точки розбиття   Значення функції\n\n')
            
            for k in range(t_f.shape[0]-1):
                file.write(str(round(t_f[k], 3))+':             '+
                           str(f_approx[k])+'\n')
            
            file.write(str(round(t_f[t_f.shape[0]-1], 3))+
                       ':             '+str(f_approx[t_f.shape[0]-1]))
                    
        with open(dir_name+'fourier_coeffs.txt', 'w') as file:
            
            file.write('Коефіцієнти ряду Фур\'є\n\n')
            file.write('a[0] = '+str(a[0])+'\n\n')
            
            for k in range(1, a.shape[0]-1):
                file.write('a['+str(k)+'] = '+str(a[k])+'\n')
                
            file.write('a['+str(a.shape[0]-1)+'] = '+
                          str(a[a.shape[0]-1])+'\n\n')
                    
            for k in range(b.shape[0]-1):
                file.write('b['+str(k+1)+'] = '+str(b[k])+'\n')
                
            file.write('b['+str(b.shape[0])+'] = '+str(b[b.shape[0]-1]))
            
    def isEmpty(self):
        
        if (self.N.text() == '' or self.t_0.text() == '' or
            self.t_n.text() == '' or self.K.text() == ''):
            return False
        else:
            return True
        
    def t_0_less_than_t_n(self):
        
        if float(self.t_0.text()) < float(self.t_n.text()):
            return True
        else:
            return False
        
    def positive_N(self):
        
        if int(self.N.text()) >= 3:
            return True
        else:
            return False
        
    def positive_K(self):
        
        if int(self.K.text()) > 0:
            return True
        else:
            return False
        
    def N_more_than_2K_1(self):
        
        if int(self.N.text()) >= 2*int(self.K.text())+1:
            return True
        else:
            return False
        
    def fourier_coeffs(self, y, t, K, L):
        
        a = [2*np.mean(y)]
        b = []
        
        for i in range(1, K+1):
            a.append(2*np.mean(y*np.cos(i*t*np.pi/L)))
            b.append(2*np.mean(y*np.sin(i*t*np.pi/L)))
            
        return np.array(a), np.array(b)
    
    def fourier_approximation(self, a, b, t, K, L):
        
        f = a[0]/2
        for i in range(1, K+1):
            f += a[i]*np.cos(i*t*np.pi/L)
            f += b[i-1]*np.sin(i*t*np.pi/L)
        
        return f
    
    def plot_res(self, t, y, t_f, f_approx):
        
        plt.figure()
        plt.plot(t_f, f_approx)
        plt.scatter(t, y, c='r')
        plt.grid(True)
        plt.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())