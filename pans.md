# Pandas 101 — Beginner to Intermediate

A practical teaching resource for learning **Pandas in Python**, from the fundamentals of DataFrames and data selection to filtering, cleaning, analysis, CRUD-style operations, and exporting data.

---

## About This Repository

This repository contains materials for teaching and practicing **Pandas**, one of the core Python tools used for working with structured data.

The lesson is designed for **beginner to early-intermediate Python students**. The focus is not simply on memorizing Pandas functions, but on learning how to use Pandas to answer questions about real-world data.

The overall learning flow is:

```text
Data
  ↓
DataFrame
  ↓
Explore
  ↓
Select
  ↓
Filter
  ↓
Modify
  ↓
Clean
  ↓
Analyze
  ↓
Save
```

---

## Learning Objectives

By the end of this lesson, students should be able to:

* Explain what Pandas is and why it is useful.
* Understand the difference between a **Series** and a **DataFrame**.
* Create a DataFrame.
* Load data from CSV and Excel files.
* Inspect and understand a dataset.
* Select rows and columns.
* Use `loc` and `iloc`.
* Filter data using Boolean conditions.
* Combine multiple conditions using `&`, `|`, and `~`.
* Use `isin()` for membership filtering.
* Perform basic string operations.
* Perform CRUD-style operations on a DataFrame.
* Identify and handle missing values.
* Rename columns and convert data types.
* Group, count, aggregate, and sort data.
* Export processed data to CSV or Excel.

---

## Prerequisites

Students should have basic knowledge of:

* Python syntax
* Variables
* Lists
* Dictionaries
* Basic operators
* Functions
* Working with Jupyter Notebook or another Python environment

---

## What Is Pandas?

**Pandas** is a Python library used for **data manipulation and analysis**.

It is especially useful when working with structured data such as:

* CSV files
* Excel spreadsheets
* SQL tables
* JSON data
* API responses

The two main Pandas data structures are:

### Series

A **one-dimensional labeled data structure**.

It can be thought of as similar to a single column.

```python
df["Price"]
```

### DataFrame

A **two-dimensional labeled data structure consisting of rows and columns**.

It can be thought of as a programmable table or spreadsheet.

---

## Dataset Used in This Lesson

The practical examples use an **orders dataset** containing information such as:

| Column         | Description                        |
| -------------- | ---------------------------------- |
| `OrderID`      | Unique order identifier            |
| `CustomerName` | Customer who placed the order      |
| `Product`      | Product ordered                    |
| `Category`     | Product category                   |
| `Quantity`     | Number of items ordered            |
| `Price`        | Product price                      |
| `OrderDate`    | Date of the order                  |
| `Shipped`      | Whether the order has been shipped |
| `Country`      | Customer's country                 |

The teaching material uses this dataset to demonstrate DataFrame exploration and filtering.

---

## Getting Started

### Import Pandas

```python
import pandas as pd
```

The `pd` name is the conventional alias used for Pandas.

### Load the dataset

```python
df = pd.read_csv("orders.csv")
```

You can also load Excel files:

```python
df = pd.read_excel("data.xlsx")
```

---

# Lesson Structure

## 1. Introduction to Pandas

Students learn:

* What Pandas is
* Why Pandas is useful
* What structured data is
* What a dataset is
* What a DataFrame is
* What a Series is

---

## 2. DataFrames

Students learn how to create a DataFrame:

```python
data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "Country": ["USA", "Canada", "UK"]
}

df = pd.DataFrame(data)
```

---

## 3. Exploring Data

Before manipulating data, students learn to inspect it.

```python
df.head()
df.tail()
df.info()
df.describe()
df.columns
df.index
```

Important terminology:

* **Row** — one record or observation.
* **Column** — one attribute or field.
* **Index** — the label used to identify rows.
* **Data type** — the kind of value stored in a column.
* **Descriptive statistics** — numerical summaries of data.

The supplied lesson demonstrates `head()`, `columns`, and DataFrame inspection using the orders dataset.

---

## 4. Selecting Data

### Select one column

```python
df["Price"]
```

### Select multiple columns

```python
df[["Product", "Price"]]
```

### Select by position

```python
df.iloc[0]
```

### Select by label

```python
df.loc[0]
```

### Key terminology

**`iloc`**
Position-based selection.

**`loc`**
Label-based selection.

---

## 5. Filtering Data

Filtering means selecting rows that satisfy a condition.

```python
df[df["Price"] > 100]
```

