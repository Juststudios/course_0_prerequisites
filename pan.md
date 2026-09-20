# PANDAS 101 — INSTRUCTOR TEACHING GUIDE

## 1. Lesson Overview

**Topic:** Pandas — Beginner to Intermediate
**Level:** Beginner / early intermediate Python students
**Main goal:** By the end of the lesson, students should be able to load, inspect, select, filter, modify, clean, analyze, and save tabular data using Pandas.

The class should not feel like a list of commands to memorize. Teach Pandas as a tool for answering questions about data.

A useful teaching sequence is:

**Data → DataFrame → Explore → Select → Filter → Modify → Clean → Analyze → Save**

---

# 2. Opening the Class

## What to say

> "Today we are going to learn Pandas. Pandas allows us to work with structured data in Python in a way that is much easier than manually processing every value."

> "Imagine someone gives you an Excel file containing 1,000 customer orders and asks: Which products were sold? Which countries have the most orders? Which orders have not been shipped? Pandas helps us answer those questions programmatically."

Then introduce the dataset.

Our example contains information such as:

* Order ID
* Customer name
* Product
* Category
* Quantity
* Price
* Order date
* Shipping status
* Country

The resource's example dataset uses these same columns.

---

# 3. Essential Terminology

This is the vocabulary you should repeatedly use during the class.

## Pandas

**Definition:**
Pandas is a Python library used for data manipulation and analysis.

**Say to students:**

> "Pandas gives Python specialized tools for working with structured data."

---

## Library

**Definition:**
A collection of pre-written code that programmers can use instead of building everything from scratch.

**Example:**

```python
import pandas as pd
```

**Explain:**

> "`import` means we are bringing a library into our Python program."

---

## Module

**Definition:**
A Python file or component containing reusable code.

You do not need to spend much time here, but students will hear the term frequently.

---

## Data

**Definition:**
Information represented in a form that can be stored, processed, and analyzed.

Examples:

```text
John
25
Ghana
1200
2024-06-01
```

---

## Dataset

**Definition:**
A collection of related data.

For this class, the orders CSV file is a dataset.

**Say:**

> "Our dataset is the collection of all the customer order records."

---

## Structured Data

**Definition:**
Data organized according to a consistent structure, usually rows and columns.

**Example:**

| Name  | Age | Country |
| ----- | --: | ------- |
| Alice |  25 | USA     |
| Bob   |  30 | Canada  |

This is why spreadsheets and SQL tables are good examples of structured data.

---

# 4. Series and DataFrame

These are two of the most important terms in Pandas.

## Series

**Definition:**
A one-dimensional labeled data structure.

Think of it as approximately one column of a table.

Example:

```python
df["Age"]
```

You can say:

> "A Series is like a single column with labels."

---

## DataFrame

**Definition:**
A two-dimensional labeled data structure consisting of rows and columns.

Think of it as a programmable table or spreadsheet.

Your resource introduces the DataFrame as the main tabular structure and demonstrates it with columns such as `OrderID`, `CustomerName`, `Product`, and `Category`.

**Say:**

> "A DataFrame is the main object we will work with today."

---

# 5. Rows, Columns and Index

Students must understand these three terms before filtering.

## Column

**Definition:**
A vertical collection of values representing one attribute or field.

Example:

```text
CustomerName
```

## Row

**Definition:**
A horizontal record containing information about one observation or entry.

For example, one customer's order is one row.

## Index

**Definition:**
The label used by Pandas to identify rows.

Example:

```text
0
1
2
3
4
```

Point out that the index is not necessarily the same thing as a business identifier such as `OrderID`.

This distinction becomes important when teaching:

```python
df.iloc[0]
```

and

```python
df.loc[0]
```

---

# 6. Importing Pandas

## Code

```python
import pandas as pd
```

## Terminology

**Alias:**
A shorter alternative name.

Here:

```python
pd
```

is an alias for:

```python
pandas
```

**Say:**

> "We usually import Pandas as `pd` because it is the conventional shorthand."

---

# 7. Creating a DataFrame

Use a small example before moving to the large orders dataset.

```python
data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "Country": ["USA", "Canada", "UK"]
}

df = pd.DataFrame(data)

print(df)
```

## Teaching point

Explain the relationship:

```text
Dictionary
    ↓
Columns
    ↓
DataFrame
```

