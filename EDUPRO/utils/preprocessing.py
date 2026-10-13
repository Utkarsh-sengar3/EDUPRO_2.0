"""
EDUPRO Preprocessing Module
Constructs and validates feature matrices for single-instance or batch predictions,
including Instructor Profile features (AvgTeacherExperience, AvgTeacherRating).
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List


FEATURE_COLS = [
    "CourseCategory", "CourseType", "CourseLevel",
    "CoursePrice", "LogCoursePrice", "IsFreeCourse",
    "CourseDuration", "CourseRating",
    "AvgTeacherExperience", "AvgTeacherRating",
    "DurationBucket", "MonthNumber", "Quarter",
    "Lag1_Enrollments", "Lag2_Enrollments", "Lag3_Enrollments",
    "Rolling3_Enrollments", "Lag1_Revenue", "Rolling3_Revenue",
    "EnrollmentMomentum"
]

CATEGORICAL_FEATURES = ["CourseCategory", "CourseType", "CourseLevel", "DurationBucket"]
NUMERIC_FEATURES = [c for c in FEATURE_COLS if c not in CATEGORICAL_FEATURES]


def derive_duration_bucket(duration_hours: float) -> str:
    """Classifies course duration into standardized categorical buckets."""
    if duration_hours <= 10.0:
        return "Short"
    elif duration_hours <= 30.0:
        return "Medium"
    elif duration_hours <= 60.0:
        return "Long"
    else:
        return "Very Long"


def prepare_input_dataframe(data_dict: Dict[str, Any]) -> pd.DataFrame:
    """
    Takes raw user input dictionary, derives engineered features,
    and returns a 1-row DataFrame strictly aligned with the training feature schema.
    """
    price = float(data_dict.get("CoursePrice", 0.0))
    duration = float(data_dict.get("CourseDuration", 10.0))
    course_rating = float(data_dict.get("CourseRating", 4.5))
    
    # Instructor Profile Features
    teacher_exp = float(
        data_dict.get("AvgTeacherExperience", 
        data_dict.get("InstructorExperience", 5.0))
    )
    teacher_rating = float(
        data_dict.get("AvgTeacherRating", 
        data_dict.get("InstructorRating", 4.5))
    )
    
    # Feature calculations
    is_free = 1 if price == 0.0 else 0
    course_type = "Free" if is_free else data_dict.get("CourseType", "Paid")
    log_price = np.log1p(price)
    duration_bucket = derive_duration_bucket(duration)
    
    lag1_enr = float(data_dict.get("Lag1_Enrollments", 10.0))
    lag2_enr = float(data_dict.get("Lag2_Enrollments", lag1_enr))
    lag3_enr = float(data_dict.get("Lag3_Enrollments", lag2_enr))
    
    # Rolling 3-month average calculation
    rolling3_enr = data_dict.get("Rolling3_Enrollments")
    if rolling3_enr is None or rolling3_enr == 0.0:
        rolling3_enr = np.mean([lag1_enr, lag2_enr, lag3_enr])
    else:
        rolling3_enr = float(rolling3_enr)
        
    lag1_rev = float(data_dict.get("Lag1_Revenue", lag1_enr * price))
    
    rolling3_rev = data_dict.get("Rolling3_Revenue")
    if rolling3_rev is None or rolling3_rev == 0.0:
        rolling3_rev = float(rolling3_enr * price)
    else:
        rolling3_rev = float(rolling3_rev)
        
    momentum = float(data_dict.get("EnrollmentMomentum", lag1_enr - lag3_enr))
    
    month_num = int(data_dict.get("MonthNumber", 12))
    quarter = (month_num - 1) // 3 + 1
    
    row = {
        "CourseCategory": str(data_dict.get("CourseCategory", "Programming")),
        "CourseType": str(course_type),
        "CourseLevel": str(data_dict.get("CourseLevel", "Intermediate")),
        "CoursePrice": float(price),
        "LogCoursePrice": float(log_price),
        "IsFreeCourse": int(is_free),
        "CourseDuration": float(duration),
        "CourseRating": float(course_rating),
        "AvgTeacherExperience": float(teacher_exp),
        "AvgTeacherRating": float(teacher_rating),
        "DurationBucket": str(duration_bucket),
        "MonthNumber": int(month_num),
        "Quarter": int(quarter),
        "Lag1_Enrollments": float(lag1_enr),
        "Lag2_Enrollments": float(lag2_enr),
        "Lag3_Enrollments": float(lag3_enr),
        "Rolling3_Enrollments": float(rolling3_enr),
        "Lag1_Revenue": float(lag1_rev),
        "Rolling3_Revenue": float(rolling3_rev),
        "EnrollmentMomentum": float(momentum)
    }
    
    df = pd.DataFrame([row])[FEATURE_COLS]
    return df
