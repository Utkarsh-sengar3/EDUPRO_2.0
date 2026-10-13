# EDUPRO — Predictive Intelligence for Course Demand & Revenue Forecasting

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Framework](https://img.shields.io/badge/framework-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![ML Engine](https://img.shields.io/badge/ML-Scikit--learn-F7931E.svg)](https://scikit-learn.org/)
[![Theme Support](https://img.shields.io/badge/theme-Light%20%7C%20Dark-2563EB.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 1. Project Overview

**EDUPRO Predictive Intelligence** is an enterprise-grade predictive analytics platform designed to forecast next-month course enrollment demand and derive forward-looking revenue projections for online educational institutions.

The application operates as a unified single-page analytics application featuring custom enterprise navigation, real-time machine learning inference, dynamic Light and Dark mode theming, and multi-dimensional curriculum analytics.

---

## 2. Business Problem Statement

Online educational platforms face substantial uncertainty regarding curriculum demand dynamics:
- **Resource Allocation:** Over-allocation of instructional capacity on stagnating course offerings.
- **Pricing Inefficiencies:** Setting course fees without empirical demand elasticity modeling.
- **Delayed Intervention:** Relying purely on trailing summaries instead of prospective leading indicators.
- **Instructor Quality Valuation:** Lacking quantified understanding of how instructor tenure and ratings influence course retention.

---

## 3. Core Objectives

1. **Demand Forecasting:** Construct an autoregressive machine learning pipeline to estimate next-month course enrollment volume ($Target\_NextMonthEnrollments$).
2. **Revenue Derivation:** Translate course-level demand estimates into platform revenue projections ($Predicted\_Revenue = Demand \times Price$).
3. **Instructor Profiling:** Integrate instructor experience and rating into the forecasting feature set.
4. **Cross-Category Analytics:** Diagnose curriculum track health across 12 disciplines.
5. **Transparent Model Validation:** Evaluate model candidates using strict chronological out-of-time splits.

---

## 4. Feature Engineering & Dataset

The project uses longitudinal course-month panels compiled across EduPro transaction, course metadata, instructor profile, and learner interaction databases:

| Feature Category | Variables | Description |
| :--- | :--- | :--- |
| **Instructor Profile** | `AvgTeacherExperience`, `AvgTeacherRating` | Instructor domain tenure (years) and student review rating |
| **Autoregressive Lags** | `Lag1_Enrollments`, `Lag2_Enrollments`, `Lag3_Enrollments` | 1-, 2-, and 3-month prior enrollment counts |
| **Rolling Statistics** | `Rolling3_Enrollments`, `Rolling3_Revenue` | 3-month trailing moving averages |
| **Momentum Signals** | `EnrollmentMomentum` | Velocity differential ($Lag1 - Lag3$) |
| **Financial Signals** | `Lag1_Revenue`, `CoursePrice`, `LogCoursePrice`, `IsFreeCourse` | Historical monetization velocity and pricing attributes |
| **Course Metadata** | `CourseDuration`, `CourseRating`, `DurationBucket`, `CourseLevel` | Content duration, student ratings, and complexity level |
| **Calendar Cycles** | `MonthNumber`, `Quarter` | Academic seasonality and quarterly cyclicality |

---

## 5. Model Development & Validation Results

Five regression algorithms were evaluated using strict chronological out-of-time splits (Training: Pre-September 2025; Testing: September – November 2025):

| Algorithm | Mean Absolute Error (MAE) | Root Mean Squared Error (RMSE) | $R^2$ Score |
| :--- | :---: | :---: | :---: |
| **Random Forest Regressor** | **2.9662** | 3.8748 | -0.1190 |
| **Gradient Boosting Regressor** | 2.9794 | 3.8762 | -0.1199 |
| **Lasso Regression (Selected Candidate)** | **2.9917** | **3.8445** | **-0.1016** |
| **Ridge Regression** | 2.9942 | 3.8506 | -0.1052 |
| **Linear Regression (OLS)** | 2.9983 | 3.8561 | -0.1083 |

### Methodological Disclosure
- **Generalization Challenges:** The time-based test set exhibits negative $R^2$ values ($\approx -0.10$) due to short panel history (8 months) and non-stationary enrollment surges.
- **Operational Utility:** The model achieves a mean absolute error of $\approx 2.99$ enrollments per course, providing reliable directional demand tiering (Low, Moderate, High Demand) for operational planning.

---

## 6. Project Architecture

```
EDUPRO/
│
├── Phase-3/                     # Historical feature engineering scripts & ML datasets
├── Phase-4/                     # Model baseline development & initial evaluation outputs
├── Phase-5/                     # Time-series hyperparameter tuning & diagnostics
├── Phase-6/                     # Financial forecasting & category rollups
│
├── app.py                       # Main Streamlit application entry point & router
│
├── data/                        # Synchronized analytical datasets
│   ├── ml_ready_dataset.csv
│   ├── test_forecast_detail.csv
│   ├── category_revenue_forecast.csv
│   ├── course_revenue_forecast.csv
│   ├── free_vs_paid.csv
│   ├── model_results.csv
│   └── feature_importance.csv
│
├── models/                      # Serialized Scikit-learn pipelines & metadata
│   ├── demand_model.pkl
│   ├── demand_model_pipeline.pkl
│   ├── demand_model_lasso.pkl
│   ├── demand_model_gbr.pkl
│   ├── all_models.pkl
│   └── feature_metadata.json
│
├── utils/                       # Modular business logic & data handlers
│   ├── theme.py                 # Centralized Light/Dark theme manager & Plotly styling
│   ├── config.py                # Design constants and paths
│   ├── data_loader.py           # Cached dataset loading with error handling
│   ├── model_loader.py          # Cached model pipelines & inference functions
│   ├── preprocessing.py         # Feature matrix construction with instructor attributes
│   ├── forecasting.py           # Revenue simulation & aggregation logic
│   └── metrics.py               # Currency (₹ INR), integer, and badge formatters
│
├── views/                       # Single-Page Modular View Controllers
│   ├── overview.py
│   ├── eda.py
│   ├── demand_prediction.py
│   ├── revenue_forecast.py
│   ├── category_analysis.py
│   ├── model_performance.py
│   ├── feature_importance.py
│   └── about.py
│
├── train_and_save_models.py     # Model pipeline serialization script
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
```

---

## 7. How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. (Optional) Re-train and serialize models
python train_and_save_models.py

# 3. Launch the dashboard
streamlit run app.py
```
Open `http://localhost:8501` in your browser.
