"""
Dedicated SERP & Competitor Intelligence View.
Allows users to enter a keyword, mine Google/SerpAPI competitor headings, and extract PAA questions.
"""

import customtkinter as ctk


def build_serp_view(app, parent_container):
    """Builds the dedicated SERP Intelligence & Competitor Research view."""
    colors = app.theme_mgr.colors

    card_serp = ctk.CTkFrame(
        parent_container,
        fg_color=colors["bg_card"],
        border_width=1,
        border_color=colors["border"],
        corner_radius=12
    )
    card_serp.pack(fill="x", padx=14, pady=(14, 8))

    ctk.CTkLabel(
        card_serp,
        text="🔍 SERP Intelligence & Competitor Research Suite",
        font=ctk.CTkFont(size=14, weight="bold"),
        text_color=colors["text_primary"]
    ).pack(anchor="w", padx=18, pady=(16, 4))

    ctk.CTkLabel(
        card_serp,
        text="Query live search engine results (SerpAPI / Google) to extract top 10 competitor headings, word count averages, and People Also Ask questions.",
        font=ctk.CTkFont(size=11),
        text_color=colors["text_secondary"]
    ).pack(anchor="w", padx=18, pady=(0, 12))

    row_kw = ctk.CTkFrame(card_serp, fg_color="transparent")
    row_kw.pack(fill="x", padx=18, pady=(0, 14))

    ctk.CTkLabel(row_kw, text="Primary Keyword:", font=ctk.CTkFont(weight="bold"), text_color=colors["text_primary"]).pack(side="left", padx=(0, 10))
    app.serp_kw_entry = ctk.CTkEntry(row_kw, placeholder_text="e.g. budget student laptops", width=340, height=36, fg_color=colors["bg_input"], border_color=colors["border"], text_color=colors["text_primary"])
    app.serp_kw_entry.pack(side="left", padx=(0, 10))

    btn_fetch_serp = ctk.CTkButton(
        row_kw,
        text="🔍 Fetch SERP Intel Now",
        command=app._run_standalone_serp_research,
        height=36,
        font=ctk.CTkFont(size=12, weight="bold"),
        fg_color=colors["primary"],
        hover_color=colors["primary_hover"],
        text_color="#FFFFFF"
    )
    btn_fetch_serp.pack(side="left")

    # Results Textbox
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
        text="📊 SERP Intel Results & Competitor Headings:",
        font=ctk.CTkFont(size=12, weight="bold"),
        text_color=colors["text_primary"]
    ).pack(anchor="w", padx=18, pady=(12, 4))

    app.serp_output_textbox = ctk.CTkTextbox(
        card_res,
        height=220,
        fg_color=colors["bg_input"],
        border_width=1,
        border_color=colors["border"],
        text_color=colors["text_primary"]
    )
    app.serp_output_textbox.insert("1.0", "Click 'Fetch SERP Intel Now' to inspect live Google rankings, competitor headings, and People Also Ask questions...")
    app.serp_output_textbox.pack(fill="x", padx=18, pady=(0, 14))
