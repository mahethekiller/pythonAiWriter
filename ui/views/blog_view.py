"""
SEO Blog Creator View construction.
Displays all configuration sections on a single unified page with dynamic Single/Batch CSV mode swapping,
live Activity Logs console panel, and dated output shortcut buttons.
"""

import customtkinter as ctk


def build_blog_view(app, parent_container):
    """Builds the unified single-page SEO Blog Creator view."""
    blog_cfg = app.config_mgr.data.get("blog_config", {})
    colors = app.theme_mgr.colors

    # =========================================================================
    # CARD 1: CONTENT & TOPIC CONFIGURATION
    # =========================================================================
    app.card_topic = ctk.CTkFrame(
        parent_container,
        fg_color=colors["bg_card"],
        border_width=1,
        border_color=colors["border"],
        corner_radius=12
    )
    app.card_topic.pack(fill="x", padx=14, pady=(14, 8))

    # Header & Execution Mode Selector
    hdr_frame1 = ctk.CTkFrame(app.card_topic, fg_color="transparent")
    hdr_frame1.pack(fill="x", padx=18, pady=(16, 10))

    ctk.CTkLabel(
        hdr_frame1,
        text="✍️ Content & Topic Configuration",
        font=ctk.CTkFont(size=14, weight="bold"),
        text_color=colors["text_primary"]
    ).pack(side="left")

    app.blog_mode_var = ctk.StringVar(value="single")
    app.blog_single_radio = ctk.CTkRadioButton(
        hdr_frame1,
        text="Single Article Mode",
        variable=app.blog_mode_var,
        value="single",
        command=app._toggle_blog_mode,
        font=ctk.CTkFont(size=11, weight="bold"),
        fg_color=colors["primary"],
        text_color=colors["text_primary"]
    )
    app.blog_single_radio.pack(side="right", padx=(12, 0))

    app.blog_batch_radio = ctk.CTkRadioButton(
        hdr_frame1,
        text="Batch CSV Mode",
        variable=app.blog_mode_var,
        value="batch",
        command=app._toggle_blog_mode,
        font=ctk.CTkFont(size=11, weight="bold"),
        fg_color=colors["primary"],
        text_color=colors["text_primary"]
    )
    app.blog_batch_radio.pack(side="right", padx=12)

    # Grid Container for Inputs
    app.grid1 = ctk.CTkFrame(app.card_topic, fg_color="transparent")
    app.grid1.pack(fill="x", padx=18, pady=(0, 14))

    # Single Mode Line Elements
    app.blog_topic_label = ctk.CTkLabel(app.grid1, text="Article Topic / Title *", font=ctk.CTkFont(size=11, weight="bold"), text_color=colors["text_primary"])
    app.blog_topic_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 4))

    app.blog_topic_entry = ctk.CTkEntry(
        app.grid1,
        placeholder_text="10 Best Budget Laptops for College Students in 2026",
        height=36,
        fg_color=colors["bg_input"],
        border_color=colors["border"],
        text_color=colors["text_primary"]
    )
    app.blog_topic_entry.insert(0, "10 Best Budget Laptops for College Students in 2026")
    app.blog_topic_entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=(0, 10), pady=(0, 12))

    # Batch CSV Mode Line Elements (Swapped via _toggle_blog_mode)
    app.blog_csv_label = ctk.CTkLabel(app.grid1, text="Batch CSV File:", font=ctk.CTkFont(size=11, weight="bold"), text_color=colors["text_primary"])
    app.blog_csv_entry = ctk.CTkEntry(app.grid1, placeholder_text="Path to sample_batch_topics.csv...", height=36, fg_color=colors["bg_input"], border_color=colors["border"], text_color=colors["text_primary"])
    app.blog_csv_browse_btn = ctk.CTkButton(
        app.grid1, 
        text="📁 Browse CSV...", 
        command=app._browse_blog_csv, 
        height=36, 
        width=110,
        font=ctk.CTkFont(size=11, weight="bold"),
        fg_color=colors["bg_card"], 
        hover_color=colors["bg_card_hover"], 
        border_width=1,
        border_color=colors["border"],
        text_color=colors["text_primary"]
    )
    app.blog_csv_sample_btn = ctk.CTkButton(
        app.grid1, 
        text="📥 Sample CSV", 
        command=app._download_sample_csv, 
        height=36, 
        width=110,
        font=ctk.CTkFont(size=11, weight="bold"),
        fg_color=colors["primary"], 
        hover_color=colors["primary_hover"],
        text_color="#FFFFFF"
    )

    ctk.CTkLabel(app.grid1, text="Primary Focus Keyword *", font=ctk.CTkFont(size=11, weight="bold"), text_color=colors["text_primary"]).grid(row=0, column=2, sticky="w", pady=(0, 4))
    app.blog_pk_entry = ctk.CTkEntry(
        app.grid1,
        placeholder_text="budget student laptops",
        height=36,
        fg_color=colors["bg_input"],
        border_color=colors["border"],
        text_color=colors["text_primary"]
    )
    app.blog_pk_entry.insert(0, "budget student laptops")
    app.blog_pk_entry.grid(row=1, column=2, sticky="ew", padx=(0, 10), pady=(0, 12))

    ctk.CTkLabel(app.grid1, text="Search Intent", font=ctk.CTkFont(size=11, weight="bold"), text_color=colors["text_primary"]).grid(row=0, column=3, sticky="w", pady=(0, 4))
    app.blog_intent_combo = ctk.CTkComboBox(
        app.grid1,
        values=blog_cfg.get("intents", ["Informational", "Commercial", "Transactional", "Navigational"]),
        height=36,
        fg_color=colors["bg_input"],
        border_color=colors["border"],
        button_color=colors["border"],
        dropdown_fg_color=colors["bg_card"],
        text_color=colors["text_primary"]
    )
    app.blog_intent_combo.set(blog_cfg.get("last_intent", "Informational"))
    app.blog_intent_combo.grid(row=1, column=3, sticky="ew", pady=(0, 12))

    # Row 2: Tone, Audience, Format, Word Count
    ctk.CTkLabel(app.grid1, text="Tone of Voice", font=ctk.CTkFont(size=11, weight="bold"), text_color=colors["text_primary"]).grid(row=2, column=0, sticky="w", pady=(0, 4))
    app.blog_tone_combo = ctk.CTkComboBox(
        app.grid1,
        values=blog_cfg.get("tones", ["Conversational & Engaging", "Professional & Authoritative", "Persuasive", "Informative"]),
        height=36,
        fg_color=colors["bg_input"],
        border_color=colors["border"],
        button_color=colors["border"],
        dropdown_fg_color=colors["bg_card"],
        text_color=colors["text_primary"]
    )
    app.blog_tone_combo.set(blog_cfg.get("last_tone", "Conversational & Engaging"))
    app.blog_tone_combo.grid(row=3, column=0, sticky="ew", padx=(0, 10), pady=(0, 12))

    ctk.CTkLabel(app.grid1, text="Target Audience", font=ctk.CTkFont(size=11, weight="bold"), text_color=colors["text_primary"]).grid(row=2, column=1, sticky="w", pady=(0, 4))
    app.blog_audience_combo = ctk.CTkComboBox(
        app.grid1,
        values=blog_cfg.get("audiences", ["General Audience", "Beginners", "Tech Enthusiasts", "Professionals"]),
        height=36,
        fg_color=colors["bg_input"],
        border_color=colors["border"],
        button_color=colors["border"],
        dropdown_fg_color=colors["bg_card"],
        text_color=colors["text_primary"]
    )
    app.blog_audience_combo.set(blog_cfg.get("last_audience", "General Audience"))
    app.blog_audience_combo.grid(row=3, column=1, sticky="ew", padx=(0, 10), pady=(0, 12))

    ctk.CTkLabel(app.grid1, text="Article Format", font=ctk.CTkFont(size=11, weight="bold"), text_color=colors["text_primary"]).grid(row=2, column=2, sticky="w", pady=(0, 4))
    app.blog_format_combo = ctk.CTkComboBox(
        app.grid1,
        values=blog_cfg.get("formats", ["Ultimate Guide", "Product Comparison", "Listicle", "How-to Guide"]),
        height=36,
        fg_color=colors["bg_input"],
        border_color=colors["border"],
        button_color=colors["border"],
        dropdown_fg_color=colors["bg_card"],
        text_color=colors["text_primary"]
    )
    app.blog_format_combo.set(blog_cfg.get("last_format", "Ultimate Guide"))
    app.blog_format_combo.grid(row=3, column=2, sticky="ew", padx=(0, 10), pady=(0, 12))

    ctk.CTkLabel(app.grid1, text="Target Word Count", font=ctk.CTkFont(size=11, weight="bold"), text_color=colors["text_primary"]).grid(row=2, column=3, sticky="w", pady=(0, 4))
    app.blog_wordcount_combo = ctk.CTkComboBox(
        app.grid1,
        values=["Short (~800 words)", "Standard (~1,500 words)", "Long-Form (~2,500 words)", "In-Depth (~3,500+ words)"],
        height=36,
        fg_color=colors["bg_input"],
        border_color=colors["border"],
        button_color=colors["border"],
        dropdown_fg_color=colors["bg_card"],
        text_color=colors["text_primary"]
    )
    app.blog_wordcount_combo.set("Standard (~1,500 words)")
    app.blog_wordcount_combo.grid(row=3, column=3, sticky="ew", pady=(0, 12))

    # Row 3: Live SERP Research Checkbox
    app.blog_serp_var = ctk.BooleanVar(value=True)
    app.blog_serp_check = ctk.CTkCheckBox(
        app.grid1,
        text="🔍 Live SERP Research & Competitor Outline Mining (SerpAPI / Google)",
        variable=app.blog_serp_var,
        font=ctk.CTkFont(size=12, weight="bold"),
        fg_color=colors["primary"],
        text_color=colors["text_primary"]
    )
    app.blog_serp_check.grid(row=4, column=0, columnspan=4, sticky="w", pady=(4, 0))

    # =========================================================================
    # CARD 2: SEO KEYWORDS & LINK BUILDING STRATEGY
    # =========================================================================
    app.card_seo = ctk.CTkFrame(
        parent_container,
        fg_color=colors["bg_card"],
        border_width=1,
        border_color=colors["border"],
        corner_radius=12
    )
    app.card_seo.pack(fill="x", padx=14, pady=8)

    ctk.CTkLabel(
        app.card_seo, 
        text="🔍 SEO Keywords & Link Building Strategy", 
        font=ctk.CTkFont(size=14, weight="bold"), 
        text_color=colors["text_primary"]
    ).pack(anchor="w", padx=18, pady=(16, 10))

    grid2 = ctk.CTkFrame(app.card_seo, fg_color="transparent")
    grid2.pack(fill="x", padx=18, pady=(0, 14))

    ctk.CTkLabel(grid2, text="Secondary / LSI Keywords (comma-separated):", font=ctk.CTkFont(size=11, weight="bold"), text_color=colors["text_primary"]).pack(anchor="w", pady=(0, 4))
    app.blog_sk_textbox = ctk.CTkTextbox(grid2, height=45, fg_color=colors["bg_input"], border_width=1, border_color=colors["border"], text_color=colors["text_primary"])
    app.blog_sk_textbox.pack(fill="x", pady=(0, 10))

    # XML Sitemap Row
    sitemap_row = ctk.CTkFrame(grid2, fg_color="transparent")
    sitemap_row.pack(fill="x", pady=(0, 6))

    ctk.CTkLabel(sitemap_row, text="XML Sitemap URL:", font=ctk.CTkFont(size=11, weight="bold"), text_color=colors["text_primary"]).pack(side="left", padx=(0, 10))
    app.blog_sitemap_entry = ctk.CTkEntry(sitemap_row, placeholder_text="e.g. https://myblog.com/sitemap.xml", height=32, width=340, fg_color=colors["bg_input"], border_color=colors["border"], text_color=colors["text_primary"])
    app.blog_sitemap_entry.pack(side="left", padx=(0, 10))

    btn_fetch_sitemap = ctk.CTkButton(
        sitemap_row,
        text="🔍 Auto-Fetch Internal Links",
        command=app._fetch_sitemap_links,
        height=32,
        font=ctk.CTkFont(size=11, weight="bold"),
        fg_color=colors["primary"],
        hover_color=colors["primary_hover"],
        text_color="#FFFFFF"
    )
    btn_fetch_sitemap.pack(side="left")

    ctk.CTkLabel(grid2, text="Internal Links / Sitemap URLs (one per line):", font=ctk.CTkFont(size=11, weight="bold"), text_color=colors["text_primary"]).pack(anchor="w", pady=(0, 4))
    app.blog_internal_links_textbox = ctk.CTkTextbox(grid2, height=45, fg_color=colors["bg_input"], border_width=1, border_color=colors["border"], text_color=colors["text_primary"])
    app.blog_internal_links_textbox.pack(fill="x", pady=(0, 10))

    app.blog_ext_links_var = ctk.BooleanVar(value=True)
    app.blog_ext_links_check = ctk.CTkCheckBox(grid2, text="🔗 Auto-Include Outbound Authority Reference Links", variable=app.blog_ext_links_var, font=ctk.CTkFont(size=12, weight="bold"), fg_color=colors["primary"], text_color=colors["text_primary"])
    app.blog_ext_links_check.pack(anchor="w", pady=8)

    ctk.CTkLabel(grid2, text="Competitor Reference URLs (one per line):", font=ctk.CTkFont(size=11, weight="bold"), text_color=colors["text_primary"]).pack(anchor="w", pady=(10, 4))
    app.blog_comp_urls_textbox = ctk.CTkTextbox(grid2, height=45, fg_color=colors["bg_input"], border_width=1, border_color=colors["border"], text_color=colors["text_primary"])
    app.blog_comp_urls_textbox.pack(fill="x", pady=(0, 10))

    # =========================================================================
    # CARD 3: CONTENT ENHANCEMENTS & MEDIA OPTIONS
    # =========================================================================
    app.card_enhancement = ctk.CTkFrame(
        parent_container,
        fg_color=colors["bg_card"],
        border_width=1,
        border_color=colors["border"],
        corner_radius=12
    )
    app.card_enhancement.pack(fill="x", padx=14, pady=8)

    ctk.CTkLabel(
        app.card_enhancement, 
        text="📸 Content Enhancements & Media Options", 
        font=ctk.CTkFont(size=14, weight="bold"), 
        text_color=colors["text_primary"]
    ).pack(anchor="w", padx=18, pady=(16, 10))

    grid3 = ctk.CTkFrame(app.card_enhancement, fg_color="transparent")
    grid3.pack(fill="x", padx=18, pady=(0, 14))

    app.blog_humanizer_var = ctk.BooleanVar(value=True)
    app.blog_humanizer_check = ctk.CTkCheckBox(
        grid3,
        text="🛡️ AI Content Humanizer (Strips AI Clichés & Naturalizes Tone)",
        variable=app.blog_humanizer_var,
        font=ctk.CTkFont(size=12, weight="bold"),
        fg_color=colors["primary"],
        text_color=colors["text_primary"]
    )
    app.blog_humanizer_check.pack(anchor="w", pady=6)

    app.blog_img_prompts_var = ctk.BooleanVar(value=True)
    app.blog_img_prompts_check = ctk.CTkCheckBox(grid3, text="📸 Generate AI Image Prompts & Alt Text", variable=app.blog_img_prompts_var, font=ctk.CTkFont(size=12, weight="bold"), fg_color=colors["primary"], text_color=colors["text_primary"])
    app.blog_img_prompts_check.pack(anchor="w", pady=6)

    app.blog_tldr_var = ctk.BooleanVar(value=True)
    app.blog_tldr_check = ctk.CTkCheckBox(grid3, text="💡 Include Key Takeaways / TL;DR Box", variable=app.blog_tldr_var, font=ctk.CTkFont(size=12, weight="bold"), fg_color=colors["primary"], text_color=colors["text_primary"])
    app.blog_tldr_check.pack(anchor="w", pady=6)

    app.blog_faq_var = ctk.BooleanVar(value=True)
    app.blog_faq_check = ctk.CTkCheckBox(grid3, text="❓ Include People Also Ask FAQ Section", variable=app.blog_faq_var, font=ctk.CTkFont(size=12, weight="bold"), fg_color=colors["primary"], text_color=colors["text_primary"])
    app.blog_faq_check.pack(anchor="w", pady=6)

    ctk.CTkLabel(grid3, text="Call To Action (CTA):", font=ctk.CTkFont(size=11, weight="bold"), text_color=colors["text_primary"]).pack(anchor="w", pady=(10, 4))
    app.blog_cta_entry = ctk.CTkEntry(grid3, placeholder_text="Optional closing CTA (e.g. Subscribe to our newsletter)...", height=36, fg_color=colors["bg_input"], border_color=colors["border"], text_color=colors["text_primary"])
    app.blog_cta_entry.pack(fill="x", pady=(0, 10))

    ctk.CTkLabel(grid3, text="Custom Outline / Heading Points (Optional):", font=ctk.CTkFont(size=11, weight="bold"), text_color=colors["text_primary"]).pack(anchor="w", pady=(6, 4))
    app.blog_outline_textbox = ctk.CTkTextbox(grid3, height=55, fg_color=colors["bg_input"], border_width=1, border_color=colors["border"], text_color=colors["text_primary"])
    app.blog_outline_textbox.pack(fill="x", pady=(0, 10))

    # =========================================================================
    # CARD 4: EXPORT FORMATS & GENERATION ACTION
    # =========================================================================
    app.card_export = ctk.CTkFrame(
        parent_container,
        fg_color=colors["bg_card"],
        border_width=1,
        border_color=colors["border"],
        corner_radius=12
    )
    app.card_export.pack(fill="x", padx=14, pady=8)

    ctk.CTkLabel(
        app.card_export, 
        text="📦 SEO Export Formats", 
        font=ctk.CTkFont(size=14, weight="bold"), 
        text_color=colors["text_primary"]
    ).pack(anchor="w", padx=18, pady=(16, 10))

    grid4 = ctk.CTkFrame(app.card_export, fg_color="transparent")
    grid4.pack(fill="x", padx=18, pady=(0, 14))

    app.blog_html_var = ctk.BooleanVar(value=True)
    app.blog_docx_var = ctk.BooleanVar(value=True)
    app.blog_md_var = ctk.BooleanVar(value=True)
    app.blog_json_var = ctk.BooleanVar(value=True)

    fmt_row = ctk.CTkFrame(grid4, fg_color="transparent")
    fmt_row.pack(fill="x", pady=(0, 12))

    app.blog_html_check = ctk.CTkCheckBox(fmt_row, text="WordPress HTML (.html)", variable=app.blog_html_var, font=ctk.CTkFont(size=12, weight="bold"), fg_color=colors["primary"], text_color=colors["text_primary"])
    app.blog_html_check.pack(side="left", padx=(0, 16))

    app.blog_docx_check = ctk.CTkCheckBox(fmt_row, text="Word (.docx)", variable=app.blog_docx_var, font=ctk.CTkFont(size=12, weight="bold"), fg_color=colors["primary"], text_color=colors["text_primary"])
    app.blog_docx_check.pack(side="left", padx=16)

    app.blog_md_check = ctk.CTkCheckBox(fmt_row, text="Markdown (.md)", variable=app.blog_md_var, font=ctk.CTkFont(size=12, weight="bold"), fg_color=colors["primary"], text_color=colors["text_primary"])
    app.blog_md_check.pack(side="left", padx=16)

    app.blog_json_check = ctk.CTkCheckBox(fmt_row, text="Headless CMS JSON (.json)", variable=app.blog_json_var, font=ctk.CTkFont(size=12, weight="bold"), fg_color=colors["primary"], text_color=colors["text_primary"])
    app.blog_json_check.pack(side="left", padx=16)

    # Main Action Button & Clear Button (High contrast text visibility!)
    action_btn_row = ctk.CTkFrame(app.card_export, fg_color="transparent")
    action_btn_row.pack(fill="x", padx=18, pady=(0, 16))

    app.btn_clear_all = ctk.CTkButton(
        action_btn_row,
        text="Clear All",
        font=ctk.CTkFont(size=12, weight="bold"),
        width=110,
        height=40,
        fg_color="transparent",
        border_width=1,
        border_color=colors["danger"],
        text_color=colors["danger"],
        hover_color=colors["bg_card_hover"]
    )
    app.btn_clear_all.pack(side="left")

    app.blog_start_btn = ctk.CTkButton(
        action_btn_row,
        text="🚀 Generate SEO Blog Article(s)",
        font=ctk.CTkFont(size=14, weight="bold"),
        command=app._start_blog_generation,
        height=40,
        fg_color=colors["primary"],
        hover_color=colors["primary_hover"],
        text_color="#FFFFFF"
    )
    app.blog_start_btn.pack(side="left", fill="x", expand=True, padx=(10, 0))

    # =========================================================================
    # CARD 5: ACTIVITY LOGS CONSOLE PANEL
    # =========================================================================
    if not hasattr(app, 'log_frame') or not app.log_frame:
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

    # =========================================================================
    # CARD 6: BOTTOM OUTPUT SHORTCUT BUTTONS
    # =========================================================================
    if not hasattr(app, 'bottom_frame') or not app.bottom_frame:
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
