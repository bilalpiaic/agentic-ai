import pandas as pd
data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "Salary": [50000, 60000, 70000]
}
df = pd.DataFrame(data)

def calculate_tax(salary):
    print(salary)
    if salary < 60000:
        return salary * 0.9
    elif salary < 70000:
        return salary * 0.85
    else:
        return salary * 0.8

df["Salary_After_Tax"] = df["Salary"].apply(calculate_tax)
print(df)


chunk_size = 100
for chunk in pd.read_csv("imdb-top-1000.csv", chunksize=chunk_size):
    print(chunk)
    # Do something with the chunk