"""
UI Package Views Exports for PythonAiWriter Desktop Studio.
"""

from .dashboard_view import build_dashboard_view
from .blog_view import build_blog_view
from .settings_view import build_settings_view
from .templates_view import build_templates_view
from .history_view import build_history_view
from .humanizer_view import build_humanizer_view
from .serp_view import build_serp_view
from .audit_view import build_audit_view
from .publisher_view import build_publisher_view
from .gap_view import build_gap_view
from .citation_view import build_citation_view

__all__ = [
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
    "build_citation_view"
]
