"""
EDUPRO Model Loader & Real-Time Inference Module
Provides cached model loading and dynamic inference for course demand prediction.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import joblib
import numpy as np
import pandas as pd
import streamlit as st

from utils.config import MODELS_DIR
from utils.preprocessing import prepare_input_dataframe


@st.cache_resource(show_spinner=False)
def load_demand_pipeline(model_name: str = "Lasso"):
    """
    Loads serialized scikit-learn pipeline for real-time demand inference.
    Supports 'Lasso' (primary candidate) and 'Gradient Boosting'.
    """
    if model_name == "Gradient Boosting":
        target_path = MODELS_DIR / "demand_model_gbr.pkl"
    else:
        target_path = MODELS_DIR / "demand_model_lasso.pkl"
        
    if not target_path.exists():
        fallback_path = MODELS_DIR / "demand_model_pipeline.pkl"
        if fallback_path.exists():
            target_path = fallback_path
        else:
            return None
            
    try:
        pipeline = joblib.load(target_path)
        return pipeline
    except Exception as e:
        st.error(f"Error loading model pipeline: {e}")
        return None


@st.cache_resource(show_spinner=False)
def load_all_models() -> Dict[str, Any]:
    """Loads dictionary of all trained candidate pipelines."""
    path = MODELS_DIR / "all_models.pkl"
    if path.exists():
        try:
            return joblib.load(path)
        except Exception:
            return {}
    return {}


@st.cache_data(show_spinner=False)
def load_feature_metadata() -> Dict[str, Any]:
    """Loads metadata including categories, levels, and training feature names."""
    path = MODELS_DIR / "feature_metadata.json"
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "categories": [
            "Artificial Intelligence", "Business", "Cybersecurity", "Data Science",
            "Design", "Digital Marketing", "Finance", "Machine Learning",
            "Marketing", "Programming", "Project Management", "Web Development"
        ],
        "course_types": ["Paid", "Free"],
        "course_levels": ["Beginner", "Intermediate", "Advanced"],
        "duration_buckets": ["Short", "Medium", "Long", "Very Long"]
    }


def predict_demand(input_dict: Dict[str, Any], model_name: str = "Lasso") -> Tuple[float, float, pd.DataFrame]:
    """
    Executes real-time inference for a given course parameter configuration.
    Returns: (predicted_enrollments, predicted_revenue, prepared_feature_df)
    """
    pipe = load_demand_pipeline(model_name)
    df_input = prepare_input_dataframe(input_dict)
    
    if pipe is None:
        # Graceful fallback: return simple historical momentum/lag estimate
        lag1 = float(input_dict.get("Lag1_Enrollments", 10.0))
        pred_enrollments = max(0.0, lag1)
    else:
        raw_pred = pipe.predict(df_input)[0]
        # Enrollments cannot be negative in business reality
        pred_enrollments = max(0.0, float(raw_pred))
        
    price = float(input_dict.get("CoursePrice", 0.0))
    pred_revenue = float(pred_enrollments * price)
    
    return pred_enrollments, pred_revenue, df_input
