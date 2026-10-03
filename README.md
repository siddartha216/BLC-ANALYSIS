# Smart Business Lead Scoring and Prioritization Using Machine Learning

## Project Overview

This project focuses on analyzing and prioritizing business leads from the BLC-10 dataset.

The main goal is to convert a raw business lead dataset into a structured list of High, Medium, and Low priority leads using Machine Learning and data analysis techniques.

The project uses two main approaches:

1. Review and Comment Based Lead Prioritization
2. Category and Country Based Lead Prioritization

---

## Dataset

The original BLC-10 dataset contains 300 business records.

After data cleaning and preparation, 292 records were used for the final analysis.

The dataset contains information such as:

- Company Name
- Country
- City
- Category
- Website
- Contact
- Email
- Google Maps Link
- Reviews
- Comments

The dataset contains businesses from India and the USA.

---

## Project Workflow

The project follows these main steps:

Raw BLC Data
       ↓
Data Cleaning
       ↓
Data Preprocessing
       ↓
Feature Engineering
       ↓
Machine Learning Models
       ↓
Probability Calculation
       ↓
High / Medium / Low Classification
       ↓
Final Excel Output and Dashboard

---

## 1. Review and Comment Based Model

The first model uses customer review and comment information.

The main features used are:

- Reviews
- Comments

The data is cleaned and converted into numerical values before model training.

A Logistic Regression model is used to calculate the predicted probability for each business.

### Review Model Results

| Priority | Number of Leads |
|----------|-----------------|
| High | 83 |
| Medium | 110 |
| Low | 99 |
| Total | 292 |

The leads are sorted based on predicted probability along with review and comment values.

---

## 2. Category and Country Based Model

The second model focuses on business category and country.

The category information is cleaned and standardized before applying the model.

Country-specific category rankings are used for Indian and foreign businesses.

The model considers features such as:

- Company Name Length
- Company Word Count
- Category Frequency
- City Frequency
- City Encoding
- Category Encoding

A Random Forest Regressor with 100 estimators is used for this model.

---

## Category Probability

The category scoring system uses three probability levels:

| Category Level | Probability |
|----------------|-------------|
| Higher Ranked | 85% |
| Middle Ranked | 55% |
| Lower Ranked | 15% |

The Random Forest model uses these values to generate predicted probabilities for the business leads.

### Category Model Results

| Priority | Number of Leads |
|----------|-----------------|
| High | 223 |
| Medium | 49 |
| Low | 20 |
| Total | 292 |

---

## Category Analysis

The final Category Model separates businesses into High, Medium, and Low priority.

The High Priority group contains categories such as:

- General Store
- Convenience Store
- Cafe
- Tailor Shop
- Garage
- Clothing Store
- Liquor Shop
- Market
- Super Store

The Medium Priority group contains:

- Restaurant
- Beauty Parlour and Salon
- Cake Shop and Bakery

The Low Priority group contains:

- Pharmacy

The original category of each business is retained in the final output.

---

## Country Analysis

The cleaned dataset contains:

| Country | Leads |
|---------|------:|
| India | 217 |
| USA | 75 |
| Total | 292 |

Country information is also considered during category-based analysis.

---

## Machine Learning Techniques

The project uses:

- Logistic Regression
- Random Forest Regressor
- Label Encoding
- Feature Engineering
- Probability Prediction
- Lead Classification

---

## Data Analysis

The project also includes analysis of:

- Business Categories
- Country Distribution
- City Distribution
- Reviews
- Comments
- Category Frequency
- Lead Priority
- Predicted Probability

A dashboard is used to present the main findings in an easier format.

---

## Final Output

The final output contains important information such as:

- Company
- Country
- City
- Contact
- Google Maps Link
- Category
- Predicted Probability
- Priority

The leads are separated into:

- High
- Medium
- Low

This makes the final lead list easier to analyze and use.

---

## Tools and Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Seaborn
- OpenPyXL
- Microsoft Excel
- Jupyter Notebook

---

## Key Skills

This project helped develop skills in:

- Data Cleaning
- Data Preprocessing
- Feature Engineering
- Machine Learning
- Lead Scoring
- Probability Analysis
- Category Analysis
- Country-Based Analysis
- Excel Reporting
- Data Visualization

---

## Project Outcome

The project provides a structured approach for analyzing business leads and assigning priority levels.

By using review, comment, category, and country information, the raw BLC dataset is converted into an organized lead-prioritization system.

The final results can be used to identify and organize business leads based on their predicted priority.
