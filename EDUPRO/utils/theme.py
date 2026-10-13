"""EDUPRO visual system — premium AI SaaS theme with Light/Dark modes."""
from typing import Dict, Any
import plotly.graph_objects as go

THEMES: Dict[str, Dict[str, Any]] = {
    "light": {
        "name":"light","bg_app":"#F7F7FB","bg_card":"#FFFFFF","bg_sidebar":"#FFFFFF","bg_secondary":"#F1F0F7",
        "bg_hero":"linear-gradient(135deg,#170B2B 0%,#3B176E 58%,#6D28D9 100%)","bg_hero_card":"#160A29",
        "text_primary":"#181225","text_secondary":"#433A55","text_muted":"#7B728A","text_hero":"#FFFFFF","text_hero_muted":"#D8CFE7",
        "border":"#E8E3EF","border_card":"#E7E0F0","border_hero":"rgba(255,255,255,.14)",
        "accent":"#7C3AED","accent_light":"#A855F7","accent_bg":"#F3E8FF","accent_hover":"#6D28D9",
        "success":"#10B981","success_bg":"#ECFDF5","danger":"#EF4444","danger_bg":"#FEF2F2","warning":"#F59E0B","warning_bg":"#FFFBEB","info":"#6366F1","info_bg":"#EEF2FF",
        "shadow_sm":"0 2px 10px rgba(39,20,70,.06)","shadow_md":"0 12px 30px rgba(39,20,70,.10)","shadow_lg":"0 24px 60px rgba(39,20,70,.14)",
        "chart_paper":"#FFFFFF","chart_plot":"#FFFFFF","chart_grid":"#EEEAF4","chart_line":"#DDD6E7","chart_text":"#181225","chart_muted":"#7B728A",
        "bar_primary":"#7C3AED","bar_accent":"#A855F7","series":["#7C3AED","#A855F7","#06B6D4","#10B981","#F59E0B","#EC4899","#6366F1"]
    },
    "dark": {
        "name":"dark","bg_app":"#07050C","bg_card":"#100B19","bg_sidebar":"#090610","bg_secondary":"#171021",
        "bg_hero":"linear-gradient(135deg,#12051F 0%,#2A0D46 55%,#5B21B6 100%)","bg_hero_card":"#10071C",
        "text_primary":"#FAF8FF","text_secondary":"#D6CFE0","text_muted":"#92879F","text_hero":"#FFFFFF","text_hero_muted":"#D1C5DE",
        "border":"#251A31","border_card":"#2B1D38","border_hero":"rgba(255,255,255,.12)",
        "accent":"#A855F7","accent_light":"#C084FC","accent_bg":"rgba(168,85,247,.14)","accent_hover":"#9333EA",
        "success":"#34D399","success_bg":"rgba(52,211,153,.12)","danger":"#FB7185","danger_bg":"rgba(251,113,133,.12)","warning":"#FBBF24","warning_bg":"rgba(251,191,36,.12)","info":"#818CF8","info_bg":"rgba(129,140,248,.12)",
        "shadow_sm":"0 2px 16px rgba(0,0,0,.28)","shadow_md":"0 16px 40px rgba(0,0,0,.35)","shadow_lg":"0 30px 80px rgba(0,0,0,.42)",
        "chart_paper":"#100B19","chart_plot":"#100B19","chart_grid":"#261A32","chart_line":"#382647","chart_text":"#FAF8FF","chart_muted":"#92879F",
        "bar_primary":"#A855F7","bar_accent":"#C084FC","series":["#A855F7","#7C3AED","#22D3EE","#34D399","#FBBF24","#F472B6","#818CF8"]
    }
}

def get_theme(theme_mode: str) -> Dict[str, Any]:
    return THEMES["dark" if "dark" in str(theme_mode).lower() else "light"]

