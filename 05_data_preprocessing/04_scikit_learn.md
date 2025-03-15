## **Scikit-Learn: Comprehensive Guide**

### **1. Introduction to Scikit-Learn**
Scikit-Learn is a powerful open-source Python library for **machine learning**. It provides simple and efficient tools for data mining, preprocessing, model selection, and evaluation.

### **2. Installation**
```bash
pip install scikit-learn
```
Or inside a Jupyter Notebook:
```python
!pip install scikit-learn
```

### **3. Core Modules**
Scikit-learn provides:
- **Supervised Learning**: Linear Regression, Decision Trees, SVM, Random Forests
- **Unsupervised Learning**: K-Means, PCA, DBSCAN
- **Model Evaluation**: Train-Test Split, Cross-Validation, GridSearchCV
- **Data Preprocessing**: Scaling, Encoding, Imputation

---

### **4. Getting Started with Scikit-Learn**
#### **4.1 Dataset Handling**
Scikit-learn provides built-in datasets for quick learning.
```python
from sklearn import datasets

iris = datasets.load_iris()
X, y = iris.data, iris.target
print(X.shape, y.shape)
```

#### **4.2 Data Preprocessing**
- **Scaling Data**
```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
```
- **One-Hot Encoding for Categorical Variables**
```python
from sklearn.preprocessing import OneHotEncoder

encoder = OneHotEncoder()
encoded_data = encoder.fit_transform(y.reshape(-1, 1))
```

#### **4.3 Splitting Data for Training & Testing**
```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

#### **4.4 Training a Model**
- **Using Logistic Regression**
```python
from sklearn.linear_model import LogisticRegression

model = LogisticRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
```

#### **4.5 Evaluating a Model**
```python
from sklearn.metrics import accuracy_score, classification_report

print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))
```

---

## **5. Advanced Topics**
### **5.1 Hyperparameter Tuning using GridSearchCV**
```python
from sklearn.model_selection import GridSearchCV

params = {'C': [0.1, 1, 10]}
grid_search = GridSearchCV(LogisticRegression(), params, cv=5)
grid_search.fit(X_train, y_train)

print("Best Parameters:", grid_search.best_params_)
```

### **5.2 Feature Selection using PCA**
```python
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)
```

### **5.3 Model Pipelines**
```python
from sklearn.pipeline import Pipeline

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', LogisticRegression())
])

pipeline.fit(X_train, y_train)
print("Pipeline Accuracy:", pipeline.score(X_test, y_test))
```

---

# **Projects**
### **Project 1: Handwritten Digit Recognition (Using MNIST & SVM)**
**Objective**: Train an SVM model to recognize digits from the MNIST dataset.

#### **Steps**
1. Load the MNIST dataset
2. Scale the data
3. Split into train & test sets
4. Train an **SVM (Support Vector Machine)**
5. Evaluate accuracy

```python
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# Load dataset
digits = datasets.load_digits()
X, y = digits.data, digits.target

# Scale & split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train SVM model
svm_model = SVC(kernel='rbf', C=10)
svm_model.fit(X_train, y_train)

# Predictions & Evaluation
y_pred = svm_model.predict(X_test)
print("Digit Recognition Accuracy:", accuracy_score(y_test, y_pred))
```

---

### **Project 2: Spam Email Classifier (Naive Bayes & TF-IDF)**
**Objective**: Build a **spam email classifier** using the Naive Bayes algorithm.

#### **Steps**
1. Load dataset (can use a sample dataset of spam emails)
2. Preprocess the text (Tokenization, TF-IDF transformation)
3. Train a **Naive Bayes Classifier**
4. Evaluate accuracy

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# Sample dataset
emails = [
    "Win a $1000 gift card now!", "Congratulations! You won a lottery!",
    "Meeting scheduled for 2PM tomorrow", "Project update required ASAP"
]
labels = [1, 1, 0, 0]  # 1 = Spam, 0 = Not Spam

# Pipeline for Text Classification
model = make_pipeline(TfidfVectorizer(), MultinomialNB())
model.fit(emails, labels)

# Test new email
new_email = ["Claim your free vacation now!"]
print("Prediction:", model.predict(new_email))  # 1 = Spam, 0 = Not Spam
```

---

### **Project 3: Customer Segmentation using K-Means**
**Objective**: Use **K-Means clustering** to group customers based on their purchasing behavior.

#### **Steps**
1. Load sample **customer data** (Age, Income, Spending Score)
2. Normalize the data
3. Apply **K-Means clustering**
4. Visualize the clusters

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Sample Customer Data (Age, Income, Spending Score)
X = np.array([[25, 40000, 60], [40, 80000, 80], [22, 30000, 50],
              [35, 60000, 70], [60, 100000, 90]])

# Scale Data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply K-Means Clustering
kmeans = KMeans(n_clusters=2, random_state=42)
clusters = kmeans.fit_predict(X_scaled)

# Plot Clusters
plt.scatter(X[:, 0], X[:, 1], c=clusters, cmap='viridis')
plt.xlabel("Age")
plt.ylabel("Income")
plt.title("Customer Segmentation using K-Means")
plt.show()
```

---
