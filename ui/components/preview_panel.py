"""
Right Live Preview & SEO Score Sidebar Component with native CustomTkinter Light/Dark tuple color support.
"""

import re
import customtkinter as ctk
from typing import Dict, Any, Callable


class PreviewPanelComponent(ctk.CTkFrame):
    """Right Sidebar Live Preview & SEO Metrics Panel matching design mockup."""

    def __init__(self, parent, theme_mgr, callbacks: Dict[str, Callable[[], None]] = None, **kwargs):
        colors = theme_mgr.colors
        super().__init__(
            parent, 
            fg_color=colors["bg_app"], 
            width=280, 
            corner_radius=0, 
            border_width=1,
            border_color=colors["border"],
            **kwargs
        )
        
        self.theme_mgr = theme_mgr
        self.callbacks = callbacks or {}
        self.active_tab = "seo"

        self._build_ui()

    def _build_ui(self):
        """Constructs tab headers, metric stats, circular score gauge, and execution indicators."""
        colors = self.theme_mgr.colors

        # 1. Top Tab Selector Line (Live Preview | SEO Score)
        self.tabs_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.tabs_frame.pack(fill="x", padx=14, pady=(16, 12))

        self.btn_tab_seo = ctk.CTkButton(
            self.tabs_frame,
            text="SEO Score",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="transparent",
            text_color=colors["primary"],
            hover_color=colors["bg_card_hover"],
            height=32,
            command=lambda: self._select_tab("seo")
        )
        self.btn_tab_seo.pack(side="left", fill="x", expand=True, padx=(0, 2))

        self.btn_tab_preview = ctk.CTkButton(
            self.tabs_frame,
            text="Live Preview",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="transparent",
            text_color=colors["text_muted"],
            hover_color=colors["bg_card_hover"],
            height=32,
            command=lambda: self._select_tab("preview")
        )
        self.btn_tab_preview.pack(side="right", fill="x", expand=True, padx=(2, 0))

        # Underline indicator
        self.tab_underline = ctk.CTkFrame(self, fg_color=colors["primary"], height=2)
        self.tab_underline.pack(fill="x", padx=14, pady=(0, 14))

        # 2. Container for SEO Score Tab
        self.seo_container = ctk.CTkFrame(self, fg_color="transparent")
        self.seo_container.pack(fill="both", expand=True, padx=14, pady=0)

        # Estimated Words & Reading Time Row
        self.row_words_time = ctk.CTkFrame(self.seo_container, fg_color="transparent")
        self.row_words_time.pack(fill="x", pady=(0, 10))

        words_col = ctk.CTkFrame(self.row_words_time, fg_color="transparent")
        words_col.pack(side="left", fill="both", expand=True)

        ctk.CTkLabel(words_col, text="Estimated Words", font=ctk.CTkFont(size=10, weight="bold"), text_color=colors["text_muted"]).pack(anchor="w")
        self.lbl_words_val = ctk.CTkLabel(words_col, text="-", font=ctk.CTkFont(size=18, weight="bold"), text_color=colors["text_primary"])
        self.lbl_words_val.pack(anchor="w")

        time_col = ctk.CTkFrame(self.row_words_time, fg_color="transparent")
        time_col.pack(side="left", fill="both", expand=True)

        ctk.CTkLabel(time_col, text="Reading Time", font=ctk.CTkFont(size=10, weight="bold"), text_color=colors["text_muted"]).pack(anchor="w")
        self.lbl_reading_time_val = ctk.CTkLabel(time_col, text="-", font=ctk.CTkFont(size=18, weight="bold"), text_color=colors["text_primary"])
        self.lbl_reading_time_val.pack(anchor="w")

        # 3. Circular SEO Score Gauge Card
        self.gauge_card = ctk.CTkFrame(
            self.seo_container,
            fg_color=colors["bg_card"],
            border_width=1,
            border_color=colors["border"],
            corner_radius=12
        )
        self.gauge_card.pack(fill="x", pady=10)

        gauge_inner = ctk.CTkFrame(self.gauge_card, fg_color="transparent")
        gauge_inner.pack(padx=16, pady=16)

        self.lbl_gauge_title = ctk.CTkLabel(
            gauge_inner,
            text="SEO Score",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=colors["text_muted"]
        )
        self.lbl_gauge_title.pack(anchor="center")

        # Score Circle / Pill Display
        self.score_pill = ctk.CTkLabel(
            gauge_inner,
            text="-",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=colors["text_muted"],
            width=80,
            height=80,
            fg_color=colors["bg_app"],
            corner_radius=40
        )
        self.score_pill.pack(anchor="center", pady=6)

        self.lbl_gauge_rating = ctk.CTkLabel(
            gauge_inner,
            text="Idle / Ready",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=colors["text_muted"]
        )
        self.lbl_gauge_rating.pack(anchor="center")

        # 4. Keyword Density Progress Bar Card
        self.density_card = ctk.CTkFrame(self.seo_container, fg_color="transparent")
        self.density_card.pack(fill="x", pady=8)

        density_top = ctk.CTkFrame(self.density_card, fg_color="transparent")
        density_top.pack(fill="x", pady=(0, 2))

        ctk.CTkLabel(density_top, text="Keyword Density", font=ctk.CTkFont(size=11, weight="bold"), text_color=colors["text_muted"]).pack(side="left")
        self.lbl_density_val = ctk.CTkLabel(density_top, text="0.0%", font=ctk.CTkFont(size=12, weight="bold"), text_color=colors["text_primary"])
        self.lbl_density_val.pack(side="right")

        self.density_bar = ctk.CTkProgressBar(self.density_card, height=6, progress_color=colors["primary"], fg_color=colors["border"])
        self.density_bar.set(0.0)
        self.density_bar.pack(fill="x")

        # 5. Readability Score Progress Bar Card
        self.readability_card = ctk.CTkFrame(self.seo_container, fg_color="transparent")
        self.readability_card.pack(fill="x", pady=8)

        readability_top = ctk.CTkFrame(self.readability_card, fg_color="transparent")
        readability_top.pack(fill="x", pady=(0, 2))

        ctk.CTkLabel(readability_top, text="Readability Score", font=ctk.CTkFont(size=11, weight="bold"), text_color=colors["text_muted"]).pack(side="left")
        self.lbl_readability_val = ctk.CTkLabel(readability_top, text="0", font=ctk.CTkFont(size=12, weight="bold"), text_color=colors["text_primary"])
        self.lbl_readability_val.pack(side="right")

        self.readability_bar = ctk.CTkProgressBar(self.readability_card, height=6, progress_color=colors["primary"], fg_color=colors["border"])
        self.readability_bar.set(0.0)
        self.readability_bar.pack(fill="x")

        # Separator Line
        self.sep2 = ctk.CTkFrame(self.seo_container, fg_color=colors["border"], height=1)
        self.sep2.pack(fill="x", pady=10)

        # 6. Detailed Output Metrics Grid
        self.grid_details = ctk.CTkFrame(self.seo_container, fg_color="transparent")
        self.grid_details.pack(fill="x", pady=4)

        # Est. Cost
        ctk.CTkLabel(self.grid_details, text="Est. Cost", font=ctk.CTkFont(size=10, weight="bold"), text_color=colors["text_muted"]).grid(row=0, column=0, sticky="w", pady=3)
        self.lbl_cost_val = ctk.CTkLabel(self.grid_details, text="$0.000", font=ctk.CTkFont(size=11, weight="bold"), text_color=colors["text_primary"])
        self.lbl_cost_val.grid(row=1, column=0, sticky="w", pady=(0, 6))

        # AI Provider
        ctk.CTkLabel(self.grid_details, text="AI Provider", font=ctk.CTkFont(size=10, weight="bold"), text_color=colors["text_muted"]).grid(row=0, column=1, sticky="w", padx=(20, 0), pady=3)
        self.lbl_prov_val = ctk.CTkLabel(self.grid_details, text="OpenAI gpt-4o-mini", font=ctk.CTkFont(size=11, weight="bold"), text_color=colors["text_primary"])
        self.lbl_prov_val.grid(row=1, column=1, sticky="w", padx=(20, 0), pady=(0, 6))

        # Generation Time
        ctk.CTkLabel(self.grid_details, text="Generation Time", font=ctk.CTkFont(size=10, weight="bold"), text_color=colors["text_muted"]).grid(row=2, column=0, sticky="w", pady=3)
        self.lbl_time_val = ctk.CTkLabel(self.grid_details, text="0 sec", font=ctk.CTkFont(size=11, weight="bold"), text_color=colors["text_primary"])
        self.lbl_time_val.grid(row=3, column=0, sticky="w", pady=(0, 6))

        # Status
        ctk.CTkLabel(self.grid_details, text="Status", font=ctk.CTkFont(size=10, weight="bold"), text_color=colors["text_muted"]).grid(row=2, column=1, sticky="w", padx=(20, 0), pady=3)
        self.lbl_status_val = ctk.CTkLabel(self.grid_details, text="⚪ Ready", font=ctk.CTkFont(size=11, weight="bold"), text_color=colors["text_muted"])
        self.lbl_status_val.grid(row=3, column=1, sticky="w", padx=(20, 0), pady=(0, 6))

        # 7. Container for Live Preview Tab (Hidden by default)
        self.preview_container = ctk.CTkFrame(self, fg_color="transparent")

        self.lbl_preview_title = ctk.CTkLabel(
            self.preview_container,
            text="📄 Article Text Preview",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=colors["text_primary"]
        )
        self.lbl_preview_title.pack(anchor="w", pady=(0, 6))

        self.preview_textbox = ctk.CTkTextbox(
            self.preview_container,
            fg_color=colors["bg_card"],
            border_width=1,
            border_color=colors["border"],
            font=ctk.CTkFont(size=11),
            text_color=colors["text_primary"],
            wrap="word"
        )
        self.preview_textbox.insert("1.0", "Your generated article text preview will appear here after generation...")
        self.preview_textbox.pack(fill="both", expand=True, pady=(0, 10))

        # Publish to WordPress Action Button
        self.btn_wp_publish = ctk.CTkButton(
            self.preview_container,
            text="🌐 Publish to WordPress",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=lambda: self.callbacks.get("on_wp_publish", lambda: None)(),
            height=34,
            fg_color=colors["primary"],
            hover_color=colors["primary_hover"],
            text_color="#FFFFFF"
        )
        self.btn_wp_publish.pack(fill="x", pady=(0, 6))

    def _select_tab(self, tab_id: str):
        """Switches right sidebar tabs between SEO Score and Live Preview."""
        self.active_tab = tab_id
        colors = self.theme_mgr.colors
        if tab_id == "seo":
            self.btn_tab_seo.configure(text_color=colors["primary"])
            self.btn_tab_preview.configure(text_color=colors["text_muted"])
            self.preview_container.pack_forget()
            self.seo_container.pack(fill="both", expand=True, padx=14, pady=0)
        else:
            self.btn_tab_seo.configure(text_color=colors["text_muted"])
            self.btn_tab_preview.configure(text_color=colors["primary"])
            self.seo_container.pack_forget()
            self.preview_container.pack(fill="both", expand=True, padx=14, pady=0)

    def set_preview_content(self, text_content: str):
        """Updates Live Preview tab text content formatted cleanly without raw HTML tags."""
        clean = text_content or ""
        if "<" in clean and ">" in clean:
            clean = re.sub(r'<h1>(.*?)</h1>', r'# \1\n\n', clean, flags=re.IGNORECASE | re.DOTALL)
            clean = re.sub(r'<h2>(.*?)</h2>', r'\n## \1\n', clean, flags=re.IGNORECASE | re.DOTALL)
            clean = re.sub(r'<h3>(.*?)</h3>', r'\n### \1\n', clean, flags=re.IGNORECASE | re.DOTALL)
            clean = re.sub(r'<p>(.*?)</p>', r'\1\n\n', clean, flags=re.IGNORECASE | re.DOTALL)
            clean = re.sub(r'<li>(.*?)</li>', r'• \1\n', clean, flags=re.IGNORECASE | re.DOTALL)
            clean = re.sub(r'<br\s*/?>', r'\n', clean, flags=re.IGNORECASE)
            clean = re.sub(r'<strong>(.*?)</strong>', r'**\1**', clean, flags=re.IGNORECASE | re.DOTALL)
            clean = re.sub(r'<em>(.*?)</em>', r'*\1*', clean, flags=re.IGNORECASE | re.DOTALL)
            clean = re.sub(r'<[^>]+>', '', clean)
            clean = re.sub(r'\n{3,}', '\n\n', clean).strip()

        self.preview_textbox.configure(state="normal")
        self.preview_textbox.delete("1.0", "end")
        self.preview_textbox.insert("1.0", clean)
        self.preview_textbox.see("1.0")

    def reset_to_idle(self, provider_str: str = "OpenAI gpt-4o-mini", cost_str: str = "$0.000"):
        """Resets panel to clean initial state before generation."""
        colors = self.theme_mgr.colors
        self.lbl_words_val.configure(text="-")
        self.lbl_reading_time_val.configure(text="-")
        self.score_pill.configure(text="-", text_color=colors["text_muted"])
        self.lbl_gauge_rating.configure(text="Idle / Ready", text_color=colors["text_muted"])
        self.lbl_density_val.configure(text="0.0%")
        self.density_bar.set(0.0)
        self.lbl_readability_val.configure(text="0")
        self.readability_bar.set(0.0)
        self.lbl_cost_val.configure(text=cost_str)
        self.lbl_prov_val.configure(text=provider_str)
        self.lbl_time_val.configure(text="0 sec")
        self.lbl_status_val.configure(text="⚪ Ready", text_color=colors["text_muted"])

    def update_metrics(
        self, 
        words: int, 
        reading_time_min: int, 
        seo_score: int, 
        density: float, 
        readability: int, 
        cost_str: str, 
        provider_str: str, 
        duration_sec: int, 
        status_str: str
    ):
        """Updates all live metrics on right panel with calculated data."""
        colors = self.theme_mgr.colors

        self.lbl_words_val.configure(text=f"{words:,}")
        self.lbl_reading_time_val.configure(text=f"{reading_time_min} min")
        
        self.score_pill.configure(text=str(seo_score))
        if seo_score >= 80:
            self.score_pill.configure(text_color=colors["success"])
            self.lbl_gauge_rating.configure(text="Excellent", text_color=colors["success"])
        elif seo_score >= 60:
            self.score_pill.configure(text_color=colors["warning"])
            self.lbl_gauge_rating.configure(text="Good", text_color=colors["warning"])
        else:
            self.score_pill.configure(text_color=colors["danger"])
            self.lbl_gauge_rating.configure(text="Needs Audit", text_color=colors["danger"])

        self.lbl_density_val.configure(text=f"{density:.1f}%")
        self.density_bar.set(min(1.0, density / 2.5))

        self.lbl_readability_val.configure(text=str(int(readability)))
        self.readability_bar.set(min(1.0, readability / 100.0))

        self.lbl_cost_val.configure(text=cost_str)
        self.lbl_prov_val.configure(text=provider_str)
        self.lbl_time_val.configure(text=f"{duration_sec} sec")
        self.lbl_status_val.configure(text=status_str, text_color=colors["success"])
