"""
Rewriter Studio View construction with crisp high-contrast button text across all themes and states.
"""

import customtkinter as ctk


def build_dashboard_view(app, parent_container):
    """Builds all UI cards and controls for the Rewriter Studio view."""
    colors = app.theme_mgr.colors
    
    # Card 1: Target Webpage URLs Input Section
    app.input_frame = ctk.CTkFrame(
        parent_container, 
        fg_color=colors["bg_card"], 
        border_width=1, 
        border_color=colors["border"], 
        corner_radius=12
    )
    app.input_frame.pack(fill="x", padx=14, pady=(14, 8))

    header_subframe = ctk.CTkFrame(app.input_frame, fg_color="transparent")
    header_subframe.pack(fill="x", padx=16, pady=(14, 6))

    ctk.CTkLabel(
        header_subframe, 
        text="🌐 Target Webpage URLs (one per line):", 
        font=ctk.CTkFont(size=13, weight="bold"),
        text_color=colors["text_primary"]
    ).pack(side="left")

    info_urls_btn = ctk.CTkButton(
        header_subframe, 
        text="ℹ️", 
        width=28, 
        height=24, 
        fg_color=colors["bg_card_hover"], 
        hover_color=colors["border"],
        text_color=colors["text_primary"],
        command=lambda: app.show_info_popup(
            "Target Webpage URLs",
            "Enter one or more web page URLs to scrape and rewrite.\n\n"
            "Examples:\n"
            "https://example.com/blog/article-1\n"
            "https://example.com/about-us\n\n"
            "Each URL will be fetched, processed concurrently, and saved to your dated output folder."
        )
    )
    info_urls_btn.pack(side="left", padx=8)

    app.urls_textbox = ctk.CTkTextbox(
        app.input_frame, 
        height=100, 
        font=ctk.CTkFont(family="Consolas", size=11),
        fg_color=colors["bg_input"],
        border_width=1,
        border_color=colors["border"],
        text_color=colors["text_primary"],
        corner_radius=8
    )
    app.urls_textbox.pack(fill="x", padx=16, pady=(0, 14))

    # Card 2: Custom Prompt Instructions Section
    app.instruction_frame = ctk.CTkFrame(
        parent_container, 
        fg_color=colors["bg_card"], 
        border_width=1, 
        border_color=colors["border"], 
        corner_radius=12
    )
    app.instruction_frame.pack(fill="x", padx=14, pady=8)

    app.custom_prompt_var = ctk.BooleanVar(value=False)
    app.custom_prompt_checkbox = ctk.CTkCheckBox(
        app.instruction_frame, 
        text="💡 Add Custom Prompt Instructions", 
        variable=app.custom_prompt_var,
        command=app._toggle_custom_prompt,
        font=ctk.CTkFont(size=13, weight="bold"),
        fg_color=colors["primary"],
        text_color=colors["text_primary"]
    )
    app.custom_prompt_checkbox.pack(anchor="w", padx=16, pady=12)

    app.custom_prompt_textbox = ctk.CTkTextbox(
        app.instruction_frame, 
        height=50,
        fg_color=colors["bg_input"],
        border_width=1,
        border_color=colors["border"],
        text_color=colors["text_primary"],
        corner_radius=8
    )
    app.custom_prompt_textbox.insert("1.0", "Focus on technical clarity, punchy headers, and concise sentences.")
    app.custom_prompt_textbox.configure(state="disabled")
    app.custom_prompt_textbox.pack(fill="x", padx=16, pady=(0, 14))

    # Card 3: Action & Export Options Section
    app.action_frame = ctk.CTkFrame(
        parent_container, 
        fg_color=colors["bg_card"], 
        border_width=1, 
        border_color=colors["border"], 
        corner_radius=12
    )
    app.action_frame.pack(fill="x", padx=14, pady=8)

    # Rewriting Execution Mode Selection Row
    app.mode_subframe = ctk.CTkFrame(app.action_frame, fg_color="transparent")
    app.mode_subframe.pack(fill="x", padx=16, pady=(14, 4))

    ctk.CTkLabel(
        app.mode_subframe, 
        text="⚡ Rewriter Execution Mode:", 
        font=ctk.CTkFont(size=13, weight="bold"),
        text_color=colors["text_primary"]
    ).pack(side="left", padx=(0, 10))

    app.mode_combo = ctk.CTkComboBox(
        app.mode_subframe, 
        values=["Layout-Preserving HTML", "Semantic HTML Clean rewrite"],
        command=lambda selected: app._update_config_status_label(),
        width=260,
        fg_color=colors["bg_input"],
        border_color=colors["border"],
        button_color=colors["border"],
        dropdown_fg_color=colors["bg_card"],
        text_color=colors["text_primary"]
    )
    app.mode_combo.set("Layout-Preserving HTML")
    app.mode_combo.pack(side="left", padx=5)

    info_mode_btn = ctk.CTkButton(
        app.mode_subframe, 
        text="ℹ️", 
        width=28, 
        height=24, 
        fg_color=colors["bg_card_hover"], 
        hover_color=colors["border"],
        text_color=colors["text_primary"],
        command=lambda: app.show_info_popup(
            "Rewriter Execution Modes",
            "1. Layout-Preserving HTML:\n"
            "   Extracts text nodes while preserving 100% of original CSS styles, classes, IDs, DOM structure, and page layout.\n\n"
            "2. Semantic HTML Clean rewrite:\n"
            "   Extracts core article content (headings, paragraphs, lists) and rewrites it into clean semantic HTML without original page styling."
        )
    )
    info_mode_btn.pack(side="left", padx=5)

    # Header / Footer Navigation Option Row
    app.hf_subframe = ctk.CTkFrame(app.action_frame, fg_color="transparent")
    app.hf_subframe.pack(fill="x", padx=16, pady=(4, 4))

    app.include_header_footer_var = ctk.BooleanVar(value=False)
    app.include_header_footer_checkbox = ctk.CTkCheckBox(
        app.hf_subframe, 
        text="📌 Include Header & Footer Navigation Elements", 
        variable=app.include_header_footer_var,
        font=ctk.CTkFont(size=12, weight="bold"),
        fg_color=colors["primary"],
        text_color=colors["text_primary"]
    )
    app.include_header_footer_checkbox.pack(side="left")

    app.formats_subframe = ctk.CTkFrame(app.action_frame, fg_color="transparent")
    app.formats_subframe.pack(fill="x", padx=16, pady=(4, 6))

    ctk.CTkLabel(
        app.formats_subframe, 
        text="SEO Export Formats:", 
        font=ctk.CTkFont(size=13, weight="bold"),
        text_color=colors["text_primary"]
    ).pack(side="left", padx=(0, 12))

    app.html_var = ctk.BooleanVar(value=True)
    app.docx_var = ctk.BooleanVar(value=True)

    app.html_checkbox = ctk.CTkCheckBox(
        app.formats_subframe, 
        text="WordPress HTML (.html)", 
        variable=app.html_var,
        fg_color=colors["primary"],
        text_color=colors["text_primary"]
    )
    app.html_checkbox.pack(side="left", padx=10)

    app.docx_checkbox = ctk.CTkCheckBox(
        app.formats_subframe, 
        text="Word (.docx)", 
        variable=app.docx_var,
        fg_color=colors["primary"],
        text_color=colors["text_primary"]
    )
    app.docx_checkbox.pack(side="left", padx=10)

    # Start Action Button
    app.start_btn = ctk.CTkButton(
        app.action_frame, 
        text="🚀 Start Batch Rewriting", 
        font=ctk.CTkFont(size=14, weight="bold"),
        command=app._start_processing,
        height=40,
        fg_color=colors["primary"],
        hover_color=colors["primary_hover"],
        text_color="#FFFFFF",
        text_color_disabled="#E5E7EB",
        corner_radius=8
    )
    app.start_btn.pack(fill="x", padx=16, pady=14)

    # Card 3B: Screaming Frog Technical SEO Audit Runner
    app.sf_card = ctk.CTkFrame(
        parent_container,
        fg_color=colors["bg_card"],
        border_width=1,
        border_color=colors["border"],
        corner_radius=12
    )
    app.sf_card.pack(fill="x", padx=14, pady=8)

    sf_row = ctk.CTkFrame(app.sf_card, fg_color="transparent")
    sf_row.pack(fill="x", padx=16, pady=12)

    ctk.CTkLabel(sf_row, text="🐸 Screaming Frog Technical Audit:", font=ctk.CTkFont(size=12, weight="bold"), text_color=colors["text_primary"]).pack(side="left", padx=(0, 10))
    app.sf_audit_url_entry = ctk.CTkEntry(sf_row, placeholder_text="Target Site URL (e.g. https://myblog.com)...", width=300, fg_color=colors["bg_input"], border_color=colors["border"], text_color=colors["text_primary"])
    app.sf_audit_url_entry.pack(side="left", padx=(0, 10))

    btn_run_sf_audit = ctk.CTkButton(
        sf_row,
        text="🚀 Run Technical Audit",
        command=app._run_screaming_frog_audit,
        height=32,
        font=ctk.CTkFont(size=11, weight="bold"),
        fg_color=colors["primary"],
        hover_color=colors["primary_hover"],
        text_color="#FFFFFF"
    )
    btn_run_sf_audit.pack(side="left")

    # Card 4: Activity Logs Console Panel
    app.log_frame = ctk.CTkFrame(
        parent_container, 
        fg_color=colors["bg_card"], 
        border_width=1, 
        border_color=colors["border"], 
        corner_radius=12
    )
    app.log_frame.pack(fill="x", padx=14, pady=8)

    ctk.CTkLabel(
        app.log_frame, 
        text="Activity Logs:", 
        font=ctk.CTkFont(size=12, weight="bold"),
        text_color=colors["text_accent"]
    ).pack(anchor="w", padx=16, pady=(10, 4))

    app.log_textbox = ctk.CTkTextbox(
        app.log_frame, 
        height=90, 
        font=ctk.CTkFont(family="Consolas", size=11),
        fg_color=colors["bg_input"],
        border_width=1,
        border_color=colors["border"],
        text_color=colors["text_primary"],
        corner_radius=8
    )
    app.log_textbox.pack(fill="x", padx=16, pady=(0, 12))

    # Card 5: Bottom Output Shortcut Buttons (High contrast text visibility!)
    app.bottom_frame = ctk.CTkFrame(parent_container, fg_color="transparent")
    app.bottom_frame.pack(fill="x", padx=14, pady=(6, 16))

    app.open_folder_btn = ctk.CTkButton(
        app.bottom_frame, 
        text="📁 Open Dated Folder", 
        command=app._open_output_folder, 
        state="disabled",
        width=170,
        height=36,
        font=ctk.CTkFont(size=12, weight="bold"),
        fg_color=colors["primary"],
        hover_color=colors["primary_hover"],
        text_color="#FFFFFF",
        text_color_disabled=("#9CA3AF", "#6B7280")
    )
    app.open_folder_btn.pack(side="left", padx=(0, 8))

    app.open_excel_btn = ctk.CTkButton(
        app.bottom_frame, 
        text="📊 Open Excel Report", 
        command=app._open_excel_file, 
        state="disabled",
        width=170,
        height=36,
        font=ctk.CTkFont(size=12, weight="bold"),
        fg_color=colors["bg_card"],
        hover_color=colors["bg_card_hover"],
        border_width=1,
        border_color=colors["border"],
        text_color=colors["text_primary"],
        text_color_disabled=("#9CA3AF", "#6B7280")
    )
    app.open_excel_btn.pack(side="left", padx=(0, 8))

    app.open_cost_btn = ctk.CTkButton(
        app.bottom_frame, 
        text="📄 Open Cost Report", 
        command=app._open_cost_file, 
        state="disabled",
        width=170,
        height=36,
        font=ctk.CTkFont(size=12, weight="bold"),
        fg_color=colors["bg_card"],
        hover_color=colors["bg_card_hover"],
        border_width=1,
        border_color=colors["border"],
        text_color=colors["text_primary"],
        text_color_disabled=("#9CA3AF", "#6B7280")
    )
    app.open_cost_btn.pack(side="left")

    # Hidden compatibility elements
    app.status_info_frame = ctk.CTkFrame(parent_container, fg_color="transparent")
    app.config_status_label = ctk.CTkLabel(parent_container, text="")
    app.dash_cost_badge = ctk.CTkLabel(parent_container, text="")
    app.step_tracker_frame = ctk.CTkFrame(parent_container, fg_color="transparent")
    app.step_tracker_label = ctk.CTkLabel(parent_container, text="")
    app.progress_frame = ctk.CTkFrame(parent_container, fg_color="transparent")
    app.progress_bar = ctk.CTkProgressBar(parent_container)
    app.status_lbl = ctk.CTkLabel(parent_container, text="")
