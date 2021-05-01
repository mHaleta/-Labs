import numpy as np
from fringing_method import fringing_method

def test_2_dim_matrix():
    np.random.seed(42)
    A = np.random.randint(20, size=(2, 2))
    
    inverted = fringing_method(A, 2)
    
    assert((1/np.linalg.det(A) - np.linalg.det(inverted)) < 10**(-6))
    
def test_3_dim_matrix():
    np.random.seed(34)
    A = np.random.randint(20, size=(3, 3))
    
    inverted = fringing_method(A, 3)
    
    assert((1/np.linalg.det(A) - np.linalg.det(inverted)) < 10**(-6))
    
def test_4_dim_matrix():
    np.random.seed(47)
    A = np.random.randint(20, size=(4, 4))
    
    inverted = fringing_method(A, 4)
    
    assert((1/np.linalg.det(A) - np.linalg.det(inverted)) < 10**(-6))
    
def test_5_dim_matrix():
    np.random.seed(54)
    A = np.random.randint(20, size=(5, 5))
    
    inverted = fringing_method(A, 5)
    
    assert((1/np.linalg.det(A) - np.linalg.det(inverted)) < 10**(-6))
    
def test_6_dim_matrix():
    np.random.seed(12)
    A = np.random.randint(20, size=(6, 6))
    
    inverted = fringing_method(A, 6)
    
    assert((1/np.linalg.det(A) - np.linalg.det(inverted)) < 10**(-6))
    
def test_7_dim_matrix():
    np.random.seed(23)
    A = np.random.randint(20, size=(7, 7))
    
    inverted = fringing_method(A, 7)
    
    assert((1/np.linalg.det(A) - np.linalg.det(inverted)) < 10**(-6))
    
def test_8_dim_matrix():
    np.random.seed(82)
    A = np.random.randint(20, size=(8, 8))
    
    inverted = fringing_method(A, 8)
    
    assert((1/np.linalg.det(A) - np.linalg.det(inverted)) < 10**(-6))
    
def test_9_dim_matrix():
    np.random.seed(45)
    A = np.random.randint(20, size=(9, 9))
    
    inverted = fringing_method(A, 9)
    
    assert((1/np.linalg.det(A) - np.linalg.det(inverted)) < 10**(-6))
    
def test_10_dim_matrix():
    np.random.seed(74)
    A = np.random.randint(20, size=(10, 10))
    
    inverted = fringing_method(A, 10)
    
    assert((1/np.linalg.det(A) - np.linalg.det(inverted)) < 10**(-6))
    

test_2_dim_matrix()
print(test_2_dim_matrix.__name__, "passed")

test_3_dim_matrix()
print(test_3_dim_matrix.__name__, "passed")

test_4_dim_matrix()
print(test_4_dim_matrix.__name__, "passed")

test_5_dim_matrix()
print(test_5_dim_matrix.__name__, "passed")

test_6_dim_matrix()
print(test_6_dim_matrix.__name__, "passed")

test_7_dim_matrix()
print(test_7_dim_matrix.__name__, "passed")

test_8_dim_matrix()
print(test_8_dim_matrix.__name__, "passed")

test_9_dim_matrix()
print(test_9_dim_matrix.__name__, "passed")

test_10_dim_matrix()
print(test_10_dim_matrix.__name__, "passed")
