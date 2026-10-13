"""
EDUPRO Data Loader Module
Provides cached, validated dataset loaders for all application views.
"""

from pathlib import Path
from typing import Optional
import pandas as pd
import streamlit as st

from utils.config import DATA_DIR, PHASE3_DIR, PHASE4_DIR, PHASE6_DIR


def _find_file(primary_rel: str, fallback_path: Path) -> Path:
    """Locates a dataset either in data/ or the original Phase folders."""
    primary_path = DATA_DIR / primary_rel
    if primary_path.exists():
        return primary_path
    if fallback_path.exists():
        return fallback_path
    return primary_path


@st.cache_data(show_spinner=False)
def load_ml_ready_dataset() -> pd.DataFrame:
    """Loads master ML-ready dataset with 480 course-month observations."""
    p = _find_file("ml_ready_dataset.csv", PHASE3_DIR / "EduPro_Phase3_ML_Ready_Dataset.csv")
    if not p.exists():
        st.error(f"Master dataset file not found at {p}. Please verify data directory.")
        return pd.DataFrame()
    
    df = pd.read_csv(p)
    if "Month" in df.columns:
        df["Month"] = pd.to_datetime(df["Month"])
    return df


@st.cache_data(show_spinner=False)
def load_model_results() -> pd.DataFrame:
    """Loads Phase-4/5 model comparison metrics table."""
    p = _find_file("model_results.csv", PHASE4_DIR / "EduPro_Phase4_Model_Results.csv")
    if not p.exists():
        return pd.DataFrame()
    return pd.read_csv(p)


@st.cache_data(show_spinner=False)
def load_feature_importance() -> pd.DataFrame:
    """Loads feature importance rankings."""
    p = _find_file("feature_importance.csv", PHASE4_DIR / "EduPro_Phase4_Feature_Importance.csv")
    if not p.exists():
        return pd.DataFrame()
    return pd.read_csv(p)


@st.cache_data(show_spinner=False)
def load_test_forecast_detail() -> pd.DataFrame:
    """Loads out-of-time test set forecast details (180 records)."""
    p = _find_file("test_forecast_detail.csv", PHASE6_DIR / "EduPro_Phase6_Test_Forecast_Detail.csv")
    if not p.exists():
        # Fallback to Phase-4 best model forecasts
        p = _find_file("best_model_forecasts.csv", PHASE4_DIR / "EduPro_Phase4_Best_Model_Forecasts.csv")
    if not p.exists():
        return pd.DataFrame()
    
    df = pd.read_csv(p)
    if "Month" in df.columns:
        df["Month"] = pd.to_datetime(df["Month"])
    return df


@st.cache_data(show_spinner=False)
def load_category_forecasts() -> pd.DataFrame:
    """Loads aggregated category-level revenue and demand forecasts."""
    p = _find_file("category_revenue_forecast.csv", PHASE6_DIR / "EduPro_Phase6_Category_Revenue_Forecast.csv")
    if not p.exists():
        return pd.DataFrame()
    return pd.read_csv(p)


@st.cache_data(show_spinner=False)
def load_course_forecasts() -> pd.DataFrame:
    """Loads aggregated course-level revenue and demand forecasts."""
    p = _find_file("course_revenue_forecast.csv", PHASE6_DIR / "EduPro_Phase6_Course_Revenue_Forecast.csv")
    if not p.exists():
        return pd.DataFrame()
    return pd.read_csv(p)


@st.cache_data(show_spinner=False)
def load_free_vs_paid() -> pd.DataFrame:
    """Loads Free vs Paid course enrollment & revenue breakdown."""
    p = _find_file("free_vs_paid.csv", PHASE6_DIR / "EduPro_Phase6_Free_vs_Paid.csv")
    if not p.exists():
        return pd.DataFrame()
    return pd.read_csv(p)
