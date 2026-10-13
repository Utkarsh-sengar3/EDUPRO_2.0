"""
EDUPRO Forecasting & Analytics Utilities
Handles course-level and category-level aggregations, scenario simulations,
and revenue derivations.
"""

from typing import Dict, Any, List
import pandas as pd
import numpy as np


def compute_category_summary(forecast_df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates test forecasts by CourseCategory to evaluate total predicted demand and revenue.
    """
    if forecast_df.empty:
        return pd.DataFrame()
        
    enr_target = "Target_NextMonthEnrollments" if "Target_NextMonthEnrollments" in forecast_df.columns else "ActualEnrollments"
    
    summary = (
        forecast_df.groupby("CourseCategory")
        .agg(
            CourseCount=("CourseID", "nunique"),
            AvgPrice=("CoursePrice", "mean"),
            ActualEnrollments=(enr_target, "sum"),
            PredictedEnrollments=("PredictedEnrollments", "sum"),
            ActualRevenue=("ActualRevenue", "sum"),
            PredictedRevenue=("PredictedRevenue", "sum")
        )
        .reset_index()
    )
    
    summary["EnrollmentVariance"] = summary["PredictedEnrollments"] - summary["ActualEnrollments"]
    summary["RevenueVariance"] = summary["PredictedRevenue"] - summary["ActualRevenue"]
    return summary


def run_scenario_forecast(
    base_df: pd.DataFrame,
    price_factor: float = 1.0,
    demand_shock: float = 0.0
) -> pd.DataFrame:
    """
    Simulates portfolio revenue under hypothetical pricing and demand shock scenarios.
    """
    if base_df.empty:
        return pd.DataFrame()
        
    df = base_df.copy()
    df["SimulatedPrice"] = df["CoursePrice"] * price_factor
    df["SimulatedEnrollments"] = np.maximum(
        0, df["PredictedEnrollments"] * (1.0 + demand_shock / 100.0)
    )
    df["SimulatedRevenue"] = df["SimulatedEnrollments"] * df["SimulatedPrice"]
    return df
