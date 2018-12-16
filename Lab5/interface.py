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
from simplex import Simplex, simplex_method_fictitious_basis
import numpy as np


class MainWindow(QWidget):
    
    def __init__(self, parent=None):
        
        super().__init__(parent)
        self.number_of_variables = "3"
        self.number_of_limitations = "3"
        self.secondWin = None
        self.initUI()

    def initUI(self):
        
        self.lbl_1 = QLabel(self)
        self.lbl_1.move(10, 12)
        self.lbl_1.setFont(QFont("Arial", 11))
        self.lbl_1.setText("Виберіть кількість змінних: ")
        
        self.combo_1 = QComboBox(self)
        for i in range(11):
            self.combo_1.addItem(str(i+2), i)
        self.combo_1.move(320, 10)
        self.combo_1.setCurrentIndex(1)
        self.combo_1.activated.connect(self.set_number_of_variables)
        
        self.lbl_2 = QLabel(self)
        self.lbl_2.move(10, 40)
        self.lbl_2.setFont(QFont("Arial", 11))
        self.lbl_2.setText("Виберіть кількість рядків (обмежень): ")
        
        self.text_label = QLabel(self)
        self.text_label.move(10, 70)
        self.text_label.setText("Обмеження типу x_i >= 0 не враховуйте")
        self.text_label.setFont(QFont("Arial", 8, italic=True))
        
        self.combo_2 = QComboBox(self)
        for i in range(12):
            self.combo_2.addItem(str(i+1), i)
        self.combo_2.move(320, 40)
        self.combo_2.setCurrentIndex(2)
        self.combo_2.activated.connect(self.set_number_of_limitations)
        
        self.okbutton = QPushButton("OK", self)
        self.okbutton.move(160, 120)
        self.okbutton.clicked.connect(self.openWin)

        self.setGeometry(150, 150, 400, 170)
        self.setWindowTitle('Симплекс-метод')
        self.setWindowIcon(QIcon('icon.jpg'))

        self.show()
            
    def set_number_of_variables(self, index):
        self.number_of_variables = self.combo_1.itemText(index)
        
    def set_number_of_limitations(self, index):
        self.number_of_limitations = self.combo_2.itemText(index)
        
    def openWin(self):
        if self.secondWin is not None:
            self.secondWin = None
        self.secondWin = SecondWindow(self.number_of_variables,
                                      self.number_of_limitations)
        self.secondWin.show()
    