### Boolean values

A Boolean value is either:

```text
True
False
```

### Boolean mask

A Boolean mask is a sequence of `True` and `False` values used to determine which rows should be selected.

---

## 6. Comparison Operators

| Operator | Meaning                  |
| -------- | ------------------------ |
| `>`      | Greater than             |
| `<`      | Less than                |
| `>=`     | Greater than or equal to |
| `<=`     | Less than or equal to    |
| `==`     | Equal to                 |
| `!=`     | Not equal to             |

Remember:

```python
=
```

means assignment, while:

```python
==
```

means comparison.

---

## 7. Multiple Conditions

### AND

```python
df[
    (df["Category"] == "Electronics") &
    (df["Country"] == "USA")
]
```

Both conditions must be true.

### OR

```python
df[
    (df["Category"] == "Electronics") |
    (df["Country"] == "USA")
]
```

At least one condition must be true.

### NOT

```python
df[~df["Country"].isin(["USA"])]
```

Reverses the condition.

These Boolean filtering patterns are demonstrated in the supplied notebook.

---

## 8. Membership Filtering with `isin()`

```python
df[df["Country"].isin(["USA", "UK"])]
```

`isin()` checks whether a value belongs to a specified collection of values.

This is useful when filtering for multiple possible values.

---

## 9. String Operations

Example:

```python
df[df["Name"].str.startswith("A")]
```

Important terminology:

### String

A sequence of characters.

Examples:

```text
"Alice"
"Laptop"
"USA"
```

### `.str`

Pandas' interface for applying string operations.

### `startswith()`

Checks whether a string begins with a specified value.

---

# CRUD Operations

CRUD is a general term describing four basic operations:

```text
C → Create
R → Read
U → Update
D → Delete
```

## Create

Add new data:

```python
new_row = pd.DataFrame([
    {
        "Name": "Diana",
        "Age": 28,
        "Country": "Germany"
    }
])

df = pd.concat(
    [df, new_row],
    ignore_index=True
)
```

### Concatenation

Combining objects together.

---

## Read

Retrieve information:

```python
df.loc[df["Name"] == "Alice"]
```

or:

```python
df.iloc[2]
```

---

## Update

Modify existing values:

```python
df.loc[df["Name"] == "Bob", "Age"] = 31
```

Another example:

```python
df["Country"] = df["Country"].str.upper()
```

The lesson material also demonstrates conditional updates and converting country values to uppercase.

---

## Delete

Delete a row:

```python
df = df.drop(2, axis=0)
```

Delete a column:

```python
df = df.drop("Age", axis=1)
```

Delete rows based on a condition:

```python
df = df[df["Name"] != "Alice"]
```

---

# Data Cleaning

Real-world datasets may contain problems such as:

* Missing values
* Incorrect data types
* Inconsistent text
* Incorrect labels
* Unwanted columns

## Missing values

Check for missing values:

```python
df.isnull()
```

Count missing values:

```python
df.isnull().sum()
```

## Remove missing values

```python
df.dropna()
```

## Replace missing values

```python
df.fillna({"Age": 0})
```

In simple terms:

```text
dropna() → remove missing data
fillna() → replace missing data
```

---

## Rename Columns

```python
df.rename(
    columns={"Age": "Years"}
)
```

The lesson also demonstrates renaming `OrderID` to `Order ID`.

---

## Convert Data Types

```python
df["Years"] = df["Years"].astype(float)
```

Common types include:

```text
integer
float
string
boolean
```

---

# Data Analysis

Once data has been cleaned and prepared, students can begin extracting information from it.

## Count Values

```python
df["Country"].value_counts()
```

This counts how frequently each unique value appears.

---

## Group Data

```python
df.groupby("Category")["Price"].mean()
```

### Grouping

Dividing data into groups based on a column or rule.

### Aggregation

Producing a summary value from multiple values.

Common aggregation operations include:

```python
sum()
mean()
count()
min()
max()
```

Example:

```python
df["Price"].sum()
df["Price"].mean()
df["Price"].max()
df["Price"].min()
```

---

# Sorting

```python
df.sort_values(
    by="Price",
    ascending=False
)
```

### `ascending=True`

Smallest to largest.

### `ascending=False`

Largest to smallest.

---

# Exporting Data

Processed data can be saved for later use.

### CSV

```python
df.to_csv("processed_orders.csv", index=False)
```

### Excel

```python
df.to_excel("processed_orders.xlsx", index=False)
```

### Export

