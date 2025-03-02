### **Pandas: A Comprehensive Guide**
Pandas is a powerful Python library for data analysis and manipulation. It provides data structures and functions designed to make working with structured data intuitive and efficient.

---

## **1. Installation**
To install pandas, use:
```bash
pip install pandas
```
Or for conda users:
```bash
conda install pandas
```

---

## **2. Core Data Structures**
Pandas has two primary data structures:

### **a. Series (1D Data)**
A one-dimensional labeled array that can hold any data type (integers, floats, strings, Python objects, etc.).

#### Creating a Series:
```python
import pandas as pd

data = [10, 20, 30, 40]
series = pd.Series(data, index=['a', 'b', 'c', 'd'])
print(series)
```

#### Accessing Elements:
```python
print(series['a'])  # Output: 10
print(series[0])    # Output: 10
```

---

### **b. DataFrame (2D Data)**
A two-dimensional labeled data structure, similar to a table or spreadsheet.

#### Creating a DataFrame:
```python
data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "Salary": [50000, 60000, 70000]
}
df = pd.DataFrame(data)
print(df)
```

#### Loading Data:
```python
df = pd.read_csv("data.csv")  # Load CSV file
df = pd.read_excel("data.xlsx")  # Load Excel file
df = pd.read_json("data.json")  # Load JSON file
```

#### Saving Data:
```python
df.to_csv("output.csv", index=False)
df.to_excel("output.xlsx", index=False)
df.to_json("output.json")
```

---

## **3. DataFrame Operations**
### **a. Basic Inspection**
```python
df.head()       # First 5 rows
df.tail()       # Last 5 rows
df.info()       # Summary of the DataFrame
df.describe()   # Statistical summary
df.shape        # Rows and columns count
df.columns      # List of column names
df.dtypes       # Data types of columns
```

### **b. Selecting Data**
#### **Column Selection**
```python
df["Name"]       # Single column as Series
df[["Name", "Age"]]  # Multiple columns as DataFrame
```

#### **Row Selection**
```python
df.iloc[0]       # First row (Index-based)
df.loc[1]        # Row by label/index
df.loc[df["Age"] > 30]  # Filtering rows
```

---

## **4. Data Manipulation**
### **a. Adding and Removing Columns**
```python
df["Bonus"] = df["Salary"] * 0.10  # Add new column
df.drop("Bonus", axis=1, inplace=True)  # Remove column
```

### **b. Adding and Removing Rows**
```python
df.loc[3] = ["David", 40, 80000]  # Add new row
df.drop(3, axis=0, inplace=True)  # Remove row
```

### **c. Sorting Data**
```python
df.sort_values("Age", ascending=False, inplace=True)  # Sort by Age descending
df.sort_values(["Salary", "Age"], ascending=[True, False])  # Sort by multiple columns
```

---

## **5. Handling Missing Data**
### **a. Checking for Missing Data**
```python
df.isnull().sum()  # Count of missing values in each column
```

### **b. Filling Missing Values**
```python
df.fillna(0, inplace=True)  # Replace NaN with 0
df.fillna(df.mean(), inplace=True)  # Replace NaN with column mean
```

### **c. Dropping Missing Values**
```python
df.dropna(inplace=True)  # Drop rows with NaN values
df.dropna(axis=1, inplace=True)  # Drop columns with NaN values
```

---

## **6. Grouping and Aggregation**
### **a. Grouping Data**
```python
df.groupby("Age").mean()  # Group by Age and compute mean
df.groupby("Age")["Salary"].sum()  # Sum Salary by Age
```

### **b. Aggregation Functions**
```python
df.agg({"Age": "max", "Salary": "sum"})  # Aggregate multiple functions
df.groupby("Age").agg({"Salary": ["mean", "sum"]})  # Multiple aggregations
```

---

## **7. Merging and Joining Data**
### **a. Concatenation**
```python
df1 = pd.DataFrame({"ID": [1, 2, 3], "Name": ["A", "B", "C"]})
df2 = pd.DataFrame({"ID": [4, 5, 6], "Name": ["D", "E", "F"]})

result = pd.concat([df1, df2], ignore_index=True)
```

### **b. Merging DataFrames**
```python
df1 = pd.DataFrame({"ID": [1, 2, 3], "Salary": [1000, 2000, 3000]})
df2 = pd.DataFrame({"ID": [1, 2, 4], "Bonus": [100, 200, 400]})

merged_df = df1.merge(df2, on="ID", how="inner")  # Inner join
merged_df = df1.merge(df2, on="ID", how="outer")  # Outer join
```

---

## **8. Pivot Tables & Reshaping**
### **a. Creating Pivot Tables**
```python
df.pivot_table(index="Name", columns="Age", values="Salary", aggfunc="sum")
```

### **b. Melting DataFrames**
```python
df.melt(id_vars=["Name"], value_vars=["Age", "Salary"], var_name="Metric", value_name="Value")
```

---

## **9. Time Series Analysis**
### **a. Working with Dates**
```python
df["Date"] = pd.to_datetime(df["Date"])  # Convert to datetime
df.set_index("Date", inplace=True)  # Set Date column as index
df.resample("M").sum()  # Resample data by month
```

---

## **10. Visualization with Pandas**
```python
import matplotlib.pyplot as plt

df["Salary"].plot(kind="bar")  # Bar chart
df.plot(x="Age", y="Salary", kind="line")  # Line chart
plt.show()
```

---

## **11. Advanced Pandas Features**
### **a. Applying Functions**
```python
df["Salary_After_Tax"] = df["Salary"].apply(lambda x: x * 0.8)  # Apply function
```

### **b. Working with Large Datasets**
```python
chunk_size = 10000
for chunk in pd.read_csv("large_data.csv", chunksize=chunk_size):
    process(chunk)  # Process each chunk separately
```

---

## **Conclusion**
Pandas is a powerful and flexible tool for data manipulation and analysis. It enables efficient handling of structured data, making it indispensable for data science, machine learning, and business analytics.

