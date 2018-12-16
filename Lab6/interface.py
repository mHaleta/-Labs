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
from transport_problem import TransportProblem
import numpy as np


class MainWindow(QWidget):
    
    def __init__(self, parent=None):
        
        super().__init__(parent)
        self.number_of_customers = "4"
        self.number_of_vendors = "3"
        self.secondWin = None
        self.initUI()

    def initUI(self):
        
        self.lbl_1 = QLabel(self)
        self.lbl_1.move(10, 12)
        self.lbl_1.setFont(QFont("Arial", 11))
        self.lbl_1.setText("Виберіть кількість cтовпчиків (споживачі): ")
        
        self.combo_1 = QComboBox(self)
        for i in range(9):
            self.combo_1.addItem(str(i+2), i)
        self.combo_1.move(320, 10)
        self.combo_1.setCurrentIndex(2)
        self.combo_1.activated.connect(self.set_number_of_customers)
        
        self.lbl_2 = QLabel(self)
        self.lbl_2.move(10, 40)
        self.lbl_2.setFont(QFont("Arial", 11))
        self.lbl_2.setText("Виберіть кількість рядків (постачальники): ")
        
        self.combo_2 = QComboBox(self)
        for i in range(9):
            self.combo_2.addItem(str(i+2), i)
        self.combo_2.move(320, 40)
        self.combo_2.setCurrentIndex(1)
        self.combo_2.activated.connect(self.set_number_of_vendors)
        
        self.okbutton = QPushButton("OK", self)
        self.okbutton.move(160, 90)
        self.okbutton.clicked.connect(self.openWin)

        self.setGeometry(150, 150, 400, 140)
        self.setWindowTitle('Транспортна задача')
        self.setWindowIcon(QIcon('icon.jpg'))

        self.show()
            
    def set_number_of_customers(self, index):
        self.number_of_customers = self.combo_1.itemText(index)
        
    def set_number_of_vendors(self, index):
        self.number_of_vendors = self.combo_2.itemText(index)
        
    def openWin(self):
        if self.secondWin is not None:
            self.secondWin = None
        self.secondWin = SecondWindow(self.number_of_customers,
                                      self.number_of_vendors)
        self.secondWin.show()
    
