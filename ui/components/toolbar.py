"""
Top Application Toolbar Component with AI Provider & Model Presets Dropdown Selector.
"""

import customtkinter as ctk
from typing import Callable, Dict, Any, List


class ToolbarComponent(ctk.CTkFrame):
    """Top Toolbar Component matching mockup design."""

    TITLE_MAP = {
        "dashboard": ("Dashboard Overview", "System health & multi-provider status summary"),
        "rewriter": ("Rewriter Studio", "Scrape & rewrite webpage content with HTML layout preservation"),
        "blog": ("SEO Blog Creator", "Create SEO-optimized, engaging articles that rank."),
        "humanizer": ("AI Content Humanizer", "Naturalize tone & remove robotic AI vocabulary clichés."),
        "serp": ("SERP Intelligence", "Scrape live search rankings & competitor headings."),
        "gap": ("Keyword & Content Gap", "Head-to-head domain keyword gap analysis (You vs Competitors)."),
        "citation": ("AI Citation Tracker", "Track brand & URL citations in ChatGPT, Perplexity & Gemini."),
        "audit": ("Technical SEO & Disavow", "Run Screaming Frog crawls & toxic backlink disavow audits."),
        "publisher": ("CMS Direct Publisher", "Manage 1-click publishing to WordPress, Ghost & Shopify."),
        "templates": ("AI Templates", "Pre-configured SEO strategy presets & prompts"),
        "history": ("History & Exports", "Browse generated WordPress HTML, Docx, Markdown & JSON CMS files"),
        "settings": ("Settings & API Keys", "Manage LLM provider keys, custom endpoints, models & application preferences")
    }

    def __init__(
        self, 
        parent, 
        theme_mgr, 
        on_theme_toggle: Callable[[], None], 
        on_primary_action: Callable[[], None] = None,
        on_preset_change: Callable[[str], None] = None,
        **kwargs
    ):
        colors = theme_mgr.colors
        super().__init__(
            parent, 
            fg_color=colors["bg_toolbar"], 
            height=65, 
            corner_radius=0, 
            **kwargs
        )
        
        self.theme_mgr = theme_mgr
        self.on_theme_toggle = on_theme_toggle
        self.on_primary_action = on_primary_action
        self.on_preset_change = on_preset_change

        self._build_ui()

    def _build_ui(self):
        """Constructs title, provider preset dropdown, thread badge, cost badge, theme toggle button, help icon, and primary action button."""
        colors = self.theme_mgr.colors

        # 1. Left Page Title & Subtitle Frame
        self.title_container = ctk.CTkFrame(self, fg_color="transparent")
        self.title_container.pack(side="left", padx=18, pady=10)

        self.title_label = ctk.CTkLabel(
            self.title_container,
            text="SEO Blog Creator",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=colors["text_primary"]
        )
        self.title_label.pack(anchor="w")

        self.subtitle_label = ctk.CTkLabel(
            self.title_container,
            text="Create SEO-optimized, engaging articles that rank.",
            font=ctk.CTkFont(size=11),
            text_color=colors["text_secondary"]
        )
        self.subtitle_label.pack(anchor="w")

        # 2. Right Action Controls Container
        self.right_container = ctk.CTkFrame(self, fg_color="transparent")
        self.right_container.pack(side="right", padx=16, pady=10)

        # Primary Action Button (Top Right)
        self.btn_primary_action = ctk.CTkButton(
            self.right_container,
            text="⚡ Generate Article",
            font=ctk.CTkFont(size=12, weight="bold"),
            height=36,
            fg_color=colors["primary"],
            hover_color=colors["primary_hover"],
            text_color="#FFFFFF",
            corner_radius=8,
            command=self._handle_primary_action
        )
        self.btn_primary_action.pack(side="right", padx=(10, 0))

        # Help Icon Button
        self.btn_help = ctk.CTkButton(
            self.right_container,
            text="❓",
            width=32,
            height=32,
            fg_color=colors["bg_card"],
            hover_color=colors["bg_card_hover"],
            text_color=colors["text_secondary"],
            border_width=1,
            border_color=colors["border"],
            corner_radius=16
        )
        self.btn_help.pack(side="right", padx=4)

        # Theme Toggle Icon Button (Sun / Moon)
        theme_icon = "☀️" if self.theme_mgr.mode == "Light" else "🌙"
        self.btn_theme_toggle = ctk.CTkButton(
            self.right_container,
            text=theme_icon,
            width=36,
            height=32,
            fg_color=colors["bg_card"],
            hover_color=colors["bg_card_hover"],
            border_width=1,
            border_color=colors["border"],
            corner_radius=16,
            command=self._handle_theme_toggle
        )
        self.btn_theme_toggle.pack(side="right", padx=6)

        # Est. Cost Badge
        self.cost_badge = ctk.CTkFrame(
            self.right_container,
            fg_color=colors["bg_card"],
            border_width=1,
            border_color=colors["border"],
            corner_radius=8
        )
        self.cost_badge.pack(side="right", padx=4)

        self.lbl_cost_val = ctk.CTkLabel(
            self.cost_badge,
            text="Est. Cost  $0.003 USD",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=colors["success"]
        )
        self.lbl_cost_val.pack(padx=10, pady=4)

        # Threads Badge
        self.threads_badge = ctk.CTkFrame(
            self.right_container,
            fg_color=colors["bg_card"],
            border_width=1,
            border_color=colors["border"],
            corner_radius=8
        )
        self.threads_badge.pack(side="right", padx=4)

        self.lbl_threads_val = ctk.CTkLabel(
            self.threads_badge,
            text="Threads  3",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=colors["text_primary"]
        )
        self.lbl_threads_val.pack(padx=10, pady=4)

        # AI Provider & Model Presets Dropdown Selector
        self.provider_pill = ctk.CTkOptionMenu(
            self.right_container,
            values=["Select Model / Preset..."],
            width=260,
            height=34,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color=colors["bg_card"],
            button_color=colors["bg_card"],
            button_hover_color=colors["bg_card_hover"],
            dropdown_fg_color=colors["bg_card"],
            text_color=colors["text_primary"],
            command=self._on_preset_selected
        )
        self.provider_pill.pack(side="right", padx=6)

    def set_view_title(self, view_id: str):
        """Updates page title and subtitle."""
        title, subtitle = self.TITLE_MAP.get(view_id, ("AI Content Studio", "Multi-provider content generation studio."))
        self.title_label.configure(text=title)
        self.subtitle_label.configure(text=subtitle)

        if view_id == "rewriter":
            self.btn_primary_action.configure(text="⚡ Start Rewriting")
        elif view_id == "humanizer":
            self.btn_primary_action.configure(text="⚡ Humanize Content")
        elif view_id == "serp":
            self.btn_primary_action.configure(text="🔍 Fetch SERP Intel")
        elif view_id == "gap":
            self.btn_primary_action.configure(text="📊 Analyze Gap")
        elif view_id == "citation":
            self.btn_primary_action.configure(text="🤖 Test AI Visibility")
        elif view_id == "audit":
            self.btn_primary_action.configure(text="🚀 Run Audit")
        elif view_id == "publisher":
            self.btn_primary_action.configure(text="🌐 Publish to WP")
        else:
            self.btn_primary_action.configure(text="⚡ Generate Article")

    def update_preset_list(self, preset_names: List[str], current_preset: str = None):
        """Updates top toolbar preset dropdown values."""
        if not preset_names:
            preset_names = ["Select Model / Preset..."]
        self.provider_pill.configure(values=preset_names)
        if current_preset and current_preset in preset_names:
            self.provider_pill.set(current_preset)

    def update_provider_badge(self, provider: str, model: str, active_preset: str = None):
        """Updates top toolbar dropdown to reflect active provider and model or preset."""
        current_values = list(self.provider_pill.cget("values"))
        if active_preset and active_preset in current_values:
            self.provider_pill.set(active_preset)
        else:
            display_text = f"🤖 {provider}: {model}"
            if display_text not in current_values:
                current_values.insert(0, display_text)
                self.provider_pill.configure(values=current_values)
            self.provider_pill.set(display_text)

    def update_cost_badge(self, cost_text: str):
        """Updates cost badge text."""
        self.lbl_cost_val.configure(text=cost_text)

    def update_threads_badge(self, thread_count: int):
        """Updates thread count display."""
        self.lbl_threads_val.configure(text=f"Threads  {thread_count}")

    def _on_preset_selected(self, preset_name: str):
        """Callback when user picks a preset or model from top toolbar dropdown."""
        if self.on_preset_change:
            self.on_preset_change(preset_name)

    def _handle_theme_toggle(self):
        """Triggers theme toggle callback."""
        self.on_theme_toggle()
        theme_icon = "☀️" if self.theme_mgr.mode == "Light" else "🌙"
        self.btn_theme_toggle.configure(text=theme_icon)

    def _handle_primary_action(self):
        """Triggers main generation action."""
        if self.on_primary_action:
            self.on_primary_action()
