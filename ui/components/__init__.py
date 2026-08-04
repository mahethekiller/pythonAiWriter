"""
UI Components Package
=====================
Modular desktop layout components including Sidebar, Toolbar, StatusBar, and PreviewPanel.
"""

from .sidebar import SidebarComponent
from .toolbar import ToolbarComponent
from .statusbar import StatusBarComponent
from .preview_panel import PreviewPanelComponent

__all__ = [
    "SidebarComponent",
    "ToolbarComponent",
    "StatusBarComponent",
    "PreviewPanelComponent",
]
