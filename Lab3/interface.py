import sys
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon, QFont
from PyQt5 import QtCore, QtGui
from math import *
from sympy.parsing.sympy_parser import (parse_expr, \
    standard_transformations, implicit_multiplication_application, \
    convert_xor)
from sympy.parsing.sympy_tokenize import TokenError
from numpy import e, pi
from runge_kutta_method import runge_kutta_3_order

class MainWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        reg = QtCore.QRegExp("^[-]?[0-9]{1,4}(\.[0-9]{1,5})?")
        validator = QtGui.QRegExpValidator(reg)
        
        self.lbl_function = QLabel(self)
        self.lbl_function.move(10, 12)
        self.lbl_function.setFont(QFont("Arial", 11))
        self.lbl_function.setText("Введіть функцію:             f(x, u) =")
        
        self.func = QLineEdit(self)
        self.func.move(240, 10)
        self.func.resize(150, 20)
        
        self.lbl_initial = QLabel(self)
        self.lbl_initial.move(10, 40)
        self.lbl_initial.setFont(QFont("Arial", 11))
        self.lbl_initial.setText("Введіть початкову умову:   u_0 =")
        
        self.num_initial = QLineEdit(self)
        self.num_initial.move(240, 38)
        self.num_initial.resize(80, 20)
        self.num_initial.setValidator(validator)
        
        self.lbl_a = QLabel(self)
        self.lbl_a.move(10, 68)
        self.lbl_a.setFont(QFont("Arial", 11))
        self.lbl_a.setText("Введіть нижню границю:        a =")
        
        self.a = QLineEdit(self)
        self.a.move(240, 66)
        self.a.resize(80, 20)
        self.a.setValidator(validator)
        
        self.lbl_b = QLabel(self)
        self.lbl_b.move(10, 96)
        self.lbl_b.setFont(QFont("Arial", 11))
        self.lbl_b.setText("Введіть верхню границю:       b =")
        
        self.b = QLineEdit(self)
        self.b.move(240, 94)
        self.b.resize(80, 20)
        self.b.setValidator(validator)

        but = QPushButton("Розв\'язати рівняння", self)
        but.resize(150, 30)
        but.move(230, 130)
        but.clicked.connect(self.solve)

        self.setGeometry(150, 150, 570, 200)
        self.setWindowTitle('Метод Рунге-Кутти для диференціального рівняння')
        self.setWindowIcon(QIcon('icon.jpg'))
        self.show()
    
    def solve(self):
        
        if self.func.text() == '':
            QMessageBox.warning(self, 'Message',
                                'Всі поля мають бути заповнені')
        else:
            try:
                initial_point = float(self.num_initial.text())
                a = float(self.a.text())
                b = float(self.b.text())
            except ValueError:
                QMessageBox.warning(self, 'Message',
                                'Всі поля мають бути заповнені')
            else:
                if self.b_less_a():
                    QMessageBox.warning(self, "Message", 
                                "Нижня границя не може бути більше верхньої")
                else:
                    transformations=(standard_transformations + \
                                     (implicit_multiplication_application,))
                    transformations=transformations + (convert_xor,)
                    try:
                        func = parse_expr(self.func.text(),
                                   transformations = transformations)
                        f = lambda u, x: eval(str(func))
                        x_var, h = np.linspace(a, b, (b-a)*1000+1, retstep=True)
                        u_var = runge_kutta_3_order(f, initial_point, x_var, h)
                        if u_var is None:
                            QMessageBox.warning(self, 'Message',
                                'Неможливо розв\'язати рівняння')
                        else:                        
                            plt.figure(figsize=(15,8))
                            plt.plot(x_var, u_var, label='u(x)')
                            plt.grid(True)
                            plt.legend()
                            plt.show()
                    except NameError:
                        QMessageBox.warning(self, 'Message',
                                        'Неправильно введена функція')
                    except SyntaxError:
                        QMessageBox.warning(self, 'Message',
                                        'Неправильно введена функція')
                    except TypeError:
                        QMessageBox.warning(self, 'Message',
                                        'Неправильно введена функція')
                    except TokenError:
                        QMessageBox.warning(self, 'Message',
                                        'Неправильно введена функція')
    
    def b_less_a(self):
        return float(self.a.text()) > float(self.b.text())
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())