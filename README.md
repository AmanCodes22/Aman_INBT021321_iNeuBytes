# GOV.UK Publication Update Time Predictor

## Project Overview

This project uses historical GOV.UK publication data to predict whether a publication is likely to fall into a high update-time category.

The project covers the complete machine learning workflow:

- Data collection and web scraping
- Data cleaning and preprocessing
- Exploratory Data Analysis (EDA)
- Feature engineering
- Text feature extraction using TF-IDF
- Machine learning model development
- Hyperparameter tuning
- Model evaluation
- Model serialization
- Streamlit application
- End-to-end testing
- Live deployment

---

## Problem Statement

Government websites contain a large number of publications that may be updated at different times after their initial publication.

The objective of this project is to use historical publication information to predict whether a newly published GOV.UK document is likely to have a high update time.

This is formulated as a binary classification problem.

### Target Variable

`high_update_time`

- `0` → Normal / Low Update Time
- `1` → High Update Time

---

## Dataset

The dataset contains GOV.UK publication information including:

- Title
- Description
- URL
- Author Organisation
- Published Date
- Updated Date
- Topic URL

Total records:

**468**

Total columns:

**7**

The dataset contains publications from multiple UK government organisations and topics.

---

## Data Collection

The data was collected from publicly available GOV.UK publication pages using Python and web scraping techniques.

The scraping process was designed for educational purposes and included:

- Publicly available data
- Request rate limiting
- Identifiable request headers
- Limited sample size
- Respect for website scraping policies

---

## Data Preprocessing

The following preprocessing tasks were performed:

- Missing value analysis
- Duplicate detection
- HTML removal from descriptions
- Date conversion
- URL validation
- Whitespace checking
- Data type validation
- Text cleaning
- Column consistency checks

### Missing Values

The final dataset contains:

- `description`: 146 missing values
- `topic_url`: 170 missing values

Missing text values were handled during feature processing.

---

## Exploratory Data Analysis

EDA was performed to understand:

- Publication distribution by year
- Top publishing organisations
- Missing values
- Description length distribution
- Publication topic distribution
- Relationship between publication year and organisation

The dataset contains publications from **1975 to 2026**, with publication activity increasing substantially in recent years.

---

## Feature Engineering

Several new features were created.

### Date Features

- `published_year`
- `published_month`
- `published_quarter`
- `published_dayofweek`

### Text Features

- `title_length`
- `title_word_count`
- `description_length`
- `description_word_count`
- `text_length`
- `text_word_count`

### Organisation Features

- `organisation_length`
- `organisation_word_count`

### Topic Features

- `has_topic`
- `topic_category`

---

## Target Creation

The number of days between publication and update was calculated using:

`days_to_update`

The target variable `high_update_time` was then created from the update-time information.

The target distribution was:

| Class | Records | Percentage |
|------|--------:|-----------:|
| 0 - Normal | 336 | 71.79% |
| 1 - High | 132 | 28.21% |

Because the classes are imbalanced, class-weighted models were considered during model development.

---

## Text Feature Extraction

TF-IDF was used to convert publication text into numerical features.

### Title

Maximum:

**500 TF-IDF features**

### Description

Maximum:

**1000 TF-IDF features**

These features were combined with numerical and categorical features.

---

## Machine Learning Models

Three classification models were evaluated:

1. Logistic Regression
2. Support Vector Machine (SVM)
3. Random Forest

A baseline model was established before hyperparameter tuning.

---

## Baseline Results

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|------|---------:|----------:|-------:|----:|--------:|
| Logistic Regression | 0.7021 | 0.4737 | 0.3333 | 0.3913 | 0.6855 |
| SVM | 0.7234 | 0.6000 | 0.1111 | 0.1875 | 0.6313 |
| Random Forest | 0.7234 | 0.6000 | 0.1111 | 0.1875 | 0.6479 |

---

## Hyperparameter Tuning

GridSearchCV with 5-fold cross-validation was used to tune the models.

### Tuned Logistic Regression

Best parameters:

```text
C = 10
class_weight = balanced
solver = liblinear

F1 score:

0.4407

Tuned SVM

Best parameters:

C = 1
class_weight = balanced
kernel = linear

F1 score:

0.4483

Tuned Random Forest

Best parameters:

class_weight = balanced
max_depth = 10
min_samples_split = 5
n_estimators = 100

F1 score:

0.4912

Final Model

Random Forest was selected as the final model.

Final test performance:

Metric	Score
Accuracy	69.15%
Precision	46.67%
Recall	51.85%
F1 Score	49.12%
ROC-AUC	69.43%

The Random Forest provided the best F1 score among the tuned models and was therefore selected for deployment.

Model Interpretability

Feature importance analysis was performed for the Random Forest model.

Important features included:

Published year
Description word count
Text word count
Title TF-IDF features
Text length
Organisation length
Description length
Published month
Topic category
Title word count

These features indicate that publication timing, text characteristics, organisation information and topic information contribute to the model's predictions.

Final Pipeline

A complete deployment pipeline was created containing:

Raw Input
    ↓
Feature Engineering
    ↓
TF-IDF + Numerical + Categorical Preprocessing
    ↓
Random Forest
    ↓
Prediction

The complete pipeline was serialized using joblib.

File:

data/govuk_final_deployment_pipeline.joblib
Streamlit Application

A Streamlit application was developed around the trained model.

The application accepts:

Publication Title
Description
Author Organisation
Published Date
Topic URL

The application then predicts:

Low Update Time
High Update Time

along with the probability of high update time.

End-to-End Testing

The deployed application was tested using several new inputs, including missing-value edge cases.

Example results:

Test Case	Prediction	High Update Probability
Test 1	Low Update Time	41.37%
Test 2	High Update Time	51.74%
Test 3	High Update Time	52.03%
Test 4	Low Update Time	43.00%

The application successfully returned predictions for the tested inputs.

Project Structure
govuk-web-scrapper/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── govuk_publications.csv
│   ├── govuk_publications_cleaned.csv
│   └── govuk_final_deployment_pipeline.joblib
│
└── src/
    ├── scraper.py
    └── govuk_publication_prediction.ipynb
Technologies Used
Python
Pandas
NumPy
Scikit-learn
BeautifulSoup
Matplotlib
Seaborn
Joblib
Streamlit
Conclusion

This project demonstrates an end-to-end machine learning workflow starting from web data collection and ending with a working prediction application.

The final Random Forest model uses publication metadata and text-based features to classify whether a GOV.UK publication is likely to fall into the high update-time category.
Disclaimer

This project was developed for educational purposes. Predictions are based on historical GOV.UK publication data and should not be considered official government forecasts or decisions.