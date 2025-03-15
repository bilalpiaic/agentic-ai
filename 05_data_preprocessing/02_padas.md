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

Here are **three interesting Pandas projects** with datasets and code that you can use to teach your students. Each project includes **data analysis, visualization, and insights**.

---

## 📌 **Project 1: IMDb Movie Data Analysis**
### **Objective:**  
Analyze IMDb movie data to find top-rated movies, most popular genres, and trends over the years.

### **Dataset:**  
[Download IMDb Movies Dataset](https://raw.githubusercontent.com/erikgregorywebb/datasets/master/imdb_top_1000.csv)

### **Code:**
```python
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
url = "https://raw.githubusercontent.com/erikgregorywebb/datasets/master/imdb_top_1000.csv"
df = pd.read_csv(url)

# Display first few rows
print(df.head())

# Convert 'Released_Year' column to numeric
df['Released_Year'] = pd.to_numeric(df['Released_Year'], errors='coerce')

# Top 10 highest-rated movies
top_movies = df[['Series_Title', 'IMDB_Rating']].sort_values(by='IMDB_Rating', ascending=False).head(10)
print("\nTop 10 Highest-Rated Movies:\n", top_movies)

# Count movies by genre
df['Genre'] = df['Genre'].apply(lambda x: x.split(',')[0])  # Take first genre if multiple
genre_counts = df['Genre'].value_counts()

# Plot genres
plt.figure(figsize=(10,5))
genre_counts.head(10).plot(kind='bar', color='skyblue')
plt.title("Top 10 Movie Genres in IMDb Dataset")
plt.xlabel("Genre")
plt.ylabel("Number of Movies")
plt.xticks(rotation=45)
plt.show()

# Trend of movies released over years
df.groupby('Released_Year').size().plot(kind='line', figsize=(10,5), color='red', marker='o')
plt.title("Movies Released Over the Years")
plt.xlabel("Year")
plt.ylabel("Number of Movies")
plt.grid()
plt.show()
```


---

## 📌 **Project 2: Stock Market Data Analysis**
### **Objective:**  
Analyze stock price data, calculate moving averages, and visualize stock trends.

### **Dataset:**  
[Download Apple Stock Data](https://query1.finance.yahoo.com/v7/finance/download/AAPL?period1=1609459200&period2=1640995200&interval=1d&events=history&includeAdjustedClose=true) (Apple Stock Prices for One Year)

### **Code:**
```python
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
url = "https://query1.finance.yahoo.com/v7/finance/download/AAPL?period1=1609459200&period2=1640995200&interval=1d&events=history&includeAdjustedClose=true"
df = pd.read_csv(url)

# Convert 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Set Date as index
df.set_index('Date', inplace=True)

# Plot closing price over time
plt.figure(figsize=(10,5))
plt.plot(df.index, df['Close'], label="Closing Price", color='blue')
plt.title("Apple Stock Prices")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid()
plt.show()

# Calculate moving average (50-day and 200-day)
df['50-day MA'] = df['Close'].rolling(window=50).mean()
df['200-day MA'] = df['Close'].rolling(window=200).mean()

# Plot Moving Averages
plt.figure(figsize=(10,5))
plt.plot(df.index, df['Close'], label="Closing Price", color='blue', alpha=0.5)
plt.plot(df.index, df['50-day MA'], label="50-Day Moving Average", color='red')
plt.plot(df.index, df['200-day MA'], label="200-Day Moving Average", color='green')
plt.title("Apple Stock Price with Moving Averages")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid()
plt.show()
```

---

## 📌 **Project 3: COVID-19 Data Analysis**
### **Objective:**  
Analyze COVID-19 cases, deaths, and trends across different countries.

### **Dataset:**  
[Download COVID-19 Data](https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv)

### **Code:**
```python
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
df = pd.read_csv(url)

# Select relevant columns
df = df[['location', 'date', 'total_cases', 'total_deaths', 'new_cases', 'new_deaths']]
df['date'] = pd.to_datetime(df['date'])

# Select data for a specific country
country = "United States"
df_country = df[df['location'] == country]

# Plot new cases over time
plt.figure(figsize=(10,5))
plt.plot(df_country['date'], df_country['new_cases'], label="New Cases", color='red', alpha=0.7)
plt.title(f"Daily New COVID-19 Cases in {country}")
plt.xlabel("Date")
plt.ylabel("Number of Cases")
plt.legend()
plt.grid()
plt.show()

# Calculate Case Fatality Rate (CFR)
df_country['CFR'] = (df_country['total_deaths'] / df_country['total_cases']) * 100

# Plot Case Fatality Rate over time
plt.figure(figsize=(10,5))
plt.plot(df_country['date'], df_country['CFR'], label="Case Fatality Rate (%)", color='purple')
plt.title(f"COVID-19 Case Fatality Rate in {country}")
plt.xlabel("Date")
plt.ylabel("Fatality Rate (%)")
plt.legend()
plt.grid()
plt.show()
```