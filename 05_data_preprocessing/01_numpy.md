## **1. Introduction to NumPy**
NumPy (Numerical Python) is an open-source Python library for numerical computing. It provides a powerful N-dimensional array object, mathematical functions, random number capabilities, and tools for integrating C/C++ and Fortran code.

### **Why Use NumPy?**
- Faster than Python lists due to optimized C backend.
- Uses less memory and provides built-in mathematical functions.
- Supports multi-dimensional arrays and matrices.
- Enables vectorized operations for efficiency.

### **Installation**
```bash
pip install numpy
```

---

## **2. NumPy Arrays**
### **Creating Arrays**
```python
import numpy as np

# Creating a 1D array
arr1 = np.array([1, 2, 3, 4, 5])

# Creating a 2D array
arr2 = np.array([[1, 2, 3], [4, 5, 6]])

print(arr1)
print(arr2)
```

### **Array Properties**
```python
print(arr2.shape)  # Returns (2,3) -> Rows x Columns
print(arr2.ndim)   # Number of dimensions
print(arr2.size)   # Total number of elements
print(arr2.dtype)  # Data type of elements
```

### **Generating Special Arrays**
```python
np.zeros((3,3))      # 3x3 matrix of zeros
np.ones((2,2))       # 2x2 matrix of ones
np.eye(3)            # 3x3 Identity matrix
np.full((2,3), 5)    # 2x3 matrix filled with 5
np.arange(1, 10, 2)  # Array from 1 to 10 with step 2
```

---

## **3. NumPy Operations**
### **Mathematical Operations**
```python
arr = np.array([1, 2, 3, 4])

print(arr + 2)  # [3 4 5 6]
print(arr * 3)  # [3 6 9 12]
print(arr / 2)  # [0.5 1.0 1.5 2.0]
print(arr ** 2) # [1 4 9 16]
```

### **Matrix Operations**
```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

print(A + B)  # Matrix addition
print(A - B)  # Matrix subtraction
print(A @ B)  # Matrix multiplication
print(A.T)    # Transpose of A
```

### **Statistical Functions**
```python
arr = np.array([1, 2, 3, 4, 5])

print(np.mean(arr))   # Mean
print(np.median(arr)) # Median
print(np.std(arr))    # Standard Deviation
print(np.var(arr))    # Variance
print(np.sum(arr))    # Sum
print(np.min(arr))    # Minimum value
print(np.max(arr))    # Maximum value
```

---

## **4. Indexing and Slicing**
```python
arr = np.array([10, 20, 30, 40, 50])

print(arr[1])    # Access element at index 1 -> 20
print(arr[1:4])  # Slice elements from index 1 to 3 -> [20, 30, 40]
print(arr[:3])   # First three elements
print(arr[-1])   # Last element
```

### **Indexing in Multi-Dimensional Arrays**
```python
mat = np.array([[10, 20, 30], [40, 50, 60], [70, 80, 90]])

print(mat[1,2])  # Access row 1, column 2 -> 60
print(mat[0:2, 1:3])  # Slice first two rows and last two columns
print(mat[:,1])  # Select second column
```

---

## **5. Random Number Generation**
```python
np.random.seed(42)  # Set seed for reproducibility

print(np.random.rand(3,3))    # 3x3 matrix of random numbers (0 to 1)
print(np.random.randint(1, 100, (3,3)))  # 3x3 random integers from 1 to 100
print(np.random.randn(3,3))   # 3x3 matrix of normally distributed random numbers
```
---

## **Real-World Projects Using NumPy**
### **1. Analyzing Student Scores**
Load student scores and compute statistics.
```python
scores = np.random.randint(50, 100, (10, 5))  # 10 students, 5 subjects
print("Scores:\n", scores)
print("Mean Score:", np.mean(scores, axis=1)) # Mean per student
print("Highest Score:", np.max(scores, axis=1)) # Max per student
```

---

### **2. Stock Price Simulation (Monte Carlo)**
```python
np.random.seed(0)
days = 365
initial_price = 100
returns = np.random.normal(0, 1, days)
prices = initial_price * np.cumprod(1 + returns / 100)

import matplotlib.pyplot as plt
plt.plot(prices)
plt.title("Simulated Stock Prices")
plt.show()
```

---

### **3. Weather Data Analysis**
```python
temps = np.random.normal(30, 5, (365,))  # Yearly temperatures
print("Average Temperature:", np.mean(temps))
print("Hottest Day:", np.max(temps))
print("Coldest Day:", np.min(temps))
```

---