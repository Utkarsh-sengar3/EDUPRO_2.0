"""EDUPRO About, creator story and methodology."""
import streamlit as st
from utils.theme import get_theme
from pathlib import Path


def render_about(theme_mode: str = "light"):
    t = get_theme(theme_mode)
    st.markdown("<h1>About EDUPRO</h1>", unsafe_allow_html=True)
    st.markdown("<p class='page-subtitle'>A predictive intelligence workspace for course demand, revenue and portfolio decisions.</p>", unsafe_allow_html=True)

    st.markdown('''
    <div class="hero-box">
      <div class="hero-kicker">✦ Built with data science + product thinking</div>
      <h2>EDUPRO turns educational data into decisions.</h2>
      <p>Instead of stopping at charts, the platform connects historical course activity with machine-learning forecasts so a decision-maker can move from <strong>what happened</strong> to <strong>what may happen next</strong> and finally to <strong>what should be investigated</strong>.</p>
    </div>''', unsafe_allow_html=True)

    st.markdown("### The creator", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown(f'''<div class="creator-card" style="min-height:190px;">
          <div style="display:flex;align-items:center;gap:12px;">
            <div class="creator-avatar" style="width:58px;height:58px;font-size:1.05rem;">US</div>
            <div><div style="font-size:1.05rem;font-weight:800;color:{t["text_primary"]};">Utkarsh Sengar</div>
            <div style="font-size:.74rem;color:{t["accent_light"]};font-weight:700;">AI / ML-focused developer</div></div>
          </div>
          <p style="margin-top:1rem;color:{t["text_secondary"]};font-size:.82rem;line-height:1.65;">EDUPRO is designed as a practical AI/ML portfolio project: combining predictive modelling, data visualization, product UX and transparent model evaluation in one application.</p>
        </div>''', unsafe_allow_html=True)
    with c2:
        st.markdown(f'''<div class="info-note" style="height:100%;border-left:3px solid {t["accent"]};">
          <strong style="color:{t["text_primary"]};">Why I built it</strong><br><br>
          Educational platforms generate a lot of activity data, but raw historical numbers do not automatically tell teams what to prioritize next. EDUPRO was built to explore how machine learning can support course planning through demand forecasting, revenue estimation, category comparisons and model explainability.<br><br>
          <strong style="color:{t["text_primary"]};">Project philosophy:</strong> keep the interface modern, the analysis understandable and the model evaluation honest.
        </div>''', unsafe_allow_html=True)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown("### What EDUPRO does", unsafe_allow_html=True)
    a,b,c,d = st.columns(4)
    cards = [
        (a,"01","Demand","Forecast upcoming course enrollment demand."),
        (b,"02","Revenue","Translate demand and price into revenue projections."),
        (c,"03","Intelligence","Compare categories, trends and portfolio signals."),
        (d,"04","Explainability","Inspect model performance and influential features."),
    ]
    for col,num,title,desc in cards:
        with col:
            st.markdown(f'''<div class="kpi-card" style="min-height:150px;"><div class="kpi-title">{num}</div><div style="font-size:1rem;font-weight:800;color:{t["text_primary"]};margin:.55rem 0 .35rem;">{title}</div><div class="kpi-subtext" style="line-height:1.5;">{desc}</div></div>''', unsafe_allow_html=True)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown("### End-to-end workflow", unsafe_allow_html=True)
    st.markdown(f'''<div class="info-note" style="border-left:0;border-top:3px solid {t["accent"]};">
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;">
        <div><strong style="color:{t["text_primary"]};">01 · Data</strong><br><span style="font-size:.78rem;">Clean course-month panels and prepare modelling data.</span></div>
        <div><strong style="color:{t["text_primary"]};">02 · Features</strong><br><span style="font-size:.78rem;">Build lag, rolling and momentum signals.</span></div>
        <div><strong style="color:{t["text_primary"]};">03 · Models</strong><br><span style="font-size:.78rem;">Benchmark linear and ensemble regressors.</span></div>
        <div><strong style="color:{t["text_primary"]};">04 · Decisions</strong><br><span style="font-size:.78rem;">Forecast demand, revenue and portfolio opportunities.</span></div>
      </div>
    </div>''', unsafe_allow_html=True)

    st.markdown("### Technology stack", unsafe_allow_html=True)
    tech = ["Python", "Streamlit", "Pandas", "NumPy", "Plotly", "Scikit-learn", "Joblib", "Custom CSS"]
    st.markdown(" ".join([f'<span class="badge badge-moderate" style="margin:3px;">{x}</span>' for x in tech]), unsafe_allow_html=True)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    paper = Path(__file__).resolve().parents[1] / "EduPro_Research_Paper.pdf"
    if paper.exists():
        st.download_button("↗  Open / download research paper", data=paper.read_bytes(), file_name="EduPro_Research_Paper.pdf", mime="application/pdf", type="primary")

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    l1,l2 = st.columns(2)
    with l1:
        st.markdown("### Honest limitations")
        st.markdown("""
        - The historical panel covers a limited number of seasonal cycles.
        - External shocks such as campaigns and holidays are not fully represented.
        - Out-of-time performance should be interpreted carefully; forecasts are decision-support signals, not guarantees.
        """)
    with l2:
        st.markdown("### Future direction")
        st.markdown("""
        - Longer longitudinal history and richer learner behaviour.
        - Scenario-based pricing and capacity planning.
        - Real-time data ingestion and scheduled model refreshes.
        - More granular explainability and confidence intervals.
        """)

    st.markdown(f'''<div style="text-align:center;margin-top:2rem;padding:1rem;color:{t["text_muted"]};font-size:.72rem;">
      EDUPRO · Predictive Intelligence · Designed & developed by <strong style="color:{t["text_secondary"]};">Utkarsh Sengar</strong>
    </div>''', unsafe_allow_html=True)
