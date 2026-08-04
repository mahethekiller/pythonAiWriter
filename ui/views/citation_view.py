"""
Dedicated AI Search Visibility & Citation Tracker View.
Allows users to test if their brand or URL is cited in ChatGPT, Gemini, and Perplexity search answers.
"""

import customtkinter as ctk


def build_citation_view(app, parent_container):
    """Builds the dedicated AI Citation Tracker view."""
    colors = app.theme_mgr.colors

    card_cit = ctk.CTkFrame(
        parent_container,
        fg_color=colors["bg_card"],
        border_width=1,
        border_color=colors["border"],
        corner_radius=12
    )
    card_cit.pack(fill="x", padx=14, pady=(14, 8))

    ctk.CTkLabel(
        card_cit,
        text="🤖 AI Search Visibility & Citation Tracker",
        font=ctk.CTkFont(size=14, weight="bold"),
        text_color=colors["text_primary"]
    ).pack(anchor="w", padx=18, pady=(16, 4))

    ctk.CTkLabel(
        card_cit,
        text="Track whether your brand or website URL is cited in AI search responses (ChatGPT, Google Gemini, Perplexity) for target industry keywords.",
        font=ctk.CTkFont(size=11),
        text_color=colors["text_secondary"]
    ).pack(anchor="w", padx=18, pady=(0, 12))

    row_brand = ctk.CTkFrame(card_cit, fg_color="transparent")
    row_brand.pack(fill="x", padx=18, pady=(0, 8))

    ctk.CTkLabel(row_brand, text="Brand / Website Domain:", font=ctk.CTkFont(weight="bold"), text_color=colors["text_primary"], width=160, anchor="w").pack(side="left")
    app.cit_brand_entry = ctk.CTkEntry(
        row_brand,
        placeholder_text="e.g. mybrand.com or PythonAiWriter",
        height=36,
        fg_color=colors["bg_input"],
        border_color=colors["border"],
        text_color=colors["text_primary"]
    )
    app.cit_brand_entry.pack(side="left", fill="x", expand=True)

    row_kw = ctk.CTkFrame(card_cit, fg_color="transparent")
    row_kw.pack(fill="x", padx=18, pady=(0, 12))

    ctk.CTkLabel(row_kw, text="Target Industry Keyword:", font=ctk.CTkFont(weight="bold"), text_color=colors["text_primary"], width=160, anchor="w").pack(side="left")
    app.cit_kw_entry = ctk.CTkEntry(
        row_kw,
        placeholder_text="e.g. AI content rewriting software",
        height=36,
        fg_color=colors["bg_input"],
        border_color=colors["border"],
        text_color=colors["text_primary"]
    )
    app.cit_kw_entry.pack(side="left", fill="x", expand=True)

    row_act = ctk.CTkFrame(card_cit, fg_color="transparent")
    row_act.pack(fill="x", padx=18, pady=(0, 14))

    btn_check_cit = ctk.CTkButton(
        row_act,
        text="🤖 Test AI Search Visibility Now",
        command=app._run_ai_citation_check,
        height=40,
        font=ctk.CTkFont(size=12, weight="bold"),
        fg_color=colors["primary"],
        hover_color=colors["primary_hover"],
        text_color="#FFFFFF"
    )
    btn_check_cit.pack(fill="x")

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
        text="📊 AI Citation Report & Model Response:",
        font=ctk.CTkFont(size=12, weight="bold"),
        text_color=colors["text_primary"]
    ).pack(anchor="w", padx=18, pady=(12, 4))

    app.cit_output_textbox = ctk.CTkTextbox(
        card_res,
        height=200,
        fg_color=colors["bg_input"],
        border_width=1,
        border_color=colors["border"],
        text_color=colors["text_primary"]
    )
    app.cit_output_textbox.insert("1.0", "Click 'Test AI Search Visibility Now' to query AI engines...")
    app.cit_output_textbox.pack(fill="x", padx=18, pady=(0, 14))
