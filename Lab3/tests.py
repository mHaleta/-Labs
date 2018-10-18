import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from math import *
from runge_kutta_method import runge_kutta_3_order
from interface import MainWindow
from PyQt5.QtWidgets import QApplication, QLineEdit

app = QApplication(sys.argv)

def test_positive_result_1():
    f = lambda u, x: u/x+x*cos(x)

    a = 1
    b = 3
    x_var, h = np.linspace(a, b, (b-a)*1000+1, retstep=True)
    u_true = odeint(f, 0.84147, x_var)
    u_var = runge_kutta_3_order(f, 0.84147, x_var, h)
    assert np.linalg.norm(u_true[:,0]-u_var)<0.0001
    
def test_positive_result_2():
    f = lambda u, x: cos(x) + 2*u
    
    a = 2
    b = 6
    x_var, h = np.linspace(a, b, (b-a)*1000+1, retstep=True)
    u_true = odeint(f, 1, x_var)
    u_var = runge_kutta_3_order(f, 1, x_var, h)
    assert np.linalg.norm(u_true[:,0]-u_var)<0.01 

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
    
test_positive_result_1()
print(test_positive_result_1.__name__, "passed")

test_positive_result_2()
print(test_positive_result_2.__name__, "passed")

test_true_b_less_a()
print(test_true_b_less_a.__name__, "passed")

test_false_b_less_a()
print(test_false_b_less_a.__name__, "passed")