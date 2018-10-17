import sys
import numpy as np
from interface import MainWindow
from PyQt5.QtWidgets import QApplication, QLineEdit
from middle_rectangles_method import middle_rectangles_method

app = QApplication(sys.argv)

def test_positive_result():
    f = lambda x: x**2
    I = lambda x: x**3/3
    a = 1
    b = 5
    res = middle_rectangles_method(f, a, b, 10000)
    assert np.abs(res - (I(b)-I(a))) < 0.001

def test_true_num():
    window = MainWindow()
    window.num_breakdown = QLineEdit(window)
    window.num_breakdown.setText("1")
    assert window.num_low()

def test_false_num():
    window = MainWindow()
    window.num_breakdown = QLineEdit(window)
    window.num_breakdown.setText("5")
    assert not window.num_low()

def test_true_b_less_a():
    window = MainWindow()
    window.a = QLineEdit(window)
    window.b = QLineEdit(window)
    window.a.setText("5")
    window.b.setText("1")
    assert window.b_less_a() 
    
def test_false_b_less_a():
    window = MainWindow()
    window.a = QLineEdit(window)
    window.b = QLineEdit(window)
    window.a.setText("1")
    window.b.setText("5")
    assert not window.b_less_a() 


test_positive_result()
print(test_positive_result.__name__, "passed")

test_true_num()
print(test_true_num.__name__, "passed")

test_false_num()
print(test_false_num.__name__, "passed")

test_true_b_less_a()
print(test_true_b_less_a.__name__, "passed")

test_false_b_less_a()
print(test_false_b_less_a.__name__, "passed")