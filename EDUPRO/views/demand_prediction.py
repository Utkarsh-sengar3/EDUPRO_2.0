"""
EDUPRO - Course Demand Prediction View
Interactive real-time inference interface incorporating course characteristics,
instructor profile attributes (experience, rating), and historical lag velocity.
"""

import streamlit as st
import pandas as pd
import numpy as np

from utils.theme import get_theme
from utils.data_loader import load_ml_ready_dataset
from utils.model_loader import predict_demand, load_feature_metadata
from utils.metrics import (
    format_currency,
    format_int,
    render_kpi_card,
    get_demand_category_info
)


def render_demand_prediction(theme_mode: str = "light"):
    theme = get_theme(theme_mode)
    
    # Top Header
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.35rem;">
            <div>
                <h1>Course Demand Prediction</h1>
                <div class="page-subtitle">Estimate next-month enrollment demand using course characteristics, instructor profile, and historical performance.</div>
            </div>
            <div>
                <span class="badge badge-moderate" style="font-size: 0.76rem; padding: 0.35rem 0.75rem;">🤖 REAL-TIME INFERENCE</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    ml_df = load_ml_ready_dataset()
    meta = load_feature_metadata()
    
    categories = meta.get("categories", [
        "Artificial Intelligence", "Business", "Cybersecurity", "Data Science",
        "Design", "Digital Marketing", "Finance", "Machine Learning",
        "Marketing", "Programming", "Project Management", "Web Development"
    ])
    levels = meta.get("course_levels", ["Beginner", "Intermediate", "Advanced"])
    types = meta.get("course_types", ["Paid", "Free"])

    # Input Method Card
    is_dark = theme_mode == "dark"
    card_bg = theme["bg_card"]
    border_col = theme["border_card"]
    
    mode_col1, mode_col2 = st.columns([2, 2])
    with mode_col1:
        entry_mode = st.radio(
            "Inference Mode",
            options=["Select Existing Course from Catalog", "Custom Course Parameters"],
            horizontal=True
        )

    preset_data = {}
    if entry_mode == "Select Existing Course from Catalog" and not ml_df.empty:
        latest_records = ml_df.sort_values("Month").groupby("CourseID").last().reset_index()
        course_options = latest_records["CourseID"].tolist()
        
        with mode_col2:
            selected_course_id = st.selectbox(
                "Select Course ID",
                options=course_options,
                index=0
            )
            
        c_row = latest_records[latest_records["CourseID"] == selected_course_id].iloc[0]
        preset_data = {
            "CourseCategory": c_row["CourseCategory"],
            "CourseType": c_row["CourseType"],
            "CourseLevel": c_row["CourseLevel"],
            "CoursePrice": float(c_row["CoursePrice"]),
            "CourseDuration": float(c_row["CourseDuration"]),
            "CourseRating": float(c_row["CourseRating"]),
            "AvgTeacherExperience": float(c_row.get("AvgTeacherExperience", 6.0)),
            "AvgTeacherRating": float(c_row.get("AvgTeacherRating", 4.5)),
            "Lag1_Enrollments": float(c_row["Lag1_Enrollments"]),
            "Lag2_Enrollments": float(c_row["Lag2_Enrollments"]),
            "Lag3_Enrollments": float(c_row["Lag3_Enrollments"]),
            "Rolling3_Enrollments": float(c_row["Rolling3_Enrollments"]),
            "Lag1_Revenue": float(c_row["Lag1_Revenue"]),
            "Rolling3_Revenue": float(c_row["Rolling3_Revenue"]),
            "MonthNumber": int(c_row["MonthNumber"])
        }

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 2-Column Structured Form
    with st.form("demand_prediction_form"):
        left_col, right_col = st.columns(2)
        
        with left_col:
            st.markdown("### 1. Course Architecture")
            
            cat_idx = categories.index(preset_data["CourseCategory"]) if preset_data.get("CourseCategory") in categories else 0
            in_category = st.selectbox("Course Category", options=categories, index=cat_idx)
            
            type_idx = types.index(preset_data["CourseType"]) if preset_data.get("CourseType") in types else 0
            in_type = st.selectbox("Course Type", options=types, index=type_idx)
            
            lvl_idx = levels.index(preset_data["CourseLevel"]) if preset_data.get("CourseLevel") in levels else 1
            in_level = st.selectbox("Course Level", options=levels, index=lvl_idx)
            
            default_price = 0.0 if in_type == "Free" else float(preset_data.get("CoursePrice", 499.0))
            in_price = st.number_input(
                "Course Price (₹)",
                min_value=0.0,
                max_value=20000.0,
                value=default_price,
                step=50.0
            )
            
            in_duration = st.number_input(
                "Course Duration (Hours)",
                min_value=1.0,
                max_value=200.0,
                value=float(preset_data.get("CourseDuration", 24.0)),
                step=1.0
            )
            
        with right_col:
            st.markdown("### 2. Instructor Profile & Historical Velocity")
            
            in_rating = st.slider(
                "Course Rating (1.0 to 5.0 Stars)",
                min_value=1.0,
                max_value=5.0,
                value=float(preset_data.get("CourseRating", 4.6)),
                step=0.1
            )
            
            inst_c1, inst_c2 = st.columns(2)
            with inst_c1:
                in_teacher_exp = st.number_input(
                    "Instructor Experience (Years)",
                    min_value=0.5,
                    max_value=30.0,
                    value=float(preset_data.get("AvgTeacherExperience", 6.5)),
                    step=0.5
                )
            with inst_c2:
                in_teacher_rating = st.slider(
                    "Instructor Rating (1-5★)",
                    min_value=1.0,
                    max_value=5.0,
                    value=float(preset_data.get("AvgTeacherRating", 4.7)),
                    step=0.1
                )
                
            lag_c1, lag_c2, lag_c3 = st.columns(3)
            with lag_c1:
                in_lag1_enr = st.number_input(
                    "Previous Month (t-1)",
                    min_value=0.0,
                    max_value=500.0,
                    value=float(preset_data.get("Lag1_Enrollments", 15.0)),
                    step=1.0
                )
            with lag_c2:
                in_lag2_enr = st.number_input(
                    "Previous 2 Month (t-2)",
                    min_value=0.0,
                    max_value=500.0,
                    value=float(preset_data.get("Lag2_Enrollments", 14.0)),
                    step=1.0
                )
            with lag_c3:
                in_lag3_enr = st.number_input(
                    "Previous 3 Month (t-3)",
                    min_value=0.0,
                    max_value=500.0,
                    value=float(preset_data.get("Lag3_Enrollments", 12.0)),
                    step=1.0
                )

        st.markdown("### 3. Trailing Horizon Financials")
        b_c1, b_c2, b_c3 = st.columns(3)
        with b_c1:
            default_rolling_enr = (in_lag1_enr + in_lag2_enr + in_lag3_enr) / 3.0
            in_rolling3_enr = st.number_input(
                "3-Month Average Enrollment",
                min_value=0.0,
                max_value=500.0,
                value=float(preset_data.get("Rolling3_Enrollments", default_rolling_enr)),
                step=0.5
            )
        with b_c2:
            default_lag1_rev = in_lag1_enr * in_price
            in_lag1_rev = st.number_input(
                "Previous Month Revenue (₹)",
                min_value=0.0,
                max_value=2000000.0,
                value=float(preset_data.get("Lag1_Revenue", default_lag1_rev)),
                step=100.0
            )
        with b_c3:
            default_rolling_rev = in_rolling3_enr * in_price
            in_rolling3_rev = st.number_input(
                "3-Month Average Revenue (₹)",
                min_value=0.0,
                max_value=2000000.0,
                value=float(preset_data.get("Rolling3_Revenue", default_rolling_rev)),
                step=100.0
            )

        st.markdown("<div style='margin-top: 0.75rem;'></div>", unsafe_allow_html=True)
        submit_btn = st.form_submit_button("⚡ GENERATE FORECAST", use_container_width=True)

    # Process and display prediction
    if submit_btn or entry_mode == "Select Existing Course from Catalog":
        input_payload = {
            "CourseCategory": in_category,
            "CourseType": "Free" if in_price == 0 else in_type,
            "CourseLevel": in_level,
            "CoursePrice": in_price,
            "CourseDuration": in_duration,
            "CourseRating": in_rating,
            "AvgTeacherExperience": in_teacher_exp,
            "AvgTeacherRating": in_teacher_rating,
            "MonthNumber": 12,
            "Lag1_Enrollments": in_lag1_enr,
            "Lag2_Enrollments": in_lag2_enr,
            "Lag3_Enrollments": in_lag3_enr,
            "Rolling3_Enrollments": in_rolling3_enr,
            "Lag1_Revenue": in_lag1_rev,
            "Rolling3_Revenue": in_rolling3_rev,
            "EnrollmentMomentum": in_lag1_enr - in_lag3_enr
        }
        
        pred_enrollments, pred_revenue, _ = predict_demand(input_payload, model_name="Lasso")
        
        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
        st.markdown("<h2>Inference Output & Planning Intelligence</h2>", unsafe_allow_html=True)
        
        demand_cat, badge_class, demand_desc = get_demand_category_info(pred_enrollments)
        rounded_enrollments = int(round(pred_enrollments))
        
        # Primary Elevated Prediction Hero Box
        hero_border = theme["accent"]
        st.markdown(
            f"""
            <div style="background-color: {theme['bg_card']}; border: 1px solid {theme['border_card']}; border-left: 4px solid {hero_border}; border-radius: 8px; padding: 1.6rem 2.2rem; margin-bottom: 1.4rem; box-shadow: {theme['shadow_md']};">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.4rem;">
                    <span style="font-size: 0.78rem; font-weight: 700; text-transform: uppercase; color: {theme['text_muted']}; letter-spacing: 0.07em;">
                        Predicted Next-Month Demand
                    </span>
                    <span class="badge {badge_class}" style="font-size: 0.8rem; padding: 0.35rem 0.85rem;">{demand_cat}</span>
                </div>
                <div style="display: flex; align-items: baseline; gap: 1.5rem; margin-bottom: 0.6rem;">
                    <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 2.8rem; font-weight: 800; color: {theme['text_primary']}; letter-spacing: -0.03em;">
                        {rounded_enrollments} enrollments
                    </span>
                    <span style="font-size: 1.1rem; color: {theme['text_muted']}; font-weight: 500;">(Exact: {pred_enrollments:.2f})</span>
                </div>
                <p style="margin: 0; font-size: 0.9rem; color: {theme['text_secondary']};">{demand_desc}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # 5 Structured Micro-Metric Cards
        m1, m2, m3, m4, m5 = st.columns(5)
        with m1:
            st.markdown(render_kpi_card("Course Price", format_currency(in_price), "Configured course fee", icon="🏷️", accent_color=theme["accent"]), unsafe_allow_html=True)
        with m2:
            st.markdown(render_kpi_card("Instructor Rating", f"{in_teacher_rating:.2f} ★", "Quality review score", icon="⭐", accent_color="#F59E0B"), unsafe_allow_html=True)
        with m3:
            st.markdown(render_kpi_card("Instructor Experience", f"{in_teacher_exp:.1f} Yrs", "Tenure in domain", icon="💼", accent_color="#8B5CF6"), unsafe_allow_html=True)
        with m4:
            st.markdown(render_kpi_card("Historical Demand", f"{format_int(in_lag1_enr)} enr.", "Prior month volume", icon="👥", accent_color="#3B82F6"), unsafe_allow_html=True)
        with m5:
            st.markdown(render_kpi_card("Projected Revenue", format_currency(pred_revenue), f"{rounded_enrollments} × {format_currency(in_price)}", icon="💰", accent_color="#10B981"), unsafe_allow_html=True)
            
        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
        
        # Why this prediction? Explanation Section
        st.markdown("<h3>Why this prediction?</h3>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="info-note" style="border-left-color: {theme['accent']};">
                <strong>Feature Contribution Breakdown:</strong><br>
                The following variables contributed directly to the model's forward prediction:
                <ul style="margin-top: 0.5rem; margin-bottom: 0.5rem; padding-left: 1.25rem;">
                    <li><strong>Historical Demand Velocity:</strong> Prior volume (<code>Lag1: {in_lag1_enr:.0f}</code>) and momentum (<code>{in_lag1_enr - in_lag3_enr:+.0f}</code>) establish the primary baseline trajectory.</li>
                    <li><strong>Course Price:</strong> Configured fee of <code>{format_currency(in_price)}</code> applies standard demand elasticity weighting.</li>
                    <li><strong>Course & Instructor Ratings:</strong> Quality metrics (Course: <code>{in_rating:.1f}★</code>, Instructor: <code>{in_teacher_rating:.1f}★</code>) provide positive long-tail learner retention weight.</li>
                    <li><strong>Instructor Experience:</strong> <code>{in_teacher_exp:.1f} years</code> of domain tenure reinforces curriculum credibility for this <code>{in_level}</code> course.</li>
                </ul>
                <span style="font-size: 0.78rem; color: {theme['text_muted']};">
                    * Note: These variables contributed mathematically to the model's inference calculation; this does not establish definitive statistical causation.
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )
