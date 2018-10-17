#from __future__ import division
import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon, QFont
from PyQt5 import QtCore, QtGui
from sympy import *
from sympy.parsing.sympy_parser import (parse_expr, \
    standard_transformations, implicit_multiplication_application, \
    convert_xor)
from sympy.parsing.sympy_tokenize import TokenError
from mpmath import e, pi
from middle_rectangles_method import middle_rectangles_method


class MainWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        reg_num = QtCore.QRegExp("[0-9]{1,6}")
        validator_num = QtGui.QRegExpValidator(reg_num)
        reg = QtCore.QRegExp("^[-]?[0-9]{1,4}(\.[0-9]{1,5})?")
        validator = QtGui.QRegExpValidator(reg)
        
        self.lbl_function = QLabel(self)
        self.lbl_function.move(10, 12)
        self.lbl_function.setFont(QFont("Arial", 11))
        self.lbl_function.setText("Введіть функцію:     y(x)   =")
        
        self.func = QLineEdit(self)
        self.func.move(210, 10)
        self.func.resize(150, 20)
        
        self.lbl_breakdown = QLabel(self)
        self.lbl_breakdown.move(10, 40)
        self.lbl_breakdown.setFont(QFont("Arial", 11))
        self.lbl_breakdown.setText("Введіть кількість розбиттів: ")
        
        self.num_breakdown = QLineEdit(self)
        self.num_breakdown.move(210, 38)
        self.num_breakdown.resize(80, 20)
        self.num_breakdown.setValidator(validator_num)
        
        self.lbl_a = QLabel(self)
        self.lbl_a.move(10, 68)
        self.lbl_a.setFont(QFont("Arial", 11))
        self.lbl_a.setText("Введіть нижню границю: ")
        
        self.a = QLineEdit(self)
        self.a.move(210, 66)
        self.a.resize(80, 20)
        self.a.setValidator(validator)
        
        self.lbl_b = QLabel(self)
        self.lbl_b.move(10, 96)
        self.lbl_b.setFont(QFont("Arial", 11))
        self.lbl_b.setText("Введіть верхню границю: ")
        
        self.b = QLineEdit(self)
        self.b.move(210, 94)
        self.b.resize(80, 20)
        self.b.setValidator(validator)

        but = QPushButton("Інтегрувати", self)
        but.resize(100, 30)
        but.move(250, 140)
        but.clicked.connect(self.solve)

        self.setGeometry(150, 150, 570, 200)
        self.setWindowTitle('Метод середніх прямокутників')
        self.setWindowIcon(QIcon('icon.jpg'))
        self.show()
    
    def solve(self):
        
        if self.func.text() == '':
            QMessageBox.warning(self, 'Message',
                                'Всі поля мають бути заповнені')
        else:
            try:
                num_breakdown = int(self.num_breakdown.text())
                a = float(self.a.text())
                b = float(self.b.text())
            except ValueError:
                QMessageBox.warning(self, 'Message',
                                'Всі поля мають бути заповнені')
            else:
                if self.num_low():
                    QMessageBox.warning(self, "Message", 
                                "Занадто мало проміжків розбиття")
                elif self.b_less_a():
                    QMessageBox.warning(self, "Message", 
                                "Нижня границя не може бути більше верхньої")
                else:
                    transformations=(standard_transformations + \
                                     (implicit_multiplication_application,))
                    transformations=transformations + (convert_xor,)
                    try:
                        func = parse_expr(self.func.text(),
                                   transformations = transformations)
                        f = lambda x: eval(str(func))
                        res = middle_rectangles_method(f, a, b, num_breakdown)
                        QMessageBox.information(self, "Message",
                                                "Integral = "+str(res))
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
            
    def num_low(self):
        return int(self.num_breakdown.text()) < 3
    
    def b_less_a(self):
        return float(self.a.text()) > float(self.b.text())
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())