The important idea is that Pandas converts structured information into a DataFrame that we can manipulate programmatically.

---

# 8. Loading Real Data

Now move to the actual dataset.

## CSV

```python
df = pd.read_csv("orders.csv")
```

## Excel

```python
df = pd.read_excel("data.xlsx")
```

## Terminology

### CSV

**Definition:**
Comma-Separated Values.

It is a plain-text file format commonly used to store tabular data.

### File path

**Definition:**
The location used to identify a file on a computer.

---

## What to say

> "Instead of manually creating our table, we can tell Pandas to read an existing data file."

Your supplied notebook demonstrates loading the orders dataset using `pd.read_csv("orders.csv")`.

---

# 9. Exploring the DataFrame

Before manipulating data, teach students to inspect it.

## `head()`

```python
df.head()
```

**Definition:**
Displays the first five rows by default.

**Teaching phrase:**

> "Before analyzing data, we need to look at what we actually have."

The supplied material demonstrates `df.head()` on the orders table.

---

## `tail()`

```python
df.tail()
```

**Definition:**
Displays the final five rows by default.

---

## `info()`

```python
df.info()
```

**Definition:**
Provides structural information about the DataFrame, including columns, data types, and non-null information.

**Teaching phrase:**

> "`info()` helps us understand the structure of our data."

---

## `describe()`

```python
df.describe()
```

**Definition:**
Produces descriptive statistics for applicable numeric columns.

Use the phrase:

> "Descriptive statistics summarize the numerical data."

---

## `columns`

```python
df.columns
```

**Definition:**
Returns the column labels.

The notebook shows the orders DataFrame containing columns such as `OrderID`, `CustomerName`, `Product`, `Category`, `Quantity`, `Price`, `OrderDate`, `Shipped`, and `Country`.

---

## `index`

```python
df.index
```

**Definition:**
Provides the row labels/index information.

---

# 10. Selecting Data

Now teach students how to retrieve specific information.

## Selecting one column

```python
df["Age"]
```

Explain:

> "We are selecting one column, so the result is a Series."

---

## Selecting multiple columns

```python
df[["Name", "Age"]]
```

Explain why there are **two sets of brackets**.

The inner brackets contain a Python list of column names.

---

# 11. Position-Based and Label-Based Selection

This is an important distinction.

## `iloc`

```python
df.iloc[0]
```

**Definition:**
Integer-location based selection.

In simple words:

> "`iloc` selects using position."

So:

```python
df.iloc[0]
```

means the first row by position.

---

## `loc`

```python
df.loc[0]
```

**Definition:**
Label-based selection.

In simple words:

> "`loc` selects using labels."

The supplied examples use both `iloc` and `loc` for row access.

---

# 12. Filtering Data

This should be one of the major teaching sections.

## Concept

**Filtering:**
Selecting only the rows that satisfy a condition.

Start with:

```python
df[df["Age"] > 30]
```

Say:

> "We are asking Pandas to keep only the rows where Age is greater than 30."

---

# 13. Boolean Conditions

## Boolean

**Definition:**
A value representing one of two logical states:

```text
True
False
```

For example:

```python
df["Age"] > 30
```

produces a Boolean result for each row.

---

## Boolean Mask

**Definition:**
A sequence of Boolean values used to select rows that meet a condition.

Explain it visually:

```text
Age > 30

True
False
True
False
True
```

Pandas uses this pattern to decide which rows to keep.

---

# 14. Comparison Operators

Teach these explicitly.

| Operator | Meaning                  |
| -------- | ------------------------ |
| `>`      | greater than             |
| `<`      | less than                |
| `>=`     | greater than or equal to |
| `<=`     | less than or equal to    |
| `==`     | equal to                 |
| `!=`     | not equal to             |

Make sure students understand:

```python
==
```

is comparison, while

```python
=
```

is assignment.

---

# 15. Multiple Conditions

## AND

```python
df[(df["Category"] == "Electronics") &
   (df["Country"] == "USA")]
```

**Definition — AND:**
Both conditions must be true.

The supplied notebook uses this exact pattern.

Say:

> "The customer must satisfy condition one AND condition two."

---

## OR

```python
df[(df["Category"] == "Electronics") |
   (df["Country"] == "USA")]
```

**Definition — OR:**
At least one condition must be true.

This pattern also appears in the supplied notebook.

---

## NOT

```python
~df["Country"].isin(["USA", "Sweden", "Brazil"])
```

**Definition — NOT:**
Reverses a Boolean condition.

The supplied notebook demonstrates this form of exclusion filtering.

---

# 16. `isin()`

```python
df[df["Country"].isin(["USA", "UK"])]
```

**Definition:**
Checks whether values belong to a specified collection of values.

Say:

> "Instead of writing a long OR condition, `isin()` allows us to test membership in a list of values."

---

# 17. String Filtering

Example:

```python
df[df["Name"].str.startswith("A")]
```

## Terminology

### String

A sequence of characters.

Examples:

```text
"Alice"
"USA"
"Laptop"
```

### `.str`

The Pandas string-accessor interface used for string operations.

### `startswith()`

Checks whether a string begins with a particular value.

---

# 18. CRUD in Pandas

Introduce CRUD carefully.

**CRUD means:**

```text
C = Create
R = Read
U = Update
D = Delete
```

Explain:

> "CRUD is a general term used to describe the four basic operations performed on data."

In this lesson, we are using CRUD as a way to organize common DataFrame operations.

---

# 19. CREATE

## Adding a row

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

## Terminology

### Concatenation

**Definition:**
Combining objects together.

### `ignore_index=True`

Tells Pandas to create a fresh sequential index for the resulting DataFrame.

---

# 20. READ

Examples:

```python
df.loc[df["Name"] == "Alice"]
```

and

```python
df.iloc[2]
```

Explain:

> "READ means retrieving information without changing it."

---

# 21. UPDATE

Example:

```python
df.loc[df["Name"] == "Bob", "Age"] = 31
```

Explain this carefully:

```text
df.loc[
    rows,
    column
]
```

We are saying:

> "Find Bob's row, then update the Age column."

Another example:

```python
df["Country"] = df["Country"].str.upper()
```

This changes all values in the Country column to uppercase.

The supplied notebook also demonstrates conditional country updates and string conversion to uppercase.

---

# 22. DELETE

## Delete a row

```python
df = df.drop(2, axis=0)
```

## Delete a column

```python
df = df.drop("Age", axis=1)
```

## Delete based on a condition

```python
df = df[df["Name"] != "Alice"]
```

---

# 23. `axis`

This is a terminology students often struggle with.

**`axis=0`**

Refers to the row axis.

**`axis=1`**

Refers to the column axis.

A simple classroom explanation:

> "`axis=0` means operate down the rows, while `axis=1` means operate across the columns."

Do not spend too long on the abstract meaning. Demonstrate it visually.

---

# 24. Data Cleaning

Introduce this with a practical problem.

Say:

> "Real-world data is rarely perfect."

Common problems include:

* Missing values
* Incorrect data types
* Inconsistent text
* Unwanted columns
* Incorrect labels

---

# 25. Missing Values

## Definition

A **missing value** is data that is absent or unavailable for a particular entry.

## Detecting missing values

```python
df.isnull()
```

This returns Boolean information indicating missing entries.

To count them:

```python
df.isnull().sum()
```

Explain:

> "`isnull()` asks which values are missing."

---

# 26. `dropna()`

```python
df.dropna(inplace=True)
```

**Definition:**
Removes rows or columns containing missing values according to the operation's configuration.

### `inplace`

**Definition:**
A parameter that tells the method whether to modify the existing object directly rather than returning a separately assigned result.

Say:

> "`inplace=True` means apply the change to the existing DataFrame."

---

# 27. `fillna()`

```python
df.fillna({"Age": 0}, inplace=True)
```

**Definition:**
Replaces missing values with a specified value.

Explain the difference:

```text
dropna → remove missing data
fillna → replace missing data
```

---

# 28. Renaming Columns

```python
df.rename(
    columns={"Age": "Years"},
    inplace=True
)
```

**Definition:**
Changes column labels.

The source also demonstrates renaming `OrderID` to `Order ID`.

---

# 29. Data Types

## Definition

A **data type** determines the kind of value stored.

Examples:

```text
integer → 10
float   → 10.5
string  → "Alice"
boolean → True
```

## `astype()`

```python
df["Years"] = df["Years"].astype(float)
```

**Definition:**
Converts values to a specified data type when the conversion is valid.

---

# 30. Data Analysis

Now transition from manipulation to answering questions.

Say:

> "Cleaning and filtering data are useful, but the real goal is usually to learn something from the data."

---

# 31. `value_counts()`

```python
df["Country"].value_counts()
```

**Definition:**
Counts how many times each unique value appears.

Teaching question:

> "Which country appears most often in our data?"

---

# 32. Grouping

```python
df.groupby("Country")["Age"].mean()
```

## Grouping

**Definition:**
Dividing data into groups based on a specific column or rule.

Explain:

```text
Country
   ↓
Group rows by country
   ↓
Calculate the average Age for each group
```

---

# 33. Aggregation

**Definition:**
Combining multiple values into a summary value such as:

```text
sum
mean
count
min
max
```

Examples:

```python
df["Price"].sum()
df["Price"].mean()
df["Price"].max()
df["Price"].min()
```

This terminology will prepare students for more advanced Pandas.

---

# 34. Sorting

```python
df.sort_values(
    by="Age",
    ascending=False
)
```

## Sorting

**Definition:**
Arranging data according to a specified order.

### `ascending=True`

Smallest to largest.

### `ascending=False`

Largest to smallest.

---

# 35. Saving the Result

## CSV

```python
df.to_csv("cleaned_data.csv", index=False)
```

## Excel

```python
df.to_excel("output.xlsx", index=False)
```

## Terminology

### Export

Moving processed data from the program into a file or another system.

### `index=False`

Prevents Pandas from writing the DataFrame index as an additional column.

---

# 36. The Main Pandas Vocabulary Students Should Know

At the end of the lesson, students should recognize these terms:

| Term            | Simple meaning                                    |
| --------------- | ------------------------------------------------- |
| Pandas          | Python library for data manipulation and analysis |
| Library         | Reusable collection of code                       |
| Dataset         | Collection of related data                        |
| Structured data | Data arranged in a consistent structure           |
| Series          | One-dimensional labeled data                      |
| DataFrame       | Two-dimensional labeled table                     |
| Row             | One record/observation                            |
| Column          | One attribute/field                               |
| Index           | Row labels                                        |
| Data type       | Kind of value stored                              |
| Boolean         | `True` or `False`                                 |
| Boolean mask    | Boolean conditions used to select rows            |
| Filter          | Select rows matching a condition                  |
| `loc`           | Label-based selection                             |
| `iloc`          | Position-based selection                          |
| String          | Sequence of characters                            |
| Concatenate     | Combine objects                                   |
| CRUD            | Create, Read, Update, Delete                      |
| Missing value   | Data that is absent                               |
| Clean           | Correct or prepare data                           |
| Grouping        | Divide data into groups                           |
| Aggregation     | Produce a summary from values                     |
| Sort            | Arrange data in order                             |
| Export          | Save data to another format/file                  |

---

# 37. Recommended Demonstration Sequence

Do not immediately give students every command.

Use this progression on the projector:

### Stage 1 — Load

```python
import pandas as pd

df = pd.read_csv("orders.csv")
```

Ask:

> "What do you think `df` contains?"

---

### Stage 2 — Look

```python
df.head()
df.info()
df.columns
```

Ask:

> "What information can we learn about the dataset without changing anything?"

---

### Stage 3 — Select

```python
df["Product"]
```

Then:

```python
df[["Product", "Price"]]
```

---

### Stage 4 — Filter

```python
df[df["Price"] > 100]
```

Then:

```python
df[
    (df["Category"] == "Electronics") &
    (df["Shipped"] == "Yes")
]
```

---

### Stage 5 — Modify

```python
df.loc[df["Country"] == "USA", "Country"] = "United States"
```

---

### Stage 6 — Analyze

```python
df["Country"].value_counts()
```

Then:

```python
df.groupby("Category")["Price"].mean()
```

---

### Stage 7 — Save

```python
df.to_csv("processed_orders.csv", index=False)
```

At this point students have experienced the complete data workflow.

---

# 38. Questions to Ask While Teaching

Do not wait until the end to test students.

Ask questions such as:

**After DataFrame introduction:**

> "What is the difference between a Series and a DataFrame?"

**After indexing:**

> "What is the difference between `loc` and `iloc`?"

**After filtering:**

> "Why are we using `==` here instead of `=`?"

**After Boolean filtering:**

> "What does `&` mean?"

**After `isin()`:**

> "How could we select records from three countries?"

**After cleaning:**

> "What is the difference between `dropna()` and `fillna()`?"

**After grouping:**

> "Why would a data analyst group data?"

---

# 39. Mini Practical Exercise

Give students the orders dataset and tell them:

### Task 1

Load the dataset.

```python
import pandas as pd

df = pd.read_csv("orders.csv")
```

### Task 2

Display the first five records.

### Task 3

Display the names of all columns.

### Task 4

Display only:

```text
CustomerName
Product
Price
```

### Task 5

Find all orders where:

```text
Price > 100
```

### Task 6

Find all Electronics orders that have been shipped.

### Task 7

Find all orders from Japan.

### Task 8

Count how many orders came from each country.

### Task 9

Sort orders from highest price to lowest price.

### Task 10

Save the processed dataset as:

```text
processed_orders.csv
```

---

# 40. Challenge Exercise

Give students the following problem:

> "You work for an online store. The manager wants a quick report from the orders dataset."

Ask them to find:

1. The most expensive order.
2. The cheapest order.
3. The total quantity ordered.
4. The number of Electronics orders.
5. The number of Furniture orders.
6. The number of Stationery orders.
7. The countries represented in the dataset.
8. The number of orders that have not been shipped.
9. The average price by category.
10. All orders where the quantity is greater than 5.

This changes the lesson from **memorizing Pandas syntax** into **solving a data problem**.

---

# 41. Common Student Mistakes

## Mistake 1

Writing:

```python
df["Age"] = 30
```

when they intended to compare.

Explain:

```python
=
```

means assignment.

```python
==
```

means comparison.

---

## Mistake 2

Forgetting parentheses with multiple conditions.

Correct:

```python
df[(df["Age"] > 25) & (df["Country"] == "UK")]
```

---

## Mistake 3

Using Python's `and` instead of Pandas' element-wise operators.

For DataFrame filtering, demonstrate:

```python
&
|
~
```

rather than:

```python
and
or
not
```

---

## Mistake 4

Confusing position with label.

Reinforce:

```text
iloc → position
loc  → label
```

---

## Mistake 5

Changing a DataFrame and expecting the original variable to change automatically.

For example:

```python
df.drop(...)
```

versus assigning the result or using `inplace=True`.

---

# 42. Instructor's Key Teaching Principle

Do not teach:

> "Here are 30 Pandas functions. Memorize them."

Teach:

> "Here is a question we want to answer. Which Pandas operation can answer it?"

For example:

**Question:** Which orders cost more than $100?

**Thinking:**

```text
Question
   ↓
Need rows
   ↓
Need condition
   ↓
Need filtering
   ↓
Boolean mask
   ↓
df[df["Price"] > 100]
```

This teaches students to think like programmers and analysts rather than copy code.

---

# 43. Final Mental Model

End the class with this diagram on the board:

```text
              PANDAS
                 │
        ┌────────┴────────┐
        │                 │
     SERIES           DATAFRAME
                           │
             ┌─────────────┼─────────────┐
             │             │             │
           READ          FILTER        MODIFY
             │             │             │
          Explore       Conditions      Update
          Select        Boolean         Delete
             │          masks           Create
             │             │             │
             └─────────────┼─────────────┘
                           │
                         CLEAN
                           │
                      MISSING DATA
                      DATA TYPES
                      RENAMING
                           │
                         ANALYZE
                           │
                   GROUP / COUNT / SORT
                           │
                         EXPORT
```

The core idea students should leave with is:

> **Pandas lets us turn raw structured data into information we can inspect, manipulate, clean, analyze, and save.**

# 44. Instructor Quick Reference

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
df[(df["Category"] == "Electronics") &
   (df["Country"] == "USA")]

# Membership
df[df["Country"].isin(["USA", "UK"])]

# NOT
df[~df["Country"].isin(["USA"])]

# Update
df.loc[df["Country"] == "USA", "Country"] = "United States"

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
df.sort_values(by="Price", ascending=False)

# Save
df.to_csv("processed.csv", index=False)
df.to_excel("processed.xlsx", index=False)
```

This reference follows the operations covered in the supplied Pandas material, including inspection, Boolean filtering, conditional updates, string transformations, and renaming.
