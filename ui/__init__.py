"""
UI Package Initialization
=========================
Exports ConfigManager, ThemeManager, components, views, and backwards-compatible tab builders.
"""

from .config_manager import ConfigManager
from .theme_manager import ThemeManager
from .components import SidebarComponent, ToolbarComponent, StatusBarComponent, PreviewPanelComponent
from .views import (
    build_dashboard_view, 
    build_blog_view, 
    build_settings_view, 
    build_templates_view, 
    build_history_view,
    build_humanizer_view,
    build_serp_view,
    build_audit_view,
    build_publisher_view,
    build_gap_view,
    build_citation_view
)
from .dashboard_tab import build_dashboard_tab
from .blog_tab import build_blog_tab
from .settings_tab import build_settings_tab

__all__ = [
    "ConfigManager",
    "ThemeManager",
    "SidebarComponent",
    "ToolbarComponent",
    "StatusBarComponent",
    "PreviewPanelComponent",
    "build_dashboard_view",
    "build_blog_view",
    "build_settings_view",
    "build_templates_view",
    "build_history_view",
    "build_humanizer_view",
    "build_serp_view",
    "build_audit_view",
    "build_publisher_view",
    "build_gap_view",
    "build_citation_view",
    "build_dashboard_tab",
    "build_blog_tab",
    "build_settings_tab",
]