class SecondWindow(QMainWindow):
    
    def __init__(self, number_of_variables,
                 number_of_limitations, parent=None):
        
        super().__init__(parent, QtCore.Qt.Window)
        self.matrix_entry = []
        self.x_str = []
        self.sign = []
        self.b = []
        self.z = []
        self.z_str = []
        self.number_of_variables = int(number_of_variables)
        self.number_of_limitations = int(number_of_limitations)
        self.initUI()
        
    def initUI(self):
        
        reg = QtCore.QRegExp("^[-]?[0-9]{1,8}(\.[0-9]{1,5})?")
        validator = QtGui.QRegExpValidator(reg)
        
        for i in range(self.number_of_variables):
            self.x_str.append(QLabel("x"+str(i+1), self))
            self.x_str[i].move(30+70*i, 10)
            self.x_str[i].setFont(QFont("Arial", 9))
            
        self.b_lbl = QLabel("B", self)
        self.b_lbl.move(30+70*(i+2), 10)
        self.b_lbl.setFont(QFont("Arial", 9))
        
        for i in range(self.number_of_variables):
            self.matrix_entry.append([])
            for j in range(self.number_of_limitations):
                self.matrix_entry[i].append(QLineEdit(self))
                self.matrix_entry[i][j].resize(45, 20)
                self.matrix_entry[i][j].move(10+70*i, 35+30*j)
                self.matrix_entry[i][j].setValidator(validator)
                
        for j in range(self.number_of_limitations):
            self.sign.append(QComboBox(self))
            item = ["<=", "=", ">="]
            for itr in range(3):
                self.sign[j].addItem(item[itr], itr)
            self.sign[j].move(10+70*(i+1), 35+30*j)
            self.sign[j].resize(45, 20)
        
        for j in range(self.number_of_limitations):
            self.b.append(QLineEdit(self))
            self.b[j].resize(45, 20)
            self.b[j].move(10+70*(i+2), 35+30*j)
            self.b[j].setValidator(validator)
            
        self.f_lbl = QLabel("Функція цілі Z", self)
        self.f_lbl.move(10, 35+30*(j+2))
        self.f_lbl.setFont(QFont("Arial", 11))
        
        for i in range(self.number_of_variables):
            self.z_str.append(QLabel("x"+str(i+1), self))
            self.z_str[i].move(30+70*i, 35+30*(j+3))
            self.z_str[i].setFont(QFont("Arial", 9))
            
        self.z_str.append(QLabel("C", self))
        self.z_str[-1].move(30+70*(i+1), 35+30*(j+3))
        self.z_str[-1].setFont(QFont("Arial", 9))
        
        self.z_str.append(QLabel("extr", self))
        self.z_str[-1].move(30+70*(i+2), 35+30*(j+3))
        self.z_str[-1].setFont(QFont("Arial", 9))
            
        for i in range(self.number_of_variables+1):
            self.z.append(QLineEdit(self))
            self.z[i].resize(45, 20)
            self.z[i].move(10+70*i, 35+30*(j+4))
            self.z[i].setValidator(validator)
            
        self.sign.append(QComboBox(self))
        self.sign[-1].addItem("min", 0)
        self.sign[-1].addItem("max", 1)
        self.sign[-1].move(10+70*(i+1), 35+30*(j+4))
        self.sign[-1].resize(45, 20)
        
        but = QPushButton("Знайти екстремум", self)
        but.resize(130, 30)
        but.move((80+70*(self.number_of_variables+1))//2, 50+30*(j+5))
        but.clicked.connect(self.solve)
        
        clear_line_button = QPushButton("Очистити всі поля", self)
        clear_line_button.resize(130, 30)
        clear_line_button.move((70*(self.number_of_variables+1)-200)//2,
                               50+30*(j+5))
        clear_line_button.clicked.connect(self.clear_line)
        
        self.setGeometry(150, 150, 70+70*(self.number_of_variables+1),
                         70+30*(j+6))
        self.setWindowTitle('Симплекс-метод')
        self.setWindowIcon(QIcon('icon.jpg'))
        
    def clear_line(self):
        for i in range(self.number_of_variables):
            for j in range(self.number_of_limitations):
                self.matrix_entry[i][j].clear()
                
        for i in range(self.number_of_limitations):
            self.b[i].clear()
            
        for i in range(self.number_of_variables+1):
            self.z[i].clear()
        
    def isEmpty(self):
        empty = False
        for i in np.reshape(self.matrix_entry,
                            self.number_of_variables*
                            self.number_of_limitations):
            if i.text() == "":
                empty = True
                break
        if empty:
            return empty
        
        for i in self.b:
            if i.text() == "":
                empty = True
                break
        if empty:
            return empty
        
        for i in self.z:
            if i.text() == "":
                empty = True
                break
            
        return empty
                
    
    def solve(self):
        
        isMax = False
        isEqual = False
        
        if self.isEmpty():
            QMessageBox.warning(self, "Message",
                                "Всі поля мають бути заповнені")
        else:
            
            signs = []
            for i in range(self.number_of_limitations+1):
                signs.append(self.sign[i].currentText())
                
            X = np.zeros((self.number_of_limitations+1,
                          self.number_of_variables+1))
        
            for i in range(self.number_of_limitations):
                X[i][0] = float(self.b[i].text())
            X[i+1][0] = float(self.z[-1].text())
            
            for i in range(self.number_of_limitations):
                for j in range(self.number_of_variables):
                    X[i][j+1] = float(self.matrix_entry[j][i].text())
                
            for i in range(self.number_of_variables):
                X[-1][i+1] = float(self.z[i].text())
            
            for i in range(self.number_of_limitations):
                if signs[i] == ">=":
                    X[i] = (-1)*X[i]
                
            if signs[-1] == "min":
                X[-1][1:] = (-1)*X[-1][1:]
            else:
                X[-1][0] = (-1)*X[-1][0]
                isMax = True
                
            initial_shape = X.shape[1]
                
            if "=" in signs:
                isEqual = True
                rows_with_fict_vars = []
                X = np.insert(X, X.shape[0], np.zeros(X.shape[1]), axis=0)
                for i in range(self.number_of_limitations):
                    if X[i][0] < 0 and signs[i] != "=":
                        X = np.concatenate((X, np.zeros((X.shape[0], 1))), axis=1)
                        X[i] = (-1)*X[i]
                        X[i][-1] = -1.
                        X[-1] += X[i]
                        rows_with_fict_vars.append(i)
                    elif X[i][0] < 0 and signs[i] == "=":
                        X[i] = (-1)*X[i]
                        X[-1] += X[i]
                        rows_with_fict_vars.append(i)
                    elif X[i][0] >= 0 and signs[i] == "=":
                        X[-1] += X[i]
                        rows_with_fict_vars.append(i)
                        
                rows_with_fict_vars = np.array(rows_with_fict_vars)
            
            if isMax:
                if not isEqual:
                    res, vector = Simplex(X).use_appropriate_simplex_method()
                    if vector is not None:
                        msg = QMessageBox(self)
                        msg.setIcon(QMessageBox.Information)
                        msg.setText("Max(Z) = {}\nX = {}".format(-res, vector))
                        msg.setWindowTitle("Результат")
                        msg.setFont(QFont("Arial", 13))
                        msg.exec_()
                    else:
                        msg = QMessageBox(self)
                        msg.setIcon(QMessageBox.Information)
                        msg.setText(res.replace("мінімум", "максимум"))
                        msg.setWindowTitle("Результат")
                        msg.setFont(QFont("Arial", 13))
                        msg.exec_()
                else:
                    res, vector = simplex_method_fictitious_basis(
                                    X, rows_with_fict_vars, initial_shape
                                )
                    if vector is not None:
                        msg = QMessageBox(self)
                        msg.setIcon(QMessageBox.Information)
                        msg.setText("Max(Z) = {}\nX = {}".format(-res, vector))
                        msg.setWindowTitle("Результат")
                        msg.setFont(QFont("Arial", 13))
                        msg.exec_()
                    else:
                        msg = QMessageBox(self)
                        msg.setIcon(QMessageBox.Information)
                        msg.setText(res.replace("мінімум", "максимум"))
                        msg.setWindowTitle("Результат")
                        msg.setFont(QFont("Arial", 13))
                        msg.exec_()
            else:
                if not isEqual:
                    res, vector = Simplex(X).use_appropriate_simplex_method()
                    if vector is not None:
                        msg = QMessageBox(self)
                        msg.setIcon(QMessageBox.Information)
                        msg.setText("Min(Z) = {}\nX = {}".format(res, vector))
                        msg.setWindowTitle("Результат")
                        msg.setFont(QFont("Arial", 13))
                        msg.exec_()
                    else:
                        msg = QMessageBox(self)
                        msg.setIcon(QMessageBox.Information)
                        msg.setText(res)
                        msg.setWindowTitle("Результат")
                        msg.setFont(QFont("Arial", 13))
                        msg.exec_()
                else:
                    res, vector = simplex_method_fictitious_basis(
                                    X, rows_with_fict_vars, initial_shape
                                )
                    if vector is not None:
                        msg = QMessageBox(self)
                        msg.setIcon(QMessageBox.Information)
                        msg.setText("Min(Z) = {}\nX = {}".format(res, vector))
                        msg.setWindowTitle("Результат")
                        msg.setFont(QFont("Arial", 13))
                        msg.exec_()
                    else:
                        msg = QMessageBox(self)
                        msg.setIcon(QMessageBox.Information)
                        msg.setText(res)
                        msg.setWindowTitle("Результат")
                        msg.setFont(QFont("Arial", 13))
                        msg.exec_()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())