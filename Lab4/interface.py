import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon, QFont
from PyQt5 import QtCore, QtGui
from hooke_jeeves import hooke_jeeves


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
        self.lbl_function.setText("Функція: f(x,y) = 100(x^2-y)^2+(x-1)^2")
        
        self.lbl_initial = QLabel(self)
        self.lbl_initial.move(10, 40)
        self.lbl_initial.setFont(QFont("Arial", 11))
        self.lbl_initial.setText("Введіть початкову точку: x0 = (              ;              )")
        
        self.initial_point_1 = QLineEdit(self)
        self.initial_point_1.move(230, 40)
        self.initial_point_1.resize(40, 20)
        self.initial_point_1.setValidator(validator)
        
        self.initial_point_2 = QLineEdit(self)
        self.initial_point_2.move(290, 40)
        self.initial_point_2.resize(40, 20)
        self.initial_point_2.setValidator(validator)
        
        self.lbl_h = QLabel(self)
        self.lbl_h.move(10, 68)
        self.lbl_h.setFont(QFont("Arial", 11))
        self.lbl_h.setText("Введіть крок:                               h = ")
        
        self.h = QLineEdit(self)
        self.h.move(255, 68)
        self.h.resize(80, 20)
        self.h.setValidator(validator)
        
        self.lbl_eps = QLabel(self)
        self.lbl_eps.move(10, 96)
        self.lbl_eps.setFont(QFont("Arial", 11))
        self.lbl_eps.setText("Введіть точність розрахунку: eps = ")
        
        self.eps = QLineEdit(self)
        self.eps.move(255, 96)
        self.eps.resize(80, 20)
        self.eps.setValidator(validator)

        but = QPushButton("Знайти мінімум", self)
        but.resize(100, 30)
        but.move(250, 140)
        but.clicked.connect(self.solve)

        self.setGeometry(150, 150, 570, 200)
        self.setWindowTitle('Метод Хука-Дживса')
        self.setWindowIcon(QIcon('icon.jpg'))
        self.show()
    
    def solve(self):
        
        try:
            x0 = float(self.initial_point_1.text())
            y0 = float(self.initial_point_2.text())
            delta = float(self.h.text())
            eps = float(self.eps.text())
        except ValueError:
                QMessageBox.warning(self, 'Message',
                                'Всі поля мають бути заповнені')
        else:
            function = lambda x, y: 100*(x**2-y)**2+(x-1)**2
            res, count = hooke_jeeves(function, x0, y0, delta, eps)
            QMessageBox.information(self, 'Message',
                'X_min = {}\nКіл-ть ітерацій = {}\nf(X_min) = {}'.format(res,
                         count, function(res[0], res[1])))
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())