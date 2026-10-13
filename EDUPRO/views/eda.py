"""
EDUPRO - Exploratory Data Analysis & Historical Insights View
Empirical examination of historical course behavior, pricing elasticity,
instructor metrics, and catalog structure.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from utils.theme import get_theme, apply_theme_to_plotly
from utils.data_loader import load_ml_ready_dataset
from utils.metrics import format_currency, format_int


def render_eda(theme_mode: str = "light"):
    theme = get_theme(theme_mode)
    
    st.markdown("<h1>Exploratory Data Analysis & Insights</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p class='page-subtitle'>Empirical investigation of historical course activity, pricing elasticity, and curriculum performance drivers.</p>",
        unsafe_allow_html=True
    )

    df_full = load_ml_ready_dataset()
    if df_full.empty:
        st.warning("Historical dataset is unavailable. Please ensure data files are present.")
        return

    # Filter Bar
    with st.container():
        st.markdown("### Filter Catalog Analytics")
        f_col1, f_col2, f_col3, f_col4 = st.columns(4)
        
        all_categories = sorted(df_full["CourseCategory"].dropna().unique().tolist())
        all_levels = ["All"] + sorted(df_full["CourseLevel"].dropna().unique().tolist())
        all_types = ["All"] + sorted(df_full["CourseType"].dropna().unique().tolist())
        min_p, max_p = float(df_full["CoursePrice"].min()), float(df_full["CoursePrice"].max())
        
        with f_col1:
            selected_categories = st.multiselect(
                "Course Category",
                options=all_categories,
                default=all_categories
            )
        with f_col2:
            selected_level = st.selectbox("Course Level", options=all_levels, index=0)
        with f_col3:
            selected_type = st.selectbox("Course Type", options=all_types, index=0)
        with f_col4:
            price_range = st.slider(
                "Price Range (₹)",
                min_value=int(min_p),
                max_value=int(max_p),
                value=(int(min_p), int(max_p)),
                step=50
            )

    # Apply Filters
    df = df_full.copy()
    if selected_categories:
        df = df[df["CourseCategory"].isin(selected_categories)]
    if selected_level != "All":
        df = df[df["CourseLevel"] == selected_level]
    if selected_type != "All":
        df = df[df["CourseType"] == selected_type]
    df = df[(df["CoursePrice"] >= price_range[0]) & (df["CoursePrice"] <= price_range[1])]

    if df.empty:
        st.warning("No records match the selected filter criteria. Please adjust your filters.")
        return

    st.markdown(f"<p style='color: {theme['text_muted']}; font-size: 0.85rem;'>Displaying <strong>{len(df)}</strong> monthly records across <strong>{df['CourseID'].nunique()}</strong> courses.</p>", unsafe_allow_html=True)
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # 1. Catalog Composition & Category Demand
    st.markdown("<h2>1. Catalog Distribution & Enrollment Demand</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        cat_counts = (
            df.groupby("CourseCategory")["CourseID"]
            .nunique()
            .reset_index(name="CourseCount")
            .sort_values("CourseCount", ascending=True)
        )
        fig1 = px.bar(
            cat_counts,
            y="CourseCategory",
            x="CourseCount",
            orientation="h",
            labels={"CourseCategory": "Category", "CourseCount": "Unique Courses"},
            color_discrete_sequence=[theme["bar_primary"]]
        )
        fig1.update_layout(height=320, title="Unique Courses by Category")
        apply_theme_to_plotly(fig1, theme_mode)
        st.plotly_chart(fig1, use_container_width=True)
        
        st.markdown(
            "<div class='info-note'><strong>Business Takeaway:</strong> Course offerings are balanced across 12 distinct tracks. High technical disciplines form the bedrock of the catalog.</div>",
            unsafe_allow_html=True
        )

    with col2:
        cat_demand = (
            df.groupby("CourseCategory")["EnrollmentCount"]
            .sum()
            .reset_index()
            .sort_values("EnrollmentCount", ascending=True)
        )
        fig2 = px.bar(
            cat_demand,
            y="CourseCategory",
            x="EnrollmentCount",
            orientation="h",
            labels={"CourseCategory": "Category", "EnrollmentCount": "Total Enrollments"},
            color_discrete_sequence=[theme["bar_accent"]]
        )
        fig2.update_layout(height=320, title="Historical Enrollment Demand by Category")
        apply_theme_to_plotly(fig2, theme_mode)
        st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown(
            "<div class='info-note'><strong>Business Takeaway:</strong> Practical career-oriented tracks exhibit the strongest learner acquisition volume.</div>",
            unsafe_allow_html=True
        )

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # 2. Price Elasticity & Ratings Analysis
    st.markdown("<h2>2. Pricing Elasticity & Quality Perception</h2>", unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    
    with col3:
        course_agg = (
            df.groupby(["CourseID", "CourseCategory", "CourseType", "CoursePrice", "CourseRating", "CourseDuration", "AvgTeacherExperience", "AvgTeacherRating"])
            .agg(TotalEnrollment=("EnrollmentCount", "sum"), TotalRevenue=("Revenue", "sum"))
            .reset_index()
        )
        
        fig3 = px.scatter(
            course_agg,
            x="CoursePrice",
            y="TotalEnrollment",
            color="CourseType",
            size="TotalRevenue",
            hover_name="CourseID",
            hover_data={"CourseCategory": True, "CoursePrice": ":.2f", "TotalEnrollment": True, "AvgTeacherExperience": True},
            labels={"CoursePrice": "Course Fee (₹)", "TotalEnrollment": "Cumulative Enrollments"},
            color_discrete_map={"Paid": theme["accent"], "Free": theme["bar_primary"]}
        )
        fig3.update_layout(height=340, title="Course Price vs. Total Enrollments")
        apply_theme_to_plotly(fig3, theme_mode)
        st.plotly_chart(fig3, use_container_width=True)
        
        st.markdown(
            "<div class='info-note'><strong>Business Takeaway:</strong> Course price shows an empirical weak negative relationship with volume, with free courses driving major top-of-funnel intake.</div>",
            unsafe_allow_html=True
        )

    with col4:
        fig4 = px.scatter(
            course_agg,
            x="CourseRating",
            y="TotalEnrollment",
            color="CourseCategory",
            hover_name="CourseID",
            labels={"CourseRating": "Learner Rating (1-5 Stars)", "TotalEnrollment": "Cumulative Enrollments"},
            color_discrete_sequence=theme["series"]
        )
        fig4.update_layout(height=340, title="Course Rating vs. Total Enrollments", showlegend=False)
        apply_theme_to_plotly(fig4, theme_mode)
        st.plotly_chart(fig4, use_container_width=True)
        
        st.markdown(
            "<div class='info-note'><strong>Business Takeaway:</strong> Quality ratings sustain course velocity over time, demonstrating the value of student satisfaction.</div>",
            unsafe_allow_html=True
        )

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # 3. Monthly Trajectories
    st.markdown("<h2>3. Monthly Trajectories (Enrollment & Revenue)</h2>", unsafe_allow_html=True)
    col5, col6 = st.columns(2)
    
    monthly_stats = (
        df.groupby("Month")
        .agg(
            Enrollments=("EnrollmentCount", "sum"),
            Revenue=("Revenue", "sum")
        )
        .reset_index()
    )
    monthly_stats["MonthStr"] = monthly_stats["Month"].dt.strftime("%b %Y")
    
    with col5:
        fig5 = px.line(
            monthly_stats,
            x="MonthStr",
            y="Enrollments",
            markers=True,
            labels={"MonthStr": "Month", "Enrollments": "Platform Enrollments"},
            color_discrete_sequence=[theme["accent"]]
        )
        fig5.update_layout(height=320, title="Monthly Enrollment Trend")
        apply_theme_to_plotly(fig5, theme_mode)
        st.plotly_chart(fig5, use_container_width=True)

    with col6:
        fig6 = px.bar(
            monthly_stats,
            x="MonthStr",
            y="Revenue",
            labels={"MonthStr": "Month", "Revenue": "Platform Revenue (₹)"},
            color_discrete_sequence=[theme["bar_primary"]]
        )
        fig6.update_layout(height=320, title="Monthly Revenue Trend")
        apply_theme_to_plotly(fig6, theme_mode)
        st.plotly_chart(fig6, use_container_width=True)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # 4. Free vs. Paid Performance Breakdown
    st.markdown("<h2>4. Free vs. Paid Monetization Split</h2>", unsafe_allow_html=True)
    fvp_agg = (
        df.groupby("CourseType")
        .agg(
            Courses=("CourseID", "nunique"),
            TotalEnrollments=("EnrollmentCount", "sum"),
            TotalRevenue=("Revenue", "sum")
        )
        .reset_index()
    )
    
    col7, col8 = st.columns(2)
    with col7:
        fig7 = px.pie(
            fvp_agg,
            names="CourseType",
            values="TotalEnrollments",
            title="Enrollment Volume by Course Type",
            color="CourseType",
            color_discrete_map={"Paid": theme["accent"], "Free": theme["bar_primary"]},
            hole=0.45
        )
        fig7.update_layout(height=300)
        apply_theme_to_plotly(fig7, theme_mode)
        st.plotly_chart(fig7, use_container_width=True)

    with col8:
        fig8 = px.bar(
            fvp_agg,
            x="CourseType",
            y="TotalRevenue",
            title="Revenue Contribution by Course Type",
            labels={"CourseType": "Course Type", "TotalRevenue": "Revenue (₹)"},
            color_discrete_sequence=[theme["bar_accent"]]
        )
        fig8.update_layout(height=300)
        apply_theme_to_plotly(fig8, theme_mode)
        st.plotly_chart(fig8, use_container_width=True)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # 5. Detailed Course Table
    st.markdown("<h2>5. Course-Level Empirical Summary</h2>", unsafe_allow_html=True)
    
    display_table = course_agg[[
        "CourseID", "CourseCategory", "CourseType", "CoursePrice", "CourseRating",
        "AvgTeacherExperience", "AvgTeacherRating", "TotalEnrollment", "TotalRevenue"
    ]].copy()
    display_table.columns = [
        "Course ID", "Category", "Type", "Price (₹)", "Rating",
        "Instructor Exp (Yrs)", "Instructor Rating", "Total Enrollments", "Total Revenue (₹)"
    ]
    display_table["Price (₹)"] = display_table["Price (₹)"].apply(lambda x: format_currency(x))
    display_table["Total Revenue (₹)"] = display_table["Total Revenue (₹)"].apply(lambda x: format_currency(x))
    display_table["Total Enrollments"] = display_table["Total Enrollments"].apply(lambda x: format_int(x))
    display_table["Rating"] = display_table["Rating"].apply(lambda x: f"{x:.2f} ★")
    display_table["Instructor Rating"] = display_table["Instructor Rating"].apply(lambda x: f"{x:.2f} ★")
    
    st.dataframe(
        display_table.sort_values("Total Enrollments", ascending=False),
        use_container_width=True,
        hide_index=True
    )
