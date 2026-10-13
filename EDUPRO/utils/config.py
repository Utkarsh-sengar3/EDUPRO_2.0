"""
EDUPRO Configuration Module
Defines visual themes, chart templates, and directory paths.
"""

from pathlib import Path
import plotly.io as pio
import plotly.graph_objects as go

# Directory Paths
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
MODELS_DIR = ROOT_DIR / "models"
ASSETS_DIR = ROOT_DIR / "assets"
PHASE3_DIR = ROOT_DIR / "Phase-3"
PHASE4_DIR = ROOT_DIR / "Phase-4"
PHASE6_DIR = ROOT_DIR / "Phase-6"

# Color Palette - Modern Enterprise Analytics
COLORS = {
    "primary": "#0F172A",       # Deep Navy
    "secondary": "#334155",     # Slate Blue
    "accent": "#2563EB",        # Enterprise Blue
    "accent_light": "#3B82F6",  # Vibrant Blue
    "background": "#F8FAFC",    # Off-white Slate
    "card": "#FFFFFF",          # Pure White
    "border": "#E2E8F0",        # Light Slate Border
    "text_primary": "#0F172A",  # Charcoal Dark
    "text_muted": "#64748B",    # Muted Slate
    "text_light": "#94A3B8",    # Light Slate
    
    # Semantic Colors
    "success": "#16A34A",       # Positive Green
    "danger": "#DC2626",        # Negative Red
    "warning": "#D97706",       # Amber Warning
    "info": "#2563EB",          # Informational Blue
    
    # Chart series palette
    "actual": "#1E293B",        # Deep Charcoal
    "predicted": "#2563EB",     # Accent Blue
    "series": [
        "#1E293B", "#2563EB", "#0D9488", "#7C3AED", "#D97706",
        "#475569", "#0284C7", "#059669", "#DB2777", "#4F46E5"
    ]
}

# Setup Clean Plotly Enterprise Template
def get_plotly_layout():
    return dict(
        font=dict(family="Inter, -apple-system, Segoe UI, Roboto, sans-serif", color="#0F172A", size=12),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        margin=dict(l=40, r=30, t=50, b=40),
        xaxis=dict(
            showgrid=True,
            gridcolor="#F1F5F9",
            linecolor="#E2E8F0",
            zeroline=False,
            tickfont=dict(color="#64748B", size=11)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#F1F5F9",
            linecolor="#E2E8F0",
            zeroline=False,
            tickfont=dict(color="#64748B", size=11)
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#334155", size=11)
        ),
        hoverlabel=dict(
            bgcolor="#0F172A",
            font_size=12,
            font_family="Inter, sans-serif",
            font_color="#FFFFFF"
        )
    )

def apply_plotly_theme(fig):
    """Applies clean enterprise styling to any Plotly Figure."""
    fig.update_layout(**get_plotly_layout())
    return fig
