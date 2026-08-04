"""
Collapsible Navigation Sidebar Component with Dedicated Standalone Feature Workspace Tabs.
"""

import customtkinter as ctk
from typing import Callable, Dict, Any, List


class SidebarComponent(ctk.CTkFrame):
    """Left Navigation Sidebar component with dedicated tabs for all major features."""

    NAV_ITEMS = [
        {"id": "blog", "icon": "✍️", "label": "SEO Blog Creator"},
        {"id": "rewriter", "icon": "🚀", "label": "Rewriter Studio"},
        {"id": "humanizer", "icon": "🛡️", "label": "AI Humanizer Studio"},
        {"id": "serp", "icon": "🔍", "label": "SERP Intelligence"},
        {"id": "gap", "icon": "📊", "label": "Keyword & Content Gap"},
        {"id": "citation", "icon": "🤖", "label": "AI Citation Tracker"},
        {"id": "audit", "icon": "🐸", "label": "Technical SEO & Disavow"},
        {"id": "publisher", "icon": "🌐", "label": "CMS Publisher"},
        {"id": "templates", "icon": "📜", "label": "AI Templates"},
        {"id": "history", "icon": "📚", "label": "History & Exports"},
        {"id": "settings", "icon": "⚙️", "label": "Settings & API Keys"},
    ]

    def __init__(self, parent, theme_mgr, on_nav_change: Callable[[str], None], **kwargs):
        colors = theme_mgr.colors
        super().__init__(
            parent, 
            fg_color=colors["bg_sidebar"], 
            width=240, 
            corner_radius=0, 
            border_width=1,
            border_color=colors["border"],
            **kwargs
        )
        
        self.theme_mgr = theme_mgr
        self.on_nav_change = on_nav_change
        self.active_view = "blog"

        self.buttons: Dict[str, ctk.CTkButton] = {}

        self._build_ui()

    def _build_ui(self):
        """Constructs logo header, navigation items, active provider card, and developer profile footer."""
        colors = self.theme_mgr.colors

        # 1. Top Logo Header Frame
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=14, pady=(14, 10))

        self.logo_icon = ctk.CTkLabel(
            self.header_frame,
            text="⚡",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=colors["primary"]
        )
        self.logo_icon.pack(side="left", padx=(0, 6))

        self.logo_text = ctk.CTkLabel(
            self.header_frame,
            text="AI Content Studio",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=colors["text_primary"],
            anchor="w"
        )
        self.logo_text.pack(side="left")

        # Separator Line
        self.sep1 = ctk.CTkFrame(self, fg_color=colors["border"], height=1)
        self.sep1.pack(fill="x", padx=14, pady=(0, 8))

        # 2. Navigation Items Container
        self.nav_container = ctk.CTkFrame(self, fg_color="transparent")
        self.nav_container.pack(fill="both", expand=True, padx=10, pady=0)

        for item in self.NAV_ITEMS:
            btn = ctk.CTkButton(
                self.nav_container,
                text=f"  {item['icon']}   {item['label']}",
                anchor="w",
                height=34,
                font=ctk.CTkFont(size=11, weight="bold"),
                fg_color="transparent",
                hover_color=colors["bg_card_hover"],
                text_color=colors["text_secondary"],
                corner_radius=8,
                command=lambda view_id=item["id"]: self._select_nav(view_id)
            )
            btn.pack(fill="x", pady=1)
            self.buttons[item["id"]] = btn

        # 3. Bottom Active AI Provider Card
        self.provider_card = ctk.CTkFrame(
            self,
            fg_color=colors["bg_card"],
            border_width=1,
            border_color=colors["border"],
            corner_radius=10
        )
        self.provider_card.pack(fill="x", padx=12, pady=(6, 4))

        self.lbl_prov_header = ctk.CTkLabel(
            self.provider_card,
            text="Active AI Provider  🟢",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=colors["text_muted"]
        )
        self.lbl_prov_header.pack(anchor="w", padx=12, pady=(6, 2))

        self.lbl_prov_name = ctk.CTkLabel(
            self.provider_card,
            text="⚡ Google Gemini",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=colors["primary"]
        )
        self.lbl_prov_name.pack(anchor="w", padx=12, pady=0)

        self.lbl_model_sub = ctk.CTkLabel(
            self.provider_card,
            text="gemini-2.0-flash",
            font=ctk.CTkFont(size=10),
            text_color=colors["text_secondary"]
        )
        self.lbl_model_sub.pack(anchor="w", padx=12, pady=(0, 2))

        self.lbl_cost = ctk.CTkLabel(
            self.provider_card,
            text="Est. Cost: ~$0.003 USD",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=colors["success"]
        )
        self.lbl_cost.pack(anchor="w", padx=12, pady=(0, 6))

        # 4. Bottom Developer Profile Footer Card
        self.dev_card = ctk.CTkFrame(
            self,
            fg_color=colors["bg_card"],
            border_width=1,
            border_color=colors["border"],
            corner_radius=10
        )
        self.dev_card.pack(fill="x", padx=12, pady=(0, 10))

        dev_inner = ctk.CTkFrame(self.dev_card, fg_color="transparent")
        dev_inner.pack(fill="x", padx=10, pady=6)

        self.dev_avatar = ctk.CTkLabel(
            dev_inner,
            text="👤",
            font=ctk.CTkFont(size=14),
            width=24,
            height=24,
            fg_color=colors["border"],
            corner_radius=12
        )
        self.dev_avatar.pack(side="left", padx=(0, 6))

        dev_text_frame = ctk.CTkFrame(dev_inner, fg_color="transparent")
        dev_text_frame.pack(side="left", fill="both", expand=True)

        self.dev_sub = ctk.CTkLabel(
            dev_text_frame,
            text="Developed by",
            font=ctk.CTkFont(size=8),
            text_color=colors["text_muted"],
            anchor="w"
        )
        self.dev_sub.pack(anchor="w")

        self.dev_name = ctk.CTkLabel(
            dev_text_frame,
            text="@mahethekiller",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=colors["text_primary"],
            anchor="w"
        )
        self.dev_name.pack(anchor="w")

        self.dev_dot = ctk.CTkLabel(
            dev_inner,
            text="🟢",
            font=ctk.CTkFont(size=8)
        )
        self.dev_dot.pack(side="right")

        self._update_button_styles()

    def _select_nav(self, view_id: str):
        """Selects a navigation view and updates styling."""
        if self.active_view != view_id:
            self.active_view = view_id
            self._update_button_styles()
            self.on_nav_change(view_id)

    def set_active(self, view_id: str):
        """Programmatically sets active view."""
        if view_id in self.buttons:
            self.active_view = view_id
            self._update_button_styles()

    def update_provider_info(self, provider: str, model: str, threads: int, cost_usd: float):
        """Updates live active provider card display."""
        self.lbl_prov_name.configure(text=f"⚡ {provider}")
        self.lbl_model_sub.configure(text=model)
        self.lbl_cost.configure(text=f"Est. Cost: ~${cost_usd:.3f} USD")

    def _update_button_styles(self):
        """Updates active nav pill styling."""
        colors = self.theme_mgr.colors
        for item in self.NAV_ITEMS:
            view_id = item["id"]
            btn = self.buttons.get(view_id)
            if not btn:
                continue

            if view_id == self.active_view:
                btn.configure(
                    fg_color=colors["primary"],
                    text_color="#FFFFFF",
                    hover_color=colors["primary_hover"]
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=colors["text_secondary"],
                    hover_color=colors["bg_card_hover"]
                )
