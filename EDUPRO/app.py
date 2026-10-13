"""EDUPRO — Predictive Intelligence for Course Demand & Revenue Forecasting."""
import streamlit as st

st.set_page_config(
    page_title="EDUPRO — Predictive Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.theme import get_theme_css, get_theme
from views.overview import render_overview
from views.eda import render_eda
from views.demand_prediction import render_demand_prediction
from views.revenue_forecast import render_revenue_forecast
from views.category_analysis import render_category_analysis
from views.model_performance import render_model_performance
from views.feature_importance import render_feature_importance
from views.about import render_about

NAV = [
    "◈ Overview",
    "⌁ EDA & Insights",
    "◎ Demand Prediction",
    "₹ Revenue Forecast",
    "▦ Category Analysis",
    "ϟ Model Performance",
    "◌ Feature Importance",
    "♡ About & Creator",
]

if "theme" not in st.session_state:
    st.session_state["theme"] = "🌙 Dark"
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "◈ Overview"


def go(page: str):
    st.session_state["current_page"] = page


def main():
    theme_mode = "dark" if "Dark" in st.session_state["theme"] else "light"
    st.markdown(get_theme_css(theme_mode), unsafe_allow_html=True)
    t = get_theme(theme_mode)

    # Sidebar brand
    st.sidebar.markdown(
        f'''<div style="display:flex;align-items:center;gap:11px;padding:.2rem .15rem 1rem;margin-bottom:.8rem;border-bottom:1px solid {t["border"]};">
            <div class="brand-mark">EP</div>
            <div><div class="brand-name">EDUPRO</div><div class="brand-sub">Predictive Intelligence</div></div>
        </div>''', unsafe_allow_html=True)

    st.sidebar.markdown('<div style="font-size:.64rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase;opacity:.55;margin:.35rem 0 .45rem .15rem;">Explore</div>', unsafe_allow_html=True)
    selected = st.sidebar.radio("Navigation", NAV, index=NAV.index(st.session_state["current_page"]), label_visibility="collapsed")
    st.session_state["current_page"] = selected

    st.sidebar.markdown('<div style="height:1px;margin:1rem 0;background:rgba(128,128,128,.16);"></div>', unsafe_allow_html=True)
    st.sidebar.markdown('<div style="font-size:.64rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase;opacity:.55;margin:.35rem 0 .45rem .15rem;">Appearance</div>', unsafe_allow_html=True)
    theme_choice = st.sidebar.radio("Theme", ["🌙 Dark", "☀ Light"], index=0 if theme_mode == "dark" else 1, horizontal=True, label_visibility="collapsed")
    if theme_choice != st.session_state["theme"]:
        st.session_state["theme"] = theme_choice
        st.rerun()

    st.sidebar.markdown('<div style="height:1px;margin:1rem 0;background:rgba(128,128,128,.16);"></div>', unsafe_allow_html=True)
    st.sidebar.markdown(
        f'''<div class="creator-card">
            <div style="display:flex;gap:10px;align-items:center;">
                <div class="creator-avatar">US</div>
                <div><div style="font-weight:800;font-size:.86rem;color:{t["text_primary"]};">Built by Utkarsh Sengar</div>
                <div style="font-size:.7rem;color:{t["text_muted"]};">AI / ML Project · EDUPRO</div></div>
            </div>
            <div style="margin-top:.75rem;font-size:.71rem;color:{t["text_muted"]};line-height:1.55;">A predictive analytics platform for understanding course demand, revenue and portfolio opportunities.</div>
        </div>''', unsafe_allow_html=True)

    st.sidebar.markdown('<div style="height:1px;margin:1rem 0;background:rgba(128,128,128,.16);"></div>', unsafe_allow_html=True)
    st.sidebar.markdown(
        f'''<div style="font-size:.72rem;color:{t["text_muted"]};line-height:1.7;">
            <div><span style="color:#34D399;">●</span> ML Engine <strong style="color:{t["text_secondary"]};">Operational</strong></div>
            <div><span style="color:#22D3EE;">●</span> Catalog <strong style="color:{t["text_secondary"]};">60 courses</strong></div>
            <div><span style="color:#A855F7;">●</span> Forecast <strong style="color:{t["text_secondary"]};">Ready</strong></div>
        </div>''', unsafe_allow_html=True)

    key = selected.split(" ", 1)[1] if " " in selected else selected
    if key == "Overview":
        render_overview(theme_mode)
    elif key == "EDA & Insights":
        render_eda(theme_mode)
    elif key == "Demand Prediction":
        render_demand_prediction(theme_mode)
    elif key == "Revenue Forecast":
        render_revenue_forecast(theme_mode)
    elif key == "Category Analysis":
        render_category_analysis(theme_mode)
    elif key == "Model Performance":
        render_model_performance(theme_mode)
    elif key == "Feature Importance":
        render_feature_importance(theme_mode)
    elif key == "About & Creator":
        render_about(theme_mode)


if __name__ == "__main__":
    main()
