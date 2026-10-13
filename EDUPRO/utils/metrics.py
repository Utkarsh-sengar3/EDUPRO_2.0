"""
EDUPRO Metrics & Formatting Utilities
Provides consistent, enterprise-grade formatting for currency (₹ INR), integers,
percentages, and modern elevated SaaS metric cards.
"""

from typing import Union, Optional


def format_currency(amount: Union[float, int], decimals: int = 0) -> str:
    """Formats amount in Indian Rupees (₹) with clean comma formatting."""
    if amount is None or amount != amount:
        return "₹0"
    
    val = float(amount)
    if decimals == 0:
        return f"₹{val:,.0f}"
    return f"₹{val:,.{decimals}f}"


def format_int(count: Union[float, int]) -> str:
    """Formats an integer with thousands separator."""
    if count is None or count != count:
        return "0"
    return f"{int(round(count)):,}"


def format_decimal(val: Union[float, int], decimals: int = 2) -> str:
    """Formats a float with specified decimal precision."""
    if val is None or val != val:
        return "0.00"
    return f"{float(val):.{decimals}f}"


def format_percentage(val: Union[float, int], decimals: int = 1) -> str:
    """Formats a ratio as a percentage string."""
    if val is None or val != val:
        return "0.0%"
    return f"{float(val) * 100:.{decimals}f}%"


def render_kpi_card(
    title: str,
    value: str,
    subtext: str = "",
    icon: str = "",
    accent_color: Optional[str] = None
) -> str:
    """Generates HTML for an elevated enterprise SaaS KPI metric card."""
    subtext_html = f'<div class="kpi-subtext">{subtext}</div>' if subtext else ""
    icon_html = f'<div class="kpi-icon">{icon}</div>' if icon else ""
    border_style = f'border-top: 3px solid {accent_color};' if accent_color else ''
    
    return f"""
    <div class="kpi-card" style="{border_style}">
        <div class="kpi-header">
            <span class="kpi-title">{title}</span>
            {icon_html}
        </div>
        <div class="kpi-value">{value}</div>
        {subtext_html}
    </div>
    """


def render_signal_card(title: str, desc: str, border_color: str = "#2563EB", icon: str = "⚡") -> str:
    """Generates HTML for an intelligence signal alert card."""
    return f"""
    <div class="signal-card" style="border-left-color: {border_color};">
        <div class="signal-title"><span style="color: {border_color};">{icon}</span> {title}</div>
        <p class="signal-desc">{desc}</p>
    </div>
    """


def get_demand_category_info(predicted_enrollment: float) -> tuple[str, str, str]:
    """
    Categorizes predicted enrollment into transparent demand tiers:
    - Low Demand: < 8 enrollments
    - Moderate Demand: 8 - 18 enrollments
    - High Demand: > 18 enrollments
    Returns: (category_name, badge_css_class, description)
    """
    if predicted_enrollment < 8.0:
        return ("Low Demand", "badge-low", "Forecast indicates limited monthly intake (< 8 enrollments/mo). Catalog optimization advised.")
    elif predicted_enrollment <= 18.0:
        return ("Moderate Demand", "badge-moderate", "Forecast indicates steady baseline engagement (8–18 enrollments/mo). Regular performance cadence.")
    else:
        return ("High Demand", "badge-high", "Forecast indicates top-tier enrollment momentum (> 18 enrollments/mo). High monetization candidate.")
