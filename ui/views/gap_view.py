"""
Dedicated Keyword & Content Gap Analysis View (Semrush Gap Analytics).
Allows users to compare their target URL against up to 4 competitor URLs.
"""

import customtkinter as ctk


def build_gap_view(app, parent_container):
    """Builds the dedicated Keyword & Content Gap Analysis view."""
    colors = app.theme_mgr.colors

    card_gap = ctk.CTkFrame(
        parent_container,
        fg_color=colors["bg_card"],
        border_width=1,
        border_color=colors["border"],
        corner_radius=12
    )
    card_gap.pack(fill="x", padx=14, pady=(14, 8))

    ctk.CTkLabel(
        card_gap,
        text="📊 Head-to-Head Keyword & Content Gap Matrix",
        font=ctk.CTkFont(size=14, weight="bold"),
        text_color=colors["text_primary"]
    ).pack(anchor="w", padx=18, pady=(16, 4))

    ctk.CTkLabel(
        card_gap,
        text="Compare your target website URL against up to 4 competitor URLs to discover missing high-value keywords and subtopic gaps.",
        font=ctk.CTkFont(size=11),
        text_color=colors["text_secondary"]
    ).pack(anchor="w", padx=18, pady=(0, 12))

    # Target URL Entry
    row_target = ctk.CTkFrame(card_gap, fg_color="transparent")
    row_target.pack(fill="x", padx=18, pady=(0, 8))

    ctk.CTkLabel(row_target, text="Your Website URL:", font=ctk.CTkFont(weight="bold"), text_color=colors["text_primary"], width=140, anchor="w").pack(side="left")
    app.gap_target_url_entry = ctk.CTkEntry(
        row_target,
        placeholder_text="e.g. https://myblog.com/best-laptops",
        height=36,
        fg_color=colors["bg_input"],
        border_color=colors["border"],
        text_color=colors["text_primary"]
    )
    app.gap_target_url_entry.pack(side="left", fill="x", expand=True)

    # Competitors Textbox
    row_comps = ctk.CTkFrame(card_gap, fg_color="transparent")
    row_comps.pack(fill="x", padx=18, pady=(0, 12))

    ctk.CTkLabel(row_comps, text="Competitor URLs\n(1 per line):", font=ctk.CTkFont(weight="bold"), text_color=colors["text_primary"], width=140, anchor="w").pack(side="left", anchor="n")
    app.gap_comp_urls_textbox = ctk.CTkTextbox(
        row_comps,
        height=90,
        fg_color=colors["bg_input"],
        border_width=1,
        border_color=colors["border"],
        text_color=colors["text_primary"]
    )
    app.gap_comp_urls_textbox.insert("1.0", "https://competitor1.com/laptops-guide\nhttps://competitor2.com/student-laptops")
    app.gap_comp_urls_textbox.pack(side="left", fill="x", expand=True)

    # Action Button
    row_act = ctk.CTkFrame(card_gap, fg_color="transparent")
    row_act.pack(fill="x", padx=18, pady=(0, 14))

    btn_analyze_gap = ctk.CTkButton(
        row_act,
        text="📊 Run Keyword & Content Gap Analysis",
        command=app._run_semrush_gap_analysis,
        height=40,
        font=ctk.CTkFont(size=12, weight="bold"),
        fg_color=colors["primary"],
        hover_color=colors["primary_hover"],
        text_color="#FFFFFF"
    )
    btn_analyze_gap.pack(fill="x")

    # Gap Output Results
    card_res = ctk.CTkFrame(
        parent_container,
        fg_color=colors["bg_card"],
        border_width=1,
        border_color=colors["border"],
        corner_radius=12
    )
    card_res.pack(fill="x", padx=14, pady=8)

    ctk.CTkLabel(
        card_res,
        text="📈 Keyword Gap & Missing Subtopics Report:",
        font=ctk.CTkFont(size=12, weight="bold"),
        text_color=colors["text_primary"]
    ).pack(anchor="w", padx=18, pady=(12, 4))

    app.gap_output_textbox = ctk.CTkTextbox(
        card_res,
        height=200,
        fg_color=colors["bg_input"],
        border_width=1,
        border_color=colors["border"],
        text_color=colors["text_primary"]
    )
    app.gap_output_textbox.insert("1.0", "Click 'Run Keyword & Content Gap Analysis' to compare your site against competitors...")
    app.gap_output_textbox.pack(fill="x", padx=18, pady=(0, 14))
