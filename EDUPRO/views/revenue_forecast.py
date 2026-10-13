"""
EDUPRO - Revenue Forecast View
Financial modeling, scenario simulation, pricing sensitivity analysis,
and course-level revenue variance reporting.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from utils.theme import get_theme, apply_theme_to_plotly
from utils.data_loader import (
    load_test_forecast_detail,
    load_category_forecasts,
    load_course_forecasts,
    load_free_vs_paid
)
from utils.metrics import (
    format_currency,
    format_int,
    render_kpi_card
)
from utils.forecasting import run_scenario_forecast


def render_revenue_forecast(theme_mode: str = "light"):
    theme = get_theme(theme_mode)
    
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.35rem;">
            <div>
                <h1>Revenue Forecast & Portfolio Modeling</h1>
                <div class="page-subtitle">Evaluate forecasted financial performance across courses and categories under baseline and scenario conditions.</div>
            </div>
            <div>
                <span class="badge badge-high" style="font-size: 0.76rem; padding: 0.35rem 0.75rem;">💰 FINANCIAL SIMULATOR</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Core Formula Callout Box
    st.markdown(
        f"""
        <div class="info-note" style="border-left: 3px solid {theme['accent']};">
            <strong>Revenue Forecasting Methodology:</strong><br>
            <code>Predicted Revenue = Predicted Enrollment × Course Price</code><br>
            <span style="font-size: 0.8rem; color: {theme['text_muted']};">
                Revenue projections are derived directly from predicted course enrollment volume multiplied by configured course fees.
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    test_detail_df = load_test_forecast_detail()
    course_rev_df = load_course_forecasts()
    cat_rev_df = load_category_forecasts()
    fvp_df = load_free_vs_paid()

    if test_detail_df.empty and course_rev_df.empty:
        st.warning("Forecast dataset not available. Please verify model outputs.")
        return

    # Scenario Modeling Controls Card
    st.markdown("### Interactive Scenario Simulation")
    sim_c1, sim_c2, sim_c3 = st.columns(3)
    
    with sim_c1:
        price_adjust_pct = st.slider(
            "Pricing Adjustment (%)",
            min_value=-50,
            max_value=100,
            value=0,
            step=5,
            help="Simulate increasing or decreasing catalog pricing."
        )
    with sim_c2:
        demand_shock_pct = st.slider(
            "Demand Sensitivity (%)",
            min_value=-50,
            max_value=100,
            value=0,
            step=5,
            help="Simulate macro demand shifts or market expansions."
        )
    with sim_c3:
        cat_filter = st.selectbox(
            "Filter Track",
            options=["All Categories"] + sorted(test_detail_df["CourseCategory"].dropna().unique().tolist())
        )

    # Filter & run scenario
    active_df = test_detail_df.copy()
    if cat_filter != "All Categories":
        active_df = active_df[active_df["CourseCategory"] == cat_filter]

    price_factor = 1.0 + (price_adjust_pct / 100.0)
    sim_df = run_scenario_forecast(active_df, price_factor=price_factor, demand_shock=demand_shock_pct)

    # Calculate Totals
    baseline_enrollment = active_df["PredictedEnrollments"].sum()
    baseline_revenue = active_df["PredictedRevenue"].sum()
    sim_enrollment = sim_df["SimulatedEnrollments"].sum()
    sim_revenue = sim_df["SimulatedRevenue"].sum()
    actual_revenue = active_df["ActualRevenue"].sum() if "ActualRevenue" in active_df.columns else 0

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # KPI Summary Cards with top accents
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(
            render_kpi_card(
                "Simulated Demand",
                format_int(sim_enrollment),
                f"Baseline: {format_int(baseline_enrollment)} enr.",
                icon="👥",
                accent_color=theme["accent"]
            ),
            unsafe_allow_html=True
        )
    with k2:
        st.markdown(
            render_kpi_card(
                "Simulated Revenue",
                format_currency(sim_revenue),
                f"Baseline: {format_currency(baseline_revenue)}",
                icon="💰",
                accent_color="#10B981"
            ),
            unsafe_allow_html=True
        )
    with k3:
        rev_diff = sim_revenue - baseline_revenue
        diff_label = f"+{format_currency(rev_diff)}" if rev_diff >= 0 else f"-{format_currency(abs(rev_diff))}"
        st.markdown(
            render_kpi_card(
                "Scenario Delta",
                diff_label,
                f"{((sim_revenue/baseline_revenue - 1)*100 if baseline_revenue > 0 else 0):+.1f}% vs baseline",
                icon="⚡",
                accent_color="#F59E0B"
            ),
            unsafe_allow_html=True
        )
    with k4:
        st.markdown(
            render_kpi_card(
                "Recorded Actual Revenue",
                format_currency(actual_revenue),
                "Historical test baseline",
                icon="🏛️",
                accent_color="#6366F1"
            ),
            unsafe_allow_html=True
        )

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # Visualizations
    st.markdown("<h2>1. Category Revenue Distribution (Actual vs. Forecast)</h2>", unsafe_allow_html=True)
    
    col_v1, col_v2 = st.columns([3, 2])
    
    with col_v1:
        if not cat_rev_df.empty:
            cat_plot_df = cat_rev_df.sort_values("PredictedRevenue", ascending=False)
            
            fig_cat_rev = go.Figure()
            fig_cat_rev.add_trace(go.Bar(
                x=cat_plot_df["CourseCategory"],
                y=cat_plot_df["ActualRevenue"],
                name="Actual Revenue",
                marker_color=theme["bar_primary"]
            ))
            fig_cat_rev.add_trace(go.Bar(
                x=cat_plot_df["CourseCategory"],
                y=cat_plot_df["PredictedRevenue"],
                name="Predicted Revenue",
                marker_color=theme["accent"]
            ))
            fig_cat_rev.update_layout(
                height=340,
                title="Category Revenue: Actual vs. Forecasted",
                xaxis_title="",
                yaxis_title="Total Revenue (₹)",
                barmode="group",
                xaxis_tickangle=-30
            )
            apply_theme_to_plotly(fig_cat_rev, theme_mode)
            st.plotly_chart(fig_cat_rev, use_container_width=True)

    with col_v2:
        if not fvp_df.empty:
            fig_fvp = px.bar(
                fvp_df,
                x="CourseType",
                y=["ActualRevenue", "PredictedRevenue"],
                barmode="group",
                title="Monetization by Course Type",
                labels={"value": "Revenue (₹)", "CourseType": "Course Type", "variable": "Metric"},
                color_discrete_map={"ActualRevenue": theme["bar_primary"], "PredictedRevenue": theme["accent"]}
            )
            fig_fvp.update_layout(height=340)
            apply_theme_to_plotly(fig_fvp, theme_mode)
            st.plotly_chart(fig_fvp, use_container_width=True)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # Granular Course-Level Revenue Forecast Table
    st.markdown("<h2>2. Course-Level Revenue Forecast Table</h2>", unsafe_allow_html=True)
    
    course_display = (
        sim_df.groupby(["CourseID", "CourseCategory", "CourseLevel"])
        .agg(
            CoursePrice=("SimulatedPrice", "mean"),
            PredictedEnrollments=("SimulatedEnrollments", "sum"),
            PredictedRevenue=("SimulatedRevenue", "sum"),
            ActualRevenue=("ActualRevenue", "sum")
        )
        .reset_index()
    )
    course_display["RevenueVariance"] = course_display["PredictedRevenue"] - course_display["ActualRevenue"]
    
    table_df = course_display.copy()
    table_df.columns = [
        "Course ID", "Category", "Level", "Price (₹)",
        "Predicted Demand", "Forecasted Revenue (₹)", "Actual Revenue (₹)", "Variance (₹)"
    ]
    
    # Download Button for CSV
    csv_data = table_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Forecast CSV",
        data=csv_data,
        file_name="EduPro_Course_Revenue_Forecast.csv",
        mime="text/csv"
    )
    
    # Format table columns
    formatted_table = table_df.copy()
    formatted_table["Price (₹)"] = formatted_table["Price (₹)"].apply(lambda x: format_currency(x))
    formatted_table["Predicted Demand"] = formatted_table["Predicted Demand"].apply(lambda x: format_int(x))
    formatted_table["Forecasted Revenue (₹)"] = formatted_table["Forecasted Revenue (₹)"].apply(lambda x: format_currency(x))
    formatted_table["Actual Revenue (₹)"] = formatted_table["Actual Revenue (₹)"].apply(lambda x: format_currency(x))
    formatted_table["Variance (₹)"] = formatted_table["Variance (₹)"].apply(lambda x: format_currency(x))
    
    st.dataframe(
        formatted_table.sort_values("Forecasted Revenue (₹)", ascending=False),
        use_container_width=True,
        hide_index=True
    )
