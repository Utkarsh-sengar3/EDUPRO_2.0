"""
EDUPRO - Model Performance & Validation View
Rigorous empirical evaluation of machine learning candidates on out-of-time validation splits,
residual diagnostics, and transparent disclosure of model capabilities and limitations.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from utils.theme import get_theme, apply_theme_to_plotly
from utils.data_loader import (
    load_model_results,
    load_test_forecast_detail
)
from utils.metrics import format_decimal, render_kpi_card


def render_model_performance(theme_mode: str = "light"):
    theme = get_theme(theme_mode)
    
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.35rem;">
            <div>
                <h1>Model Validation & Diagnostics</h1>
                <div class="page-subtitle">Rigorous empirical evaluation of ML algorithms on chronological out-of-time test splits.</div>
            </div>
            <div>
                <span class="badge badge-warning" style="font-size: 0.76rem; padding: 0.35rem 0.75rem;">🛡️ EMPIRICAL BENCHMARK</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Scientific Transparency Disclosure Box
    st.markdown(
        f"""
        <div class="info-note" style="border-left: 3px solid {theme['warning']};">
            <strong>Scientific Disclosure & Validation Methodology:</strong><br>
            The models were evaluated strictly using an out-of-time <strong>chronological validation split</strong> (Training: April 2025 – August 2025; Testing: September 2025 – November 2025) to prevent future data leakage. 
            On this out-of-time test set, the demand model's \(R^2\) remains slightly negative (\(-0.10\)), reflecting high short-term volatility relative to the 8-month panel depth. However, the regularized linear model (Lasso) successfully bounds the Mean Absolute Error to \(\\sim 2.99\) enrollments per course, providing reliable directional demand tiering (Low, Moderate, High) for operational planning.
        </div>
        """,
        unsafe_allow_html=True
    )

    model_res_df = load_model_results()
    test_df = load_test_forecast_detail()

    if model_res_df.empty:
        st.warning("Model evaluation metrics not available.")
        return

    # High-level evaluation KPIs
    best_row = model_res_df.sort_values("RMSE").iloc[0]
    
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(
            render_kpi_card("Production Model", str(best_row["Model"]), "Regularized L1 pipeline", icon="🏆", accent_color=theme["accent"]),
            unsafe_allow_html=True
        )
    with k2:
        st.markdown(
            render_kpi_card("Test MAE", f"{best_row['MAE']:.3f}", "Mean absolute enrollment error", icon="🎯", accent_color="#10B981"),
            unsafe_allow_html=True
        )
    with k3:
        st.markdown(
            render_kpi_card("Test RMSE", f"{best_row['RMSE']:.3f}", "Root mean squared error", icon="📐", accent_color="#F59E0B"),
            unsafe_allow_html=True
        )
    with k4:
        st.markdown(
            render_kpi_card("Test R² Score", f"{best_row['R2']:.3f}", "Out-of-time generalization", icon="📊", accent_color="#EF4444"),
            unsafe_allow_html=True
        )

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # 1. Multi-Model Benchmark Comparison Table
    st.markdown("<h2>1. Algorithm Benchmark Matrix</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: {theme['text_muted']}; font-size: 0.85rem;'>Performance metrics evaluated strictly on unseen test period data (180 out-of-time course-month records).</p>", unsafe_allow_html=True)
    
    display_model_df = model_res_df.copy()
    display_model_df.columns = ["Algorithm", "MAE (Enrollments)", "RMSE (Enrollments)", "R² Score"]
    display_model_df["MAE (Enrollments)"] = display_model_df["MAE (Enrollments)"].apply(lambda x: f"{x:.4f}")
    display_model_df["RMSE (Enrollments)"] = display_model_df["RMSE (Enrollments)"].apply(lambda x: f"{x:.4f}")
    display_model_df["R² Score"] = display_model_df["R² Score"].apply(lambda x: f"{x:.4f}")
    
    st.dataframe(display_model_df, use_container_width=True, hide_index=True)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # 2. Visual Comparison
    st.markdown("<h2>2. Candidate Model Benchmark Comparison</h2>", unsafe_allow_html=True)
    col_m1, col_m2 = st.columns(2)
    
    with col_m1:
        fig_mae = px.bar(
            model_res_df.sort_values("MAE"),
            x="Model",
            y="MAE",
            title="Mean Absolute Error (Lower is Better)",
            labels={"MAE": "MAE (Enrollments)", "Model": "Model"},
            color_discrete_sequence=[theme["accent"]]
        )
        fig_mae.update_layout(height=320)
        apply_theme_to_plotly(fig_mae, theme_mode)
        st.plotly_chart(fig_mae, use_container_width=True)

    with col_m2:
        fig_rmse = px.bar(
            model_res_df.sort_values("RMSE"),
            x="Model",
            y="RMSE",
            title="Root Mean Squared Error (Lower is Better)",
            labels={"RMSE": "RMSE (Enrollments)", "Model": "Model"},
            color_discrete_sequence=[theme["bar_primary"]]
        )
        fig_rmse.update_layout(height=320)
        apply_theme_to_plotly(fig_rmse, theme_mode)
        st.plotly_chart(fig_rmse, use_container_width=True)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # 3. Residual Diagnostics
    if not test_df.empty:
        st.markdown("<h2>3. Residual Diagnostics & Fit Alignment</h2>", unsafe_allow_html=True)
        col_d1, col_d2 = st.columns(2)
        
        y_act = test_df["Target_NextMonthEnrollments"]
        y_pred = test_df["PredictedEnrollments"]
        residuals = y_act - y_pred
        
        with col_d1:
            min_val = min(y_act.min(), y_pred.min())
            max_val = max(y_act.max(), y_pred.max())
            
            fig_scat = go.Figure()
            fig_scat.add_trace(go.Scatter(
                x=y_act,
                y=y_pred,
                mode="markers",
                marker=dict(color=theme["accent"], size=7, opacity=0.75),
                name="Test Observations",
                hovertext=test_df["CourseID"]
            ))
            fig_scat.add_trace(go.Scatter(
                x=[min_val, max_val],
                y=[min_val, max_val],
                mode="lines",
                line=dict(color=theme["danger"], dash="dash", width=2),
                name="Ideal Fit (y = x)"
            ))
            fig_scat.update_layout(
                height=340,
                title="Actual vs. Predicted Enrollments",
                xaxis_title="Actual Next-Month Enrollments",
                yaxis_title="Predicted Next-Month Enrollments"
            )
            apply_theme_to_plotly(fig_scat, theme_mode)
            st.plotly_chart(fig_scat, use_container_width=True)
            
        with col_d2:
            fig_hist = px.histogram(
                x=residuals,
                nbins=25,
                title="Residual Error Distribution (Actual - Predicted)",
                labels={"x": "Residual Error (Enrollments)"},
                color_discrete_sequence=[theme["bar_primary"]]
            )
            fig_hist.add_vline(x=0, line_width=2, line_dash="dash", line_color=theme["danger"])
            fig_hist.update_layout(height=340, yaxis_title="Frequency")
            apply_theme_to_plotly(fig_hist, theme_mode)
            st.plotly_chart(fig_hist, use_container_width=True)