def get_theme_css(theme_mode: str) -> str:
    t=get_theme(theme_mode)
    return f'''<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
:root {{ color-scheme: {"dark" if t["name"]=="dark" else "light"}; }}
html,body,.stApp {{ background:{t["bg_app"]}!important; color:{t["text_primary"]}!important; font-family:'Plus Jakarta Sans',Inter,system-ui,sans-serif!important; }}
[data-testid="stSidebar"] {{ background:{t["bg_sidebar"]}!important; border-right:1px solid {t["border"]}!important; }}
[data-testid="stSidebar"] .block-container {{ padding:1.1rem 1rem 1.5rem!important; }}
[data-testid="stSidebarNav"],.stSidebarNav {{ display:none!important; }}
.main .block-container {{ max-width:1420px; padding:1.6rem 2.1rem 3.5rem!important; }}
h1,h2,h3,h4 {{ color:{t["text_primary"]}!important; font-family:'Plus Jakarta Sans',sans-serif!important; letter-spacing:-.035em!important; }}
h1 {{ font-size:2.05rem!important; font-weight:800!important; }}
h2 {{ font-size:1.35rem!important; font-weight:750!important; }}
h3 {{ font-size:1.03rem!important; font-weight:700!important; }}
p,li,span,label {{ color:{t["text_secondary"]}; }}
.page-subtitle {{ color:{t["text_muted"]}!important; font-size:.93rem; margin-bottom:1.2rem; }}
div[data-testid="stSidebar"] div[data-testid="stRadio"] > div {{ gap:4px!important; }}
div[data-testid="stSidebar"] div[data-testid="stRadio"] label {{ border:1px solid transparent!important; border-radius:12px!important; padding:.62rem .78rem!important; margin:2px 0!important; cursor:pointer!important; transition:.18s ease!important; }}
div[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover {{ background:{t["bg_secondary"]}!important; transform:translateX(2px); }}
div[data-testid="stSidebar"] div[data-testid="stRadio"] label > div:first-child {{ display:none!important; }}
div[data-testid="stSidebar"] div[data-testid="stRadio"] label div[data-testid="stMarkdownContainer"] p {{ color:{t["text_secondary"]}!important; font-size:.86rem!important; font-weight:600!important; margin:0!important; }}
div[data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) {{ background:{t["accent_bg"]}!important; border-color:rgba(168,85,247,.35)!important; box-shadow:inset 3px 0 0 {t["accent"]}!important; }}
div[data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) div[data-testid="stMarkdownContainer"] p {{ color:{t["accent_light"] if t["name"]=="dark" else t["accent"]}!important; }}
.brand-mark {{ width:42px;height:42px;border-radius:13px;display:flex;align-items:center;justify-content:center;color:white;font-weight:800;background:linear-gradient(135deg,#A855F7,#6D28D9);box-shadow:0 8px 24px rgba(124,58,237,.35); }}
.brand-name {{ font-size:1.15rem;font-weight:800;letter-spacing:-.04em;color:{t["text_primary"]}; }}
.brand-sub {{ font-size:.62rem!important;font-weight:700!important;letter-spacing:.12em;text-transform:uppercase;color:{t["accent_light"]}!important; }}
.hero-box {{ position:relative; overflow:hidden; background:{t["bg_hero"]}; border:1px solid {t["border_hero"]}; border-radius:22px; padding:2rem 2.1rem; margin:.5rem 0 1.4rem; box-shadow:{t["shadow_lg"]}; }}
.hero-box:after {{ content:"";position:absolute;width:360px;height:360px;right:-120px;top:-190px;background:radial-gradient(circle,rgba(216,180,254,.24),transparent 68%);pointer-events:none; }}
.hero-box h2 {{ color:#fff!important;font-size:1.55rem!important;margin:0 0 .45rem!important; }}
.hero-box p {{ color:{t["text_hero_muted"]}!important;max-width:900px;margin:0!important;line-height:1.65!important; }}
.hero-kicker {{ color:#E9D5FF!important;font-size:.7rem!important;font-weight:800!important;letter-spacing:.12em!important;text-transform:uppercase!important;margin-bottom:.55rem!important; }}
.kpi-card {{ background:{t["bg_card"]};border:1px solid {t["border_card"]};border-radius:17px;padding:1rem 1.05rem;min-height:122px;box-shadow:{t["shadow_sm"]};transition:.2s ease;position:relative;overflow:hidden; }}
.kpi-card:after {{ content:"";position:absolute;left:0;top:0;width:100%;height:2px;background:linear-gradient(90deg,{t["accent"]},transparent);opacity:.8; }}
.kpi-card:hover {{ transform:translateY(-3px);border-color:rgba(168,85,247,.45);box-shadow:{t["shadow_md"]}; }}
.kpi-title {{ color:{t["text_muted"]}!important;font-size:.7rem!important;font-weight:800!important;text-transform:uppercase;letter-spacing:.08em; }}
.kpi-value {{ color:{t["text_primary"]}!important;font-size:1.65rem!important;font-weight:800!important;letter-spacing:-.04em;margin:.25rem 0!important; }}
.kpi-subtext {{ color:{t["text_muted"]}!important;font-size:.74rem!important; }}
.kpi-icon {{ font-size:1rem; }}
.signal-card,.info-note {{ background:{t["bg_card"]};border:1px solid {t["border"]};border-radius:16px;padding:1rem 1.1rem;box-shadow:{t["shadow_sm"]}; }}
.signal-card {{ border-left:3px solid {t["accent"]};margin-bottom:.75rem; }}
.signal-title {{ color:{t["text_primary"]}!important;font-size:.88rem;font-weight:750;margin-bottom:.25rem; }}
.signal-desc {{ color:{t["text_secondary"]}!important;font-size:.8rem;margin:0;line-height:1.55; }}
.section-divider {{ height:1px;background:{t["border"]};margin:1.5rem 0; }}
div.stButton>button {{ border-radius:12px!important;border:1px solid {t["border"]}!important;background:{t["bg_card"]}!important;color:{t["text_primary"]}!important;font-weight:700!important;padding:.62rem 1rem!important;transition:.18s ease!important; }}
div.stButton>button:hover {{ border-color:{t["accent"]}!important;color:{t["accent_light"] if t["name"]=="dark" else t["accent"]}!important;transform:translateY(-1px);box-shadow:{t["shadow_sm"]}!important; }}
button[kind="primary"],div.stButton>button[kind="primary"] {{ background:linear-gradient(135deg,{t["accent"]},{t["accent_hover"]})!important;color:white!important;border-color:transparent!important; }}
[data-baseweb="select"]>div,input,textarea {{ border-radius:11px!important; }}
div[data-testid="stDataFrame"] {{ border:1px solid {t["border"]};border-radius:14px;overflow:hidden; }}
.badge {{ display:inline-flex;align-items:center;padding:.28rem .62rem;border-radius:999px;font-size:.68rem;font-weight:800;letter-spacing:.04em;text-transform:uppercase; }}
.badge-low {{ background:{t["bg_secondary"]};color:{t["text_muted"]};border:1px solid {t["border"]}; }}
.badge-moderate {{ background:{t["accent_bg"]};color:{t["accent_light"] if t["name"]=="dark" else t["accent"]};border:1px solid rgba(168,85,247,.28); }}
.badge-high {{ background:{t["success_bg"]};color:{t["success"]};border:1px solid rgba(52,211,153,.25); }}
.badge-warning {{ background:{t["warning_bg"]};color:{t["warning"]};border:1px solid rgba(251,191,36,.25); }}
.creator-card {{ background:linear-gradient(145deg,{t["bg_card"]},{t["bg_secondary"]});border:1px solid {t["border"]};border-radius:18px;padding:1rem; }}
.creator-avatar {{ width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#A855F7,#22D3EE);color:white;font-weight:800; }}
@media(max-width:900px){{.main .block-container{{padding-left:1rem!important;padding-right:1rem!important}}.hero-box{{padding:1.4rem}}h1{{font-size:1.7rem!important}}}}
</style>'''

def apply_theme_to_plotly(fig: go.Figure, theme_mode: str) -> go.Figure:
    t=get_theme(theme_mode)
    fig.update_layout(font=dict(family="'Plus Jakarta Sans', sans-serif",color=t["chart_text"],size=12),paper_bgcolor=t["chart_paper"],plot_bgcolor=t["chart_plot"],margin=dict(l=40,r=24,t=42,b=42),xaxis=dict(showgrid=True,gridcolor=t["chart_grid"],linecolor=t["chart_line"],zeroline=False,tickfont=dict(color=t["chart_muted"])),yaxis=dict(showgrid=True,gridcolor=t["chart_grid"],linecolor=t["chart_line"],zeroline=False,tickfont=dict(color=t["chart_muted"])),legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1,font=dict(color=t["chart_text"])),hoverlabel=dict(bgcolor=t["bg_card"],font_color=t["text_primary"],bordercolor=t["border"]))
    return fig
