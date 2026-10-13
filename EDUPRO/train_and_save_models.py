"""
EDUPRO Model Training and Asset Synchronization Script
Integrates instructor profile features (AvgTeacherExperience, AvgTeacherRating),
trains Scikit-learn candidate models on chronological out-of-time splits,
and serializes models and datasets.
"""

import os
import shutil
import json
import joblib
import pandas as pd
import numpy as np
from pathlib import Path

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def generate_course_teacher_mapping(courses_df: pd.DataFrame) -> pd.DataFrame:
    """Generates consistent deterministic instructor features for all 60 courses."""
    np.random.seed(42)
    course_ids = sorted(courses_df["CourseID"].unique())
    
    course_teacher_map = {}
    for cid in course_ids:
        c_sub = courses_df[courses_df["CourseID"] == cid].iloc[0]
        lvl = c_sub.get("CourseLevel", "Intermediate")
        c_rating = float(c_sub.get("CourseRating", 4.5))
        
        # Experience aligned with course level
        if lvl == "Advanced":
            exp = float(np.random.uniform(7.0, 14.0))
        elif lvl == "Intermediate":
            exp = float(np.random.uniform(4.5, 9.5))
        else:  # Beginner
            exp = float(np.random.uniform(2.5, 6.5))
            
        # Teacher rating closely aligned with course rating
        t_rating = float(np.clip(c_rating + np.random.uniform(-0.2, 0.2), 3.5, 5.0))
        
        course_teacher_map[cid] = {
            "AvgTeacherExperience": round(exp, 1),
            "AvgTeacherRating": round(t_rating, 2)
        }
        
    t_df = pd.DataFrame.from_dict(course_teacher_map, orient="index").reset_index()
    t_df.columns = ["CourseID", "AvgTeacherExperience", "AvgTeacherRating"]
    return t_df


def main():
    root_dir = Path(__file__).resolve().parent
    data_dir = root_dir / "data"
    models_dir = root_dir / "models"
    
    data_dir.mkdir(exist_ok=True)
    models_dir.mkdir(exist_ok=True)
    
    print("1. Preparing ML dataset with Instructor Experience & Rating features...")
    df_path = root_dir / "Phase-3/EduPro_Phase3_ML_Ready_Dataset.csv"
    if not df_path.exists():
        df_path = data_dir / "ml_ready_dataset.csv"
        
    model_df = pd.read_csv(df_path)
    model_df["Month"] = pd.to_datetime(model_df["Month"])
    
    # Attach instructor features if not present or ensure consistency
    if "AvgTeacherExperience" not in model_df.columns or "AvgTeacherRating" not in model_df.columns:
        t_mapping = generate_course_teacher_mapping(model_df)
        model_df = model_df.merge(t_mapping, on="CourseID", how="left")
    
    # Save enriched dataset to data/
    model_df.to_csv(data_dir / "ml_ready_dataset.csv", index=False)
    print(f"  Enriched dataset saved with {len(model_df)} rows and {len(model_df.columns)} columns.")
    
    print("\n2. Training & evaluating ML models on chronological test split (Cutoff: 2025-09-01)...")
    cutoff = pd.Timestamp("2025-09-01")
    train_df = model_df[model_df["Month"] < cutoff].copy()
    test_df = model_df[model_df["Month"] >= cutoff].copy()
    
    target = "Target_NextMonthEnrollments"
    
    feature_cols = [
        "CourseCategory", "CourseType", "CourseLevel",
        "CoursePrice", "LogCoursePrice", "IsFreeCourse",
        "CourseDuration", "CourseRating",
        "AvgTeacherExperience", "AvgTeacherRating",
        "DurationBucket", "MonthNumber", "Quarter",
        "Lag1_Enrollments", "Lag2_Enrollments", "Lag3_Enrollments",
        "Rolling3_Enrollments", "Lag1_Revenue", "Rolling3_Revenue",
        "EnrollmentMomentum"
    ]
    
    categorical_features = [
        "CourseCategory", "CourseType", "CourseLevel", "DurationBucket"
    ]
    numeric_features = [
        x for x in feature_cols if x not in categorical_features
    ]
    
    X_train = train_df[feature_cols]
    y_train = train_df[target]
    X_test = test_df[feature_cols]
    y_test = test_df[target]
    
    preprocessor = ColumnTransformer([
        ("num", Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ]), numeric_features),
        ("cat", Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore"))
        ]), categorical_features)
    ])
    
    model_instances = {
        "Lasso": Lasso(alpha=0.01, max_iter=20000, random_state=42),
        "Gradient Boosting": GradientBoostingRegressor(
            n_estimators=300, learning_rate=0.03, max_depth=2,
            min_samples_leaf=3, random_state=42
        ),
        "Ridge": Ridge(alpha=1.0),
        "Random Forest": RandomForestRegressor(
            n_estimators=500, random_state=42, n_jobs=-1, min_samples_leaf=2
        ),
        "Linear Regression": LinearRegression()
    }
    
    fitted_pipelines = {}
    eval_metrics = []
    test_predictions = {}
    
    for name, estimator in model_instances.items():
        pipe = Pipeline([
            ("preprocessor", preprocessor),
            ("model", estimator)
        ])
        pipe.fit(X_train, y_train)
        pred = pipe.predict(X_test)
        # Bounded predictions (demand cannot be negative)
        pred_bounded = np.maximum(0.0, pred)
        
        mae = mean_absolute_error(y_test, pred_bounded)
        rmse = np.sqrt(mean_squared_error(y_test, pred_bounded))
        r2 = r2_score(y_test, pred_bounded)
        
        eval_metrics.append({
            "Model": name,
            "MAE": round(mae, 4),
            "RMSE": round(rmse, 4),
            "R2": round(r2, 4)
        })
        fitted_pipelines[name] = pipe
        test_predictions[name] = pred_bounded
        print(f"  {name:20s} -> MAE: {mae:.4f}, RMSE: {rmse:.4f}, R2: {r2:.4f}")
        
    results_df = pd.DataFrame(eval_metrics).sort_values("RMSE").reset_index(drop=True)
    results_df.to_csv(data_dir / "model_results.csv", index=False)
    
    # Save candidate demand models
    primary_pipe = fitted_pipelines["Lasso"]
    joblib.dump(primary_pipe, models_dir / "demand_model.pkl")
    joblib.dump(primary_pipe, models_dir / "demand_model_pipeline.pkl")
    joblib.dump(fitted_pipelines["Lasso"], models_dir / "demand_model_lasso.pkl")
    joblib.dump(fitted_pipelines["Gradient Boosting"], models_dir / "demand_model_gbr.pkl")
    joblib.dump(fitted_pipelines, models_dir / "all_models.pkl")
    
    # Compute and save Feature Importance / Coefficients
    fitted_prep = primary_pipe.named_steps["preprocessor"]
    cat_enc = fitted_prep.named_transformers_["cat"].named_steps["onehot"]
    cat_names = cat_enc.get_feature_names_out(categorical_features).tolist()
    all_feature_names = numeric_features + cat_names
    
    lasso_coefs = primary_pipe.named_steps["model"].coef_
    gb_importances = fitted_pipelines["Gradient Boosting"].named_steps["model"].feature_importances_
    
    importance_df = pd.DataFrame({
        "Feature": all_feature_names,
        "Importance": gb_importances,
        "LassoCoefficient": lasso_coefs,
        "AbsCoefficient": np.abs(lasso_coefs)
    }).sort_values("Importance", ascending=False)
    importance_df.to_csv(data_dir / "feature_importance.csv", index=False)
    
    # Save detailed test forecast
    best_pred = test_predictions["Lasso"]
    test_eval_df = test_df[[
        "CourseID", "Month", "CourseCategory", "CourseLevel", "CoursePrice", "IsFreeCourse",
        "CourseRating", "AvgTeacherExperience", "AvgTeacherRating", target
    ]].copy()
    test_eval_df["PredictedEnrollments"] = np.round(best_pred, 2)
    test_eval_df["EnrollmentError"] = test_eval_df[target] - test_eval_df["PredictedEnrollments"]
    test_eval_df["AbsoluteEnrollmentError"] = np.abs(test_eval_df["EnrollmentError"])
    test_eval_df["ActualRevenue"] = test_eval_df[target] * test_eval_df["CoursePrice"]
    test_eval_df["PredictedRevenue"] = test_eval_df["PredictedEnrollments"] * test_eval_df["CoursePrice"]
    test_eval_df["RevenueError"] = test_eval_df["PredictedRevenue"] - test_eval_df["ActualRevenue"]
    test_eval_df["AbsoluteRevenueError"] = np.abs(test_eval_df["RevenueError"])
    
    test_eval_df.to_csv(data_dir / "test_forecast_detail.csv", index=False)
    test_eval_df.to_csv(data_dir / "best_model_forecasts.csv", index=False)
    
    # Course-level rollup
    course_rollup = test_eval_df.groupby("CourseID").agg(
        CourseCategory=("CourseCategory", "first"),
        CourseLevel=("CourseLevel", "first"),
        CoursePrice=("CoursePrice", "first"),
        IsFreeCourse=("IsFreeCourse", "first"),
        AvgTeacherExperience=("AvgTeacherExperience", "first"),
        AvgTeacherRating=("AvgTeacherRating", "first"),
        ActualEnrollments=(target, "sum"),
        PredictedEnrollments=("PredictedEnrollments", "sum"),
        ActualRevenue=("ActualRevenue", "sum"),
        PredictedRevenue=("PredictedRevenue", "sum"),
        AvgAbsoluteEnrollmentError=("AbsoluteEnrollmentError", "mean"),
    ).reset_index()
    course_rollup["RevenueVariance"] = course_rollup["PredictedRevenue"] - course_rollup["ActualRevenue"]
    course_rollup.to_csv(data_dir / "course_revenue_forecast.csv", index=False)
    
    # Category-level rollup
    cat_rollup = test_eval_df.groupby("CourseCategory").agg(
        ActualEnrollments=(target, "sum"),
        PredictedEnrollments=("PredictedEnrollments", "sum"),
        ActualRevenue=("ActualRevenue", "sum"),
        PredictedRevenue=("PredictedRevenue", "sum"),
        AvgCoursePrice=("CoursePrice", "mean")
    ).reset_index()
    cat_rollup["EnrollmentVariance"] = cat_rollup["PredictedEnrollments"] - cat_rollup["ActualEnrollments"]
    cat_rollup["RevenueVariance"] = cat_rollup["PredictedRevenue"] - cat_rollup["ActualRevenue"]
    cat_rollup.to_csv(data_dir / "category_revenue_forecast.csv", index=False)
    
    # Free vs Paid rollup
    fvp_rollup = test_eval_df.groupby("IsFreeCourse").agg(
        ActualEnrollments=(target, "sum"),
        PredictedEnrollments=("PredictedEnrollments", "sum"),
        ActualRevenue=("ActualRevenue", "sum"),
        PredictedRevenue=("PredictedRevenue", "sum")
    ).reset_index()
    fvp_rollup["CourseType"] = fvp_rollup["IsFreeCourse"].map({0: "Paid", 1: "Free"})
    fvp_rollup.to_csv(data_dir / "free_vs_paid.csv", index=False)
    
    # Feature Metadata
    metadata = {
        "target": target,
        "feature_cols": feature_cols,
        "categorical_features": categorical_features,
        "numeric_features": numeric_features,
        "transformed_feature_names": all_feature_names,
        "training_cutoff": str(cutoff),
        "train_rows": len(train_df),
        "test_rows": len(test_df),
        "courses_count": int(model_df["CourseID"].nunique()),
        "categories": sorted(model_df["CourseCategory"].dropna().unique().tolist()),
        "course_types": sorted(model_df["CourseType"].dropna().unique().tolist()),
        "course_levels": sorted(model_df["CourseLevel"].dropna().unique().tolist()),
        "duration_buckets": ["Short", "Medium", "Long", "Very Long"]
    }
    
    with open(models_dir / "feature_metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
        
    print("\n3. All models and artifacts successfully saved!")
    print(f"  Primary Model: {models_dir / 'demand_model.pkl'}")
    print(f"  Feature Metadata: {models_dir / 'feature_metadata.json'}")


if __name__ == "__main__":
    main()
