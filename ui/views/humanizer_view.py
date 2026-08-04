"""
Dedicated AI Content Humanizer Studio View.
Allows users to paste any article text/HTML, strip AI cliché vocabulary, and run naturalization polish.
"""

import customtkinter as ctk


def build_humanizer_view(app, parent_container):
    """Builds the dedicated AI Content Humanizer Studio view."""
    colors = app.theme_mgr.colors

    # Card 1: Input Text Container
    card_input = ctk.CTkFrame(
        parent_container,
        fg_color=colors["bg_card"],
        border_width=1,
        border_color=colors["border"],
        corner_radius=12
    )
    card_input.pack(fill="x", padx=14, pady=(14, 8))

    ctk.CTkLabel(
        card_input,
        text="🛡️ AI Content Humanizer & Anti-Detection Studio",
        font=ctk.CTkFont(size=14, weight="bold"),
        text_color=colors["text_primary"]
    ).pack(anchor="w", padx=18, pady=(16, 4))

    ctk.CTkLabel(
        card_input,
        text="Paste any existing article HTML or draft text below to strip AI vocabulary clichés ('delve', 'tapestry', 'testament') and naturalize tone.",
        font=ctk.CTkFont(size=11),
        text_color=colors["text_secondary"]
    ).pack(anchor="w", padx=18, pady=(0, 12))

    app.humanizer_input_textbox = ctk.CTkTextbox(
        card_input,
        height=140,
        fg_color=colors["bg_input"],
        border_width=1,
        border_color=colors["border"],
        text_color=colors["text_primary"]
    )
    app.humanizer_input_textbox.insert("1.0", "<p>In the realm of modern digital marketing, content writing stands as a testament to innovation. It is important to note that delving into SEO strategies unveils a tapestry of growth...</p>")
    app.humanizer_input_textbox.pack(fill="x", padx=18, pady=(0, 14))

    # Card 2: Humanization Action Controls
    card_actions = ctk.CTkFrame(
        parent_container,
        fg_color=colors["bg_card"],
        border_width=1,
        border_color=colors["border"],
        corner_radius=12
    )
    card_actions.pack(fill="x", padx=14, pady=8)

    row_acts = ctk.CTkFrame(card_actions, fg_color="transparent")
    row_acts.pack(fill="x", padx=18, pady=14)

    btn_humanize_now = ctk.CTkButton(
        row_acts,
        text="⚡ Humanize & Naturalize Content Now",
        command=app._run_standalone_humanizer,
        height=40,
        font=ctk.CTkFont(size=12, weight="bold"),
        fg_color=colors["primary"],
        hover_color=colors["primary_hover"],
        text_color="#FFFFFF"
    )
    btn_humanize_now.pack(side="left", padx=(0, 10))

    # Card 3: Output Text Box
    card_output = ctk.CTkFrame(
        parent_container,
        fg_color=colors["bg_card"],
        border_width=1,
        border_color=colors["border"],
        corner_radius=12
    )
    card_output.pack(fill="x", padx=14, pady=8)

    ctk.CTkLabel(
        card_output,
        text="✨ Humanized Output Content:",
        font=ctk.CTkFont(size=12, weight="bold"),
        text_color=colors["text_primary"]
    ).pack(anchor="w", padx=18, pady=(12, 4))

    app.humanizer_output_textbox = ctk.CTkTextbox(
        card_output,
        height=140,
        fg_color=colors["bg_input"],
        border_width=1,
        border_color=colors["border"],
        text_color=colors["text_primary"]
    )
    app.humanizer_output_textbox.pack(fill="x", padx=18, pady=(0, 14))
