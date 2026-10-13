"""
EDUPRO - Feature Importance & Interpretability View
Variable contribution analysis, model weights, and causal demarcation.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from utils.theme import get_theme, apply_theme_to_plotly
from utils.data_loader import load_feature_importance


def render_feature_importance(theme_mode: str = "light"):
    theme = get_theme(theme_mode)
    
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.35rem;">
            <div>
                <h1>Feature Importance & Interpretability</h1>
                <div class="page-subtitle">Quantifying the predictive contribution of course attributes, instructor profiles, and historical velocity signals.</div>
            </div>
            <div>
                <span class="badge badge-high" style="font-size: 0.76rem; padding: 0.35rem 0.75rem;">🧬 MODEL INTERPRETABILITY</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    feat_df = load_feature_importance()
    if feat_df.empty:
        st.warning("Feature importance artifact not available.")
        return

    # Clean feature names
    feat_display = feat_df.copy()
    feat_display["CleanFeature"] = (
        feat_display["Feature"]
        .str.replace("num__", "", regex=False)
        .str.replace("cat__", "", regex=False)
        .str.replace("CourseCategory_", "Category: ", regex=False)
        .str.replace("CourseLevel_", "Level: ", regex=False)
        .str.replace("CourseType_", "Type: ", regex=False)
        .str.replace("DurationBucket_", "Duration: ", regex=False)
        .str.replace("AvgTeacherExperience", "Instructor Experience (Yrs)", regex=False)
        .str.replace("AvgTeacherRating", "Instructor Rating", regex=False)
    )

    # Top N selection controls
    ctrl_col1, ctrl_col2 = st.columns([2, 2])
    with ctrl_col1:
        top_n = st.radio("Display Depth", options=[10, 15, 20, len(feat_display)], format_func=lambda x: f"Top {x} Features" if x < len(feat_display) else "All Features", horizontal=True)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # Horizontal Bar Chart
    top_features = feat_display.head(top_n).sort_values("Importance", ascending=True)
    
    fig_imp = go.Figure()
    fig_imp.add_trace(go.Bar(
        y=top_features["CleanFeature"],
        x=top_features["Importance"],
        orientation="h",
        marker_color=theme["accent"],
        name="Relative Importance"
    ))
    fig_imp.update_layout(
        height=max(380, top_n * 24),
        title=f"Top {top_n} Predictive Features by Model Importance Weight",
        xaxis_title="Relative Feature Importance Score",
        yaxis_title="",
        margin=dict(l=10, r=20, t=40, b=40)
    )
    apply_theme_to_plotly(fig_imp, theme_mode)
    st.plotly_chart(fig_imp, use_container_width=True)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # Interpretability Callout
    st.markdown("<h2>Feature Significance & Domain Takeaways</h2>", unsafe_allow_html=True)
    
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        st.markdown(
            f"""
            <div class="info-note" style="border-left-color: {theme['accent']};">
                <strong>Methodological Demarcation:</strong><br>
                Feature importance indicates which variables contributed most effectively to minimizing prediction loss during training. 
                <em>Feature importance indicates model contribution, not causation.</em>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown(
            """
            <div class="signal-card">
                <div class="signal-title">1. Autoregressive Lag Dominance</div>
                <p class="signal-desc">
                    <code>Lag1_Revenue</code> and <code>EnrollmentMomentum</code> rank as primary predictive drivers. Course demand exhibits strong short-term inertia—courses carrying positive momentum tend to persist into adjacent months.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_c2:
        st.markdown(
            """
            <div class="signal-card">
                <div class="signal-title">2. Instructor Profile & Quality Baseline</div>
                <p class="signal-desc">
                    <code>Instructor Experience</code>, <code>Instructor Rating</code>, and <code>CourseRating</code> establish foundational credibility weights, separating high-retention professional tracks from unreviewed offerings.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown(
            """
            <div class="signal-card">
                <div class="signal-title">3. Content Duration & Academic Seasonality</div>
                <p class="signal-desc">
                    <code>CourseDuration</code>, <code>MonthNumber</code>, and <code>Quarter</code> capture course depth and quarterly academic cycles, modeling cohort surges at quarter boundaries.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
