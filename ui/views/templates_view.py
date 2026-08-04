"""
Strategy Presets & Templates View.
Interactive gallery for 1-click strategy presets (Affiliate Review, Educational Deep-Dive, Quick News Summary).
"""

import customtkinter as ctk


def build_templates_view(app, parent_container):
    """Builds the Strategy Presets gallery view."""
    
    # Header Card
    header_card = ctk.CTkFrame(
        parent_container,
        fg_color="#1E293B",
        border_width=1,
        border_color="#2B3648",
        corner_radius=10
    )
    header_card.pack(fill="x", padx=12, pady=(10, 6))

    ctk.CTkLabel(
        header_card,
        text="🎯 1-Click Strategy Presets Gallery",
        font=ctk.CTkFont(size=16, weight="bold"),
        text_color="#38BDF8"
    ).pack(anchor="w", padx=14, pady=(10, 2))

    ctk.CTkLabel(
        header_card,
        text="Select a pre-configured SEO strategy to instantly populate article parameters in the SEO Blog Creator.",
        font=ctk.CTkFont(size=11),
        text_color="#94A3B8"
    ).pack(anchor="w", padx=14, pady=(0, 10))

    # Presets List
    presets = [
        {
            "title": "🛍️ Affiliate Product Review",
            "subtitle": "Commercial Intent & High-Converting Persuasive Tone",
            "desc": "Optimized for buyer guides, product comparisons, and affiliate monetization. Automatically weaves commercial intent, pros/cons, and CTA closing sections.",
            "preset_text": "🛍️ Affiliate Product Review (Commercial Intent, Persuasive)"
        },
        {
            "title": "🎓 Educational Deep-Dive",
            "subtitle": "Informational Intent & Authoritative Ultimate Guide",
            "desc": "Long-form 2,500+ word ultimate guide format with comprehensive topic coverage, external authority reference links, and Schema-ready FAQ boxes.",
            "preset_text": "🎓 Educational Deep-Dive (Informational Intent, Authoritative)"
        },
        {
            "title": "⚡ Quick News Summary",
            "subtitle": "Short-Form ~800 Words & Punchy News Digest",
            "desc": "Fast-reading news summary format focusing on key takeaways, bulleted highlights, and concise paragraphs.",
            "preset_text": "⚡ Quick News Summary (Informational Intent, Short ~800 words)"
        }
    ]

    for p in presets:
        card = ctk.CTkFrame(
            parent_container,
            fg_color="#1E293B",
            border_width=1,
            border_color="#2B3648",
            corner_radius=10
        )
        card.pack(fill="x", padx=12, pady=6)

        title_lbl = ctk.CTkLabel(
            card,
            text=p["title"],
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#FFFFFF"
        )
        title_lbl.pack(anchor="w", padx=14, pady=(10, 2))

        sub_lbl = ctk.CTkLabel(
            card,
            text=p["subtitle"],
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#38BDF8"
        )
        sub_lbl.pack(anchor="w", padx=14, pady=(0, 4))

        desc_lbl = ctk.CTkLabel(
            card,
            text=p["desc"],
            font=ctk.CTkFont(size=11),
            text_color="#CBD5E1",
            justify="left"
        )
        desc_lbl.pack(anchor="w", padx=14, pady=(0, 10))

        apply_btn = ctk.CTkButton(
            card,
            text="🚀 Apply Strategy Preset",
            font=ctk.CTkFont(size=12, weight="bold"),
            height=32,
            fg_color="#4F7CFF",
            hover_color="#3B62E6",
            command=lambda preset_val=p["preset_text"]: _apply_preset_and_switch(app, preset_val)
        )
        apply_btn.pack(anchor="w", padx=14, pady=(0, 10))


def _apply_preset_and_switch(app, preset_val: str):
    """Applies strategy preset and switches navigation view to SEO Blog Creator."""
    if hasattr(app, "preset_combo"):
        app.preset_combo.set(preset_val)
        app._apply_blog_preset(preset_val)
    if hasattr(app, "sidebar"):
        app.sidebar.set_active("blog")
    if hasattr(app, "_show_view"):
        app._show_view("blog")