Saving or transferring processed data into a file or another system.

### `index=False`

Prevents the DataFrame index from being written as an additional column.

---

# Core Pandas Terminology

| Term                | Definition                                        |
| ------------------- | ------------------------------------------------- |
| **Pandas**          | Python library for data manipulation and analysis |
| **Library**         | Collection of reusable code                       |
| **Dataset**         | Collection of related data                        |
| **Structured Data** | Data arranged in a consistent structure           |
| **Series**          | One-dimensional labeled data                      |
| **DataFrame**       | Two-dimensional labeled data                      |
| **Row**             | One record or observation                         |
| **Column**          | One attribute or field                            |
| **Index**           | Label used to identify rows                       |
| **Boolean**         | `True` or `False` value                           |
| **Boolean Mask**    | Boolean conditions used to select rows            |
| **Filter**          | Select rows based on a condition                  |
| **String**          | Sequence of characters                            |
| **CRUD**            | Create, Read, Update, Delete                      |
| **Concatenation**   | Combining objects                                 |
| **Missing Value**   | Data that is absent                               |
| **Grouping**        | Dividing data into groups                         |
| **Aggregation**     | Producing a summary from values                   |
| **Sorting**         | Arranging data in an order                        |
| **Export**          | Saving data to a file or another system           |

---

# Recommended Teaching Flow

The recommended demonstration order is:

```text
1. Import Pandas
        ↓
2. Load Dataset
        ↓
3. Explore Dataset
        ↓
4. Select Columns
        ↓
5. Select Rows
        ↓
6. Filter Rows
        ↓
7. Combine Conditions
        ↓
8. Modify Data
        ↓
9. Clean Data
        ↓
10. Analyze Data
        ↓
11. Sort Data
        ↓
12. Export Data
```

This allows students to see a complete data-analysis workflow rather than disconnected Pandas commands.

---

# Practical Exercise

Using `orders.csv`, complete the following:

1. Load the dataset.
2. Display the first five rows.
3. Display all column names.
4. Display `CustomerName`, `Product`, and `Price`.
5. Find all orders where `Price > 100`.
6. Find all Electronics orders that have been shipped.
7. Find all orders from Japan.
8. Count the number of orders from each country.
9. Sort orders from highest price to lowest price.
10. Save the result as `processed_orders.csv`.

---

# Challenge

Imagine you are a data analyst working for an online store.

Use the dataset to determine:

* The most expensive order.
* The cheapest order.
* The total quantity ordered.
* The number of Electronics orders.
* The number of Furniture orders.
* The number of Stationery orders.
* The countries represented in the dataset.
* The number of orders that have not been shipped.
* The average price for each category.
* All orders where the quantity is greater than 5.

The goal is not merely to produce an answer, but to determine **which Pandas operation is appropriate for each question**.

---

# Quick Reference

```python
import pandas as pd

# Load
df = pd.read_csv("orders.csv")

# Explore
df.head()
df.tail()
df.info()
df.describe()
df.columns
df.index

# Select
df["Price"]
df[["Product", "Price"]]

# Rows
df.iloc[0]
df.loc[0]

# Filter
df[df["Price"] > 100]

# Multiple conditions
df[
    (df["Category"] == "Electronics") &
    (df["Country"] == "USA")
]

# Membership
df[df["Country"].isin(["USA", "UK"])]

# NOT
df[~df["Country"].isin(["USA"])]

# Update
df.loc[
    df["Country"] == "USA",
    "Country"
] = "United States"

# Strings
df["Country"] = df["Country"].str.upper()

# Missing values
df.isnull().sum()
df.dropna()
df.fillna(0)

# Rename
df.rename(columns={"Age": "Years"})

# Type conversion
df["Years"].astype(float)

# Analysis
df["Country"].value_counts()
df.groupby("Category")["Price"].mean()

# Sorting
df.sort_values(
    by="Price",
    ascending=False
)

# Save
df.to_csv("processed.csv", index=False)
df.to_excel("processed.xlsx", index=False)
```

---

# Teaching Philosophy

The central principle of this lesson is:

> **Do not teach Pandas as a list of functions to memorize. Teach students how to use Pandas to answer questions about data.**

For example:

```text
Question
   ↓
What information do we need?
   ↓
Which rows/columns matter?
   ↓
Do we need a condition?
   ↓
Which Pandas operation solves it?
   ↓
Result
```

The ultimate objective is to help students develop the ability to think about data, not simply reproduce code.