class SecondWindow(QWidget):
    
    def __init__(self, number_of_customers,
                 number_of_vendors, parent=None):
        
        super().__init__(parent)
        self.matrix_entry = []
        self.b = []
        self.a = []
        self.combo = QComboBox(self)
        self.m = int(number_of_customers)
        self.n = int(number_of_vendors)
        self.initUI()
        
    def initUI(self):
        
        reg = QtCore.QRegExp("^[0-9]{1,8}(\.[0-9]{1,5})?")
        validator = QtGui.QRegExpValidator(reg)
        
        self.C_str = QLabel(self)
        self.C_str.move((85+50*(self.m))//2, 12)
        self.C_str.setFont(QFont("Arial", 9))
        self.C_str.setText('Матриця тарифів C')
        
        self.sub_1 = QLabel(self)
        self.sub_1.move(127+(100+50*(self.m-1))//2, 17)
        self.sub_1.setFont(QFont("Arial", 7))
        self.sub_1.setText('ij')
        
        for i in range(self.m):
            self.matrix_entry.append([])
            for j in range(self.n):
                self.matrix_entry[i].append(QLineEdit(self))
                self.matrix_entry[i][j].resize(45, 20)
                self.matrix_entry[i][j].move(100+50*i, 35+30*j)
                self.matrix_entry[i][j].setValidator(validator)
                
        self.b_str = QLabel(self)
        self.b_str.move(70+50*(i+2), 12)
        self.b_str.setFont(QFont("Arial", 9))
        self.b_str.setText("Запаси A")
        
        self.sub_2 = QLabel(self)
        self.sub_2.move(124+50*(i+2), 17)
        self.sub_2.setFont(QFont("Arial", 7))
        self.sub_2.setText("i")
                
        for j in range(self.n):
            self.b.append(QLineEdit(self))
            self.b[j].resize(45, 20)
            self.b[j].move(75+50*(i+2), 35+30*j)
            self.b[j].setValidator(validator)
            
        self.a_str = QLabel(self)
        self.a_str.move(25, 84+30*j)
        self.a_str.setFont(QFont("Arial", 9))
        self.a_str.setText("Потреби B")
        
        self.sub_2 = QLabel(self)
        self.sub_2.move(86, 89+30*j)
        self.sub_2.setFont(QFont("Arial", 7))
        self.sub_2.setText("j")
        
        for i in range(self.m):
            self.a.append(QLineEdit(self))
            self.a[i].move(100+50*i, 80+30*j)
            self.a[i].resize(45, 20)
            self.a[i].setValidator(validator)
            
        self.func_label = QLabel(self)
        self.func_label.move(25, 80+30*(j+2))
        self.func_label.setFont(QFont("Arial", 11))
        self.func_label.setText("Цільова функція:")
        
        self.combo.addItem("Мінімальні витрати", 0)
        self.combo.addItem("Максимальний прибуток", 1)
        self.combo.move(150, 77+30*(j+2))
        self.combo.setFont(QFont("Arial", 11))
        self.combo.setCurrentIndex(0)
        
        but = QPushButton("Знайти значення\nцільової функції", self)
        but.resize(130, 40)
        but.move((80+70*(self.m+1))//2, 50+30*(j+5))
        but.setFont(QFont("Arial", 10))
        but.clicked.connect(self.solve)
        
        clear_line_button = QPushButton("Очистити всі поля", self)
        clear_line_button.resize(130, 40)
        clear_line_button.move((70*(self.m+1)-200)//2,
                               50+30*(j+5))
        clear_line_button.setFont(QFont("Arial", 10))
        clear_line_button.clicked.connect(self.clear_line)
        
        self.setGeometry(150, 150, 70+60*(i+3), 35+30*(j+8))
        self.setWindowTitle('Транспортна задача')
        self.setWindowIcon(QIcon('icon.jpg'))

        self.show()
        
    def clear_line(self):
        for i in range(self.m):
            for j in range(self.n):
                self.matrix_entry[i][j].clear()
                
        for i in range(self.n):
            self.b[i].clear()
            
        for i in range(self.m):
            self.a[i].clear()
            
    def isEmpty(self):
        empty = False
        for i in np.reshape(self.matrix_entry, self.m*self.n):
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
        
        for i in self.a:
            if i.text() == "":
                empty = True
                break
            
        return empty
    
    def solve(self):
        if self.isEmpty():
            QMessageBox.warning(self, "Message",
                                "Всі поля мають бути заповнені")
        else:
            
            choise = self.combo.currentIndex()
                
            C = np.zeros((self.n, self.m))
            
            for i in range(self.n):
                for j in range(self.m):
                    C[i][j] = float(self.matrix_entry[j][i].text())
                    
            supply = np.zeros(self.n)
            demand = np.zeros(self.m)
                
            for i in range(self.n):
                supply[i] = float(self.b[i].text())
            
            for i in range(self.m):
                demand[i] = float(self.a[i].text())
                
            if choise == 0:
                result = TransportProblem(C, supply, demand, self.n, self.m)()
            else:
                result = TransportProblem(C, supply, demand,
                                          self.n, self.m, isMax=True)()
                
            X_initial, res_initial, X, optimal = result
            
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            if choise == 0:
                msg.setText("Початковий опорний план:\n"+
                            "{}\n\n".format(X_initial)+
                            "Початкові витрати: {}\n\n".format(res_initial)+
                            "Оптимальний план:\n"+
                            "{}\n\n".format(X)+
                            "Мінімальні витрати: {}".format(optimal))
            else:
                msg.setText("Початковий опорний план:\n"+
                            "{}\n\n".format(X_initial)+
                            "Початковий прибуток: {}\n\n".format(res_initial)+
                            "Оптимальний план:\n"+
                            "{}\n\n".format(X)+
                            "Максимальний прибуток: {}".format(optimal))
            msg.setWindowTitle("Результат")
            msg.setFont(QFont("Arial", 10))
            msg.exec_()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())