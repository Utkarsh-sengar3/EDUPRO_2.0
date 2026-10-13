"""
EDUPRO - Overview View
Executive KPI cockpit, monthly demand & revenue outlook,
category revenue distribution, and dynamic business signals.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from utils.theme import get_theme, apply_theme_to_plotly
from utils.data_loader import (
    load_ml_ready_dataset,
    load_test_forecast_detail,
    load_category_forecasts,
    load_free_vs_paid,
    load_model_results
)
from utils.metrics import (
    format_currency,
    format_int,
    render_kpi_card,
    render_signal_card
)


def render_overview(theme_mode: str = "light"):
    theme = get_theme(theme_mode)
    
    # Header Bar with Live Badge
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.35rem;">
            <div>
                <h1>EduPro Predictive Intelligence</h1>
                <div class="page-subtitle">Course Demand & Revenue Forecasting Cockpit</div>
            </div>
            <div style="display: flex; gap: 8px;">
                <span class="badge badge-moderate" style="font-size: 0.76rem; padding: 0.35rem 0.75rem;">⚡ LIVE PREDICTIVE ENGINE</span>
                <span class="badge badge-low" style="font-size: 0.76rem; padding: 0.35rem 0.75rem;">HORIZON: Q4 2025</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Modern Executive Hero Banner
    st.markdown(
        """
        <div class="hero-box">
            <div class="hero-kicker">✦ AI-powered education intelligence</div>
            <h2>Turn historical course activity into forward-looking planning intelligence.</h2>
            <p>Empower educational leadership to forecast upcoming enrollment demand, optimize catalog pricing elasticity, and proactively project revenue trajectory with regularized machine learning pipelines.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Quick navigation — clickable product modules
    st.markdown("<div style='font-size:.68rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:" + theme["text_muted"] + ";margin:.25rem 0 .55rem;'>EXPLORE EDUPRO</div>", unsafe_allow_html=True)
    q1, q2, q3, q4 = st.columns(4)
    quick = [
        (q1, "◎", "Demand Prediction", "Forecast upcoming enrollment demand", "◎ Demand Prediction"),
        (q2, "₹", "Revenue Forecast", "Project course & category revenue", "₹ Revenue Forecast"),
        (q3, "▦", "Category Intelligence", "Compare portfolio performance", "▦ Category Analysis"),
        (q4, "ϟ", "Model Intelligence", "Understand accuracy & drivers", "ϟ Model Performance"),
    ]
    for col, icon, title, desc, target in quick:
        with col:
            if st.button(f"{icon}  {title}", key="quick_" + title.replace(" ", "_"), use_container_width=True):
                st.session_state["current_page"] = target
                st.rerun()
            st.caption(desc)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # Load core datasets
    ml_df = load_ml_ready_dataset()
    test_df = load_test_forecast_detail()
    cat_df = load_category_forecasts()
    fvp_df = load_free_vs_paid()
    model_res_df = load_model_results()
    
    if ml_df.empty:
        st.warning("Master dataset not available. Please verify the project data directory.")
        return

    # Calculate High-Level KPIs
    total_courses = ml_df["CourseID"].nunique()
    total_historical_enrollments = ml_df["EnrollmentCount"].sum()
    total_historical_revenue = ml_df["Revenue"].sum()
    
    if not test_df.empty:
        forecasted_enrollment = test_df["PredictedEnrollments"].sum()
        forecasted_revenue = test_df["PredictedRevenue"].sum()
    else:
        forecasted_enrollment = 0
        forecasted_revenue = 0

    # Display 5 KPI Cards in responsive columns with top accents and icons
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(render_kpi_card("Total Courses", format_int(total_courses), "Catalog portfolio size", icon="📚", accent_color=theme["accent"]), unsafe_allow_html=True)
    with col2:
        st.markdown(render_kpi_card("Total Enrollments", format_int(total_historical_enrollments), "Historical total volume", icon="👥", accent_color="#6366F1"), unsafe_allow_html=True)
    with col3:
        st.markdown(render_kpi_card("Historical Revenue", format_currency(total_historical_revenue), "Total earned to date", icon="💰", accent_color="#10B981"), unsafe_allow_html=True)
    with col4:
        st.markdown(render_kpi_card("Forecasted Demand", format_int(forecasted_enrollment), "Test period predicted demand", icon="📈", accent_color="#8B5CF6"), unsafe_allow_html=True)
    with col5:
        st.markdown(render_kpi_card("Forecasted Revenue", format_currency(forecasted_revenue), "Test period projected revenue", icon="💎", accent_color="#F59E0B"), unsafe_allow_html=True)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # 2-Column Analytics Layout
    row2_left, row2_right = st.columns([3, 2])
    
    with row2_left:
        st.markdown("<h2>Demand Outlook: Actual vs. Forecasted</h2>", unsafe_allow_html=True)
        
        monthly_trend = (
            ml_df.groupby("Month")
            .agg(
                ActualEnrollment=("EnrollmentCount", "sum"),
                ActualRevenue=("Revenue", "sum")
            )
            .reset_index()
        )
        
        if not test_df.empty:
            test_monthly = (
                test_df.groupby("Month")
                .agg(
                    PredictedEnrollment=("PredictedEnrollments", "sum"),
                    PredictedRevenue=("PredictedRevenue", "sum")
                )
                .reset_index()
            )
            trend_merged = pd.merge(monthly_trend, test_monthly, on="Month", how="left")
        else:
            trend_merged = monthly_trend
            trend_merged["PredictedEnrollment"] = np.nan
            trend_merged["PredictedRevenue"] = np.nan
            
        trend_merged["MonthStr"] = trend_merged["Month"].dt.strftime("%b %Y")
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Bar(
            x=trend_merged["MonthStr"],
            y=trend_merged["ActualEnrollment"],
            name="Actual Enrollments",
            marker_color=theme["bar_primary"],
            opacity=0.9
        ))
        
        pred_sub = trend_merged.dropna(subset=["PredictedEnrollment"])
        if not pred_sub.empty:
            fig_trend.add_trace(go.Scatter(
                x=pred_sub["MonthStr"],
                y=pred_sub["PredictedEnrollment"],
                name="Predicted Enrollments",
                mode="lines+markers",
                line=dict(color=theme["accent"], width=3, dash="dash"),
                marker=dict(size=8, color=theme["accent"], symbol="diamond")
            ))
            
        fig_trend.update_layout(
            height=350,
            yaxis_title="Monthly Enrollment Volume",
            xaxis_title="",
            barmode="group",
            margin=dict(l=40, r=20, t=30, b=40)
        )
        apply_theme_to_plotly(fig_trend, theme_mode)
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with row2_right:
        st.markdown("<h2>Revenue by Category</h2>", unsafe_allow_html=True)
        
        if not cat_df.empty:
            cat_sorted = cat_df.sort_values("PredictedRevenue", ascending=True)
            fig_cat = go.Figure()
            fig_cat.add_trace(go.Bar(
                y=cat_sorted["CourseCategory"],
                x=cat_sorted["PredictedRevenue"],
                name="Projected Revenue",
                orientation="h",
                marker_color=theme["accent"]
            ))
            fig_cat.update_layout(
                height=350,
                xaxis_title="Predicted Revenue (₹)",
                yaxis_title="",
                margin=dict(l=10, r=20, t=30, b=40)
            )
            apply_theme_to_plotly(fig_cat, theme_mode)
            st.plotly_chart(fig_cat, use_container_width=True)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # Dynamic Business Signals
    st.markdown("<h2>Portfolio Intelligence & Dynamic Signals</h2>", unsafe_allow_html=True)
    
    signals_col1, signals_col2 = st.columns(2)
    
    if not cat_df.empty:
        top_rev_cat = cat_df.sort_values("PredictedRevenue", ascending=False).iloc[0]
        top_enr_cat = cat_df.sort_values("PredictedEnrollments", ascending=False).iloc[0]
        
        with signals_col1:
            st.markdown(
                render_signal_card(
                    f"Top Revenue Driver: {top_rev_cat['CourseCategory']}",
                    f"Projected to generate <strong>{format_currency(top_rev_cat['PredictedRevenue'])}</strong> with an average course fee of {format_currency(top_rev_cat['AvgCoursePrice'])}. Represents the primary monetization pillar.",
                    border_color=theme["success"],
                    icon="💰"
                ),
                unsafe_allow_html=True
            )
            
            st.markdown(
                render_signal_card(
                    f"Highest Enrollment Demand: {top_enr_cat['CourseCategory']}",
                    f"Estimated at <strong>{format_int(top_enr_cat['PredictedEnrollments'])} learner enrollments</strong> across the evaluation horizon, leading all tracks in student acquisition.",
                    border_color=theme["accent"],
                    icon="📈"
                ),
                unsafe_allow_html=True
            )
            
    with signals_col2:
        if not fvp_df.empty:
            free_row = fvp_df[fvp_df["CourseType"] == "Free"]
            paid_row = fvp_df[fvp_df["CourseType"] == "Paid"]
            
            free_enr = free_row["PredictedEnrollments"].values[0] if not free_row.empty else 0
            paid_enr = paid_row["PredictedEnrollments"].values[0] if not paid_row.empty else 0
            total_pred = free_enr + paid_enr
            free_pct = (free_enr / total_pred * 100) if total_pred > 0 else 0
            
            st.markdown(
                render_signal_card(
                    "Free-to-Paid Acquisition Funnel",
                    f"Free courses generate <strong>{free_pct:.1f}% of total predicted demand</strong> ({format_int(free_enr)} learners), serving as the student acquisition feeder for {format_int(paid_enr)} paid enrollments.",
                    border_color=theme["info"],
                    icon="🔄"
                ),
                unsafe_allow_html=True
            )
            
        best_model_name = "Lasso Regularized Pipeline"
        best_mae = "2.99"
        if not model_res_df.empty:
            best_mae = f"{model_res_df.iloc[0]['MAE']:.2f}"
            best_model_name = str(model_res_df.iloc[0]['Model'])
            
        st.markdown(
            render_signal_card(
                f"Model Health Status: {best_model_name}",
                f"Operational pipeline bounds out-of-time test MAE to <strong>{best_mae} enrollments/course</strong>. Successfully categorizes courses into high, moderate, and low demand tiers.",
                border_color=theme["warning"],
                icon="🛡️"
            ),
            unsafe_allow_html=True
        )
