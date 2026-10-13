"""
EDUPRO - Category Analysis View
Category intelligence scorecard, comparative demand evaluation,
and interactive category drill-down inspector.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from utils.theme import get_theme, apply_theme_to_plotly
from utils.data_loader import (
    load_category_forecasts,
    load_ml_ready_dataset
)
from utils.metrics import (
    format_currency,
    format_int,
    render_kpi_card
)


def render_category_analysis(theme_mode: str = "light"):
    theme = get_theme(theme_mode)
    
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.35rem;">
            <div>
                <h1>Category Intelligence & Portfolio Breakdown</h1>
                <div class="page-subtitle">Comparative demand evaluation, monetization efficiency, and track-level performance diagnostics.</div>
            </div>
            <div>
                <span class="badge badge-moderate" style="font-size: 0.76rem; padding: 0.35rem 0.75rem;">📑 12 CURRICULUM TRACKS</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    cat_df = load_category_forecasts()
    ml_df = load_ml_ready_dataset()

    if cat_df.empty:
        st.warning("Category forecast dataset is not available.")
        return

    # Visualizations
    st.markdown("<h2>1. Cross-Category Demand & Revenue Comparison</h2>", unsafe_allow_html=True)
    
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        cat_enr_sorted = cat_df.sort_values("PredictedEnrollments", ascending=True)
        fig_enr = go.Figure()
        fig_enr.add_trace(go.Bar(
            y=cat_enr_sorted["CourseCategory"],
            x=cat_enr_sorted["PredictedEnrollments"],
            orientation="h",
            name="Forecasted Demand",
            marker_color=theme["accent"]
        ))
        fig_enr.update_layout(
            height=360,
            title="Forecasted Enrollment Demand by Category",
            xaxis_title="Predicted Enrollments",
            yaxis_title=""
        )
        apply_theme_to_plotly(fig_enr, theme_mode)
        st.plotly_chart(fig_enr, use_container_width=True)

    with col_c2:
        cat_rev_sorted = cat_df.sort_values("PredictedRevenue", ascending=True)
        fig_rev = go.Figure()
        fig_rev.add_trace(go.Bar(
            y=cat_rev_sorted["CourseCategory"],
            x=cat_rev_sorted["PredictedRevenue"],
            orientation="h",
            name="Projected Revenue",
            marker_color=theme["bar_primary"]
        ))
        fig_rev.update_layout(
            height=360,
            title="Projected Revenue by Category (₹)",
            xaxis_title="Predicted Revenue (₹)",
            yaxis_title=""
        )
        apply_theme_to_plotly(fig_rev, theme_mode)
        st.plotly_chart(fig_rev, use_container_width=True)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # Category Scorecard Table
    st.markdown("<h2>2. Category Performance Scorecard</h2>", unsafe_allow_html=True)
    
    course_counts = ml_df.groupby("CourseCategory")["CourseID"].nunique().to_dict() if not ml_df.empty else {}
    
    scorecard_df = cat_df.copy()
    scorecard_df["Courses"] = scorecard_df["CourseCategory"].map(course_counts).fillna(5).astype(int)
    
    display_scorecard = scorecard_df[[
        "CourseCategory", "Courses", "ActualEnrollments", "PredictedEnrollments",
        "ActualRevenue", "PredictedRevenue", "AvgCoursePrice", "RevenueVariance"
    ]].copy()
    
    display_scorecard.columns = [
        "Category", "Courses", "Actual Demand", "Predicted Demand",
        "Actual Revenue (₹)", "Predicted Revenue (₹)", "Avg Price (₹)", "Revenue Variance (₹)"
    ]
    
    # Download Button
    csv_bytes = display_scorecard.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Category Report",
        data=csv_bytes,
        file_name="EduPro_Category_Performance_Report.csv",
        mime="text/csv"
    )
    
    # Format table for visual presentation
    fmt_scorecard = display_scorecard.copy()
    fmt_scorecard["Actual Demand"] = fmt_scorecard["Actual Demand"].apply(lambda x: format_int(x))
    fmt_scorecard["Predicted Demand"] = fmt_scorecard["Predicted Demand"].apply(lambda x: format_int(x))
    fmt_scorecard["Actual Revenue (₹)"] = fmt_scorecard["Actual Revenue (₹)"].apply(lambda x: format_currency(x))
    fmt_scorecard["Predicted Revenue (₹)"] = fmt_scorecard["Predicted Revenue (₹)"].apply(lambda x: format_currency(x))
    fmt_scorecard["Avg Price (₹)"] = fmt_scorecard["Avg Price (₹)"].apply(lambda x: format_currency(x))
    fmt_scorecard["Revenue Variance (₹)"] = fmt_scorecard["Revenue Variance (₹)"].apply(lambda x: format_currency(x))
    
    st.dataframe(fmt_scorecard, use_container_width=True, hide_index=True)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # 3. Interactive Category Drilldown Inspector
    st.markdown("<h2>3. Category Drill-Down Inspector</h2>", unsafe_allow_html=True)
    
    cat_list = sorted(cat_df["CourseCategory"].unique().tolist())
    selected_cat = st.selectbox("Select Track to Inspect", options=cat_list, index=0)
    
    cat_meta_df = ml_df[ml_df["CourseCategory"] == selected_cat] if not ml_df.empty else pd.DataFrame()
    cat_summary = cat_df[cat_df["CourseCategory"] == selected_cat].iloc[0]
    
    i1, i2, i3, i4 = st.columns(4)
    with i1:
        st.markdown(
            render_kpi_card("Courses in Track", format_int(cat_meta_df["CourseID"].nunique() if not cat_meta_df.empty else 0), "Curriculum size", icon="📚", accent_color=theme["accent"]),
            unsafe_allow_html=True
        )
    with i2:
        avg_pr = cat_meta_df["CoursePrice"].mean() if not cat_meta_df.empty else cat_summary["AvgCoursePrice"]
        st.markdown(
            render_kpi_card("Average Track Price", format_currency(avg_pr), "Mean catalog fee", icon="🏷️", accent_color="#10B981"),
            unsafe_allow_html=True
        )
    with i3:
        avg_rt = cat_meta_df["CourseRating"].mean() if not cat_meta_df.empty else 4.5
        st.markdown(
            render_kpi_card("Average Course Rating", f"{avg_rt:.2f} ★", "Student satisfaction", icon="⭐", accent_color="#F59E0B"),
            unsafe_allow_html=True
        )
    with i4:
        st.markdown(
            render_kpi_card("Predicted Revenue", format_currency(cat_summary["PredictedRevenue"]), "Track projected earnings", icon="💰", accent_color="#8B5CF6"),
            unsafe_allow_html=True
        )

    # Nested Courses Table
    if not cat_meta_df.empty:
        st.markdown("#### Courses in this Track")
        nested_courses = (
            cat_meta_df.groupby(["CourseID", "CourseType", "CourseLevel", "CoursePrice", "CourseRating", "CourseDuration", "AvgTeacherExperience", "AvgTeacherRating"])
            .agg(TotalHistoricalEnrollments=("EnrollmentCount", "sum"), TotalHistoricalRevenue=("Revenue", "sum"))
            .reset_index()
        )
        nested_courses.columns = [
            "Course ID", "Type", "Level", "Price (₹)", "Rating", "Duration (hrs)", "Instructor Exp (Yrs)", "Instructor Rating", "Historical Enrollments", "Historical Revenue (₹)"
        ]
        nested_courses["Price (₹)"] = nested_courses["Price (₹)"].apply(lambda x: format_currency(x))
        nested_courses["Historical Revenue (₹)"] = nested_courses["Historical Revenue (₹)"].apply(lambda x: format_currency(x))
        nested_courses["Historical Enrollments"] = nested_courses["Historical Enrollments"].apply(lambda x: format_int(x))
        nested_courses["Rating"] = nested_courses["Rating"].apply(lambda x: f"{x:.2f} ★")
        nested_courses["Instructor Rating"] = nested_courses["Instructor Rating"].apply(lambda x: f"{x:.2f} ★")
        
        st.dataframe(nested_courses, use_container_width=True, hide_index=True)
