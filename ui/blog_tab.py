"""
Tab 2: SEO Blog Creator UI view construction with Cyber-Dark glassmorphism styling.
"""

import customtkinter as ctk

def build_blog_tab(app, parent_container):
    """Builds all UI frames for the SEO Blog Creator tab."""
    blog_cfg = app.config_mgr.data.get("blog_config", {})

    # Active Config Status Banner for Blog Creator
    app.blog_status_info_frame = ctk.CTkFrame(
        parent_container, 
        fg_color="#161e2e", 
        border_width=1, 
        border_color="#2a364f", 
        corner_radius=10
    )
    app.blog_status_info_frame.pack(fill="x", padx=10, pady=(6, 4))

    app.blog_config_status_label = ctk.CTkLabel(
        app.blog_status_info_frame, 
        text="Active AI Provider: Loading...", 
        font=ctk.CTkFont(size=12, weight="bold"),
        text_color="#38bdf8"
    )
    app.blog_config_status_label.pack(side="left", padx=14, pady=8)

    app.blog_cost_badge = ctk.CTkLabel(
        app.blog_status_info_frame,
        text="Estimated Cost: ~$0.003 USD",
        font=ctk.CTkFont(size=11, weight="bold"),
        text_color="#4ade80"
    )
    app.blog_cost_badge.pack(side="right", padx=14, pady=8)

    # Quick Strategy Preset Bar Frame
    app.preset_frame = ctk.CTkFrame(
        parent_container, 
        fg_color="#161e2e", 
        border_width=1, 
        border_color="#2a364f", 
        corner_radius=10
    )
    app.preset_frame.pack(fill="x", padx=10, pady=(6, 4))

    ctk.CTkLabel(app.preset_frame, text="🎯 Quick Strategy Preset:", font=ctk.CTkFont(weight="bold", size=13), text_color="#38bdf8").pack(side="left", padx=12, pady=8)

    app.preset_combo = ctk.CTkComboBox(
        app.preset_frame,
        values=[
            "Custom Customization...",
            "🛍️ Affiliate Product Review (Commercial Intent, Persuasive)",
            "🎓 Educational Deep-Dive (Informational Intent, Authoritative)",
            "⚡ Quick News Summary (Informational Intent, Short ~800 words)"
        ],
        command=app._apply_blog_preset,
        width=420
    )
    app.preset_combo.set("Custom Customization...")
    app.preset_combo.pack(side="left", padx=10, pady=8)

    # Panel 1: Generation Mode & Core Topic Strategy Frame
    app.blog_strategy_frame = ctk.CTkFrame(
        parent_container, 
        fg_color="#161e2e", 
        border_width=1, 
        border_color="#2a364f", 
        corner_radius=10
    )
    app.blog_strategy_frame.pack(fill="x", padx=10, pady=5)

    ctk.CTkLabel(app.blog_strategy_frame, text="Execution Mode:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=8, pady=6, sticky="w")
    app.blog_mode_var = ctk.StringVar(value="single")
    
    app.blog_single_radio = ctk.CTkRadioButton(
        app.blog_strategy_frame, 
        text="Single Article Mode", 
        variable=app.blog_mode_var, 
        value="single",
        command=app._toggle_blog_mode
    )
    app.blog_single_radio.grid(row=0, column=1, padx=8, pady=6, sticky="w")

    app.blog_batch_radio = ctk.CTkRadioButton(
        app.blog_strategy_frame, 
        text="Batch CSV Cluster Mode", 
        variable=app.blog_mode_var, 
        value="batch",
        command=app._toggle_blog_mode
    )
    app.blog_batch_radio.grid(row=0, column=2, padx=8, pady=6, sticky="w")

    # Single Topic Entry Line
    app.blog_topic_label = ctk.CTkLabel(app.blog_strategy_frame, text="Article Topic / Title:", font=ctk.CTkFont(weight="bold"))
    app.blog_topic_label.grid(row=1, column=0, padx=8, pady=6, sticky="w")
    
    app.blog_topic_entry = ctk.CTkEntry(app.blog_strategy_frame, placeholder_text="e.g. 10 Best Budget Laptops for College Students in 2026", width=420)
    app.blog_topic_entry.grid(row=1, column=1, columnspan=3, padx=8, pady=6, sticky="w")

    # Batch CSV Entry Line (Initially Hidden/Managed)
    app.blog_csv_label = ctk.CTkLabel(app.blog_strategy_frame, text="Batch Topics CSV File:", font=ctk.CTkFont(weight="bold"))
    app.blog_csv_entry = ctk.CTkEntry(app.blog_strategy_frame, placeholder_text="Path to .csv / .txt file...", width=260)
    app.blog_csv_browse_btn = ctk.CTkButton(app.blog_strategy_frame, text="📁 Browse CSV...", command=app._browse_blog_csv, width=100)
    app.blog_csv_sample_btn = ctk.CTkButton(app.blog_strategy_frame, text="📥 Sample CSV", command=app._download_sample_csv, width=105, fg_color="#2563eb", hover_color="#1d4ed8")

    # Tone, Format, Audience, Word Count Grid
    ctk.CTkLabel(app.blog_strategy_frame, text="Tone of Voice:", font=ctk.CTkFont(weight="bold")).grid(row=2, column=0, padx=8, pady=6, sticky="w")
    app.blog_tone_combo = ctk.CTkComboBox(app.blog_strategy_frame, values=blog_cfg.get("tones", []), width=210)
    app.blog_tone_combo.set(blog_cfg.get("last_tone", "Conversational & Engaging"))
    app.blog_tone_combo.grid(row=2, column=1, padx=8, pady=6, sticky="w")

    ctk.CTkLabel(app.blog_strategy_frame, text="Article Format:", font=ctk.CTkFont(weight="bold")).grid(row=2, column=2, padx=8, pady=6, sticky="w")
    app.blog_format_combo = ctk.CTkComboBox(app.blog_strategy_frame, values=blog_cfg.get("formats", []), width=210)
    app.blog_format_combo.set(blog_cfg.get("last_format", "Ultimate Guide"))
    app.blog_format_combo.grid(row=2, column=3, padx=8, pady=6, sticky="w")

    ctk.CTkLabel(app.blog_strategy_frame, text="Target Audience:", font=ctk.CTkFont(weight="bold")).grid(row=3, column=0, padx=8, pady=6, sticky="w")
    app.blog_audience_combo = ctk.CTkComboBox(app.blog_strategy_frame, values=blog_cfg.get("audiences", []), width=210)
    app.blog_audience_combo.set(blog_cfg.get("last_audience", "General Audience"))
    app.blog_audience_combo.grid(row=3, column=1, padx=8, pady=6, sticky="w")

    ctk.CTkLabel(app.blog_strategy_frame, text="Target Word Count:", font=ctk.CTkFont(weight="bold")).grid(row=3, column=2, padx=8, pady=6, sticky="w")
    app.blog_wordcount_combo = ctk.CTkComboBox(
        app.blog_strategy_frame, 
        values=["Short (~800 words)", "Standard (~1,500 words)", "Long-form (~2,500+ words)"], 
        width=210
    )
    app.blog_wordcount_combo.set(blog_cfg.get("last_word_count", "Standard (~1,500 words)"))
    app.blog_wordcount_combo.grid(row=3, column=3, padx=8, pady=6, sticky="w")

    # Panel 2: SEO & Linking Strategy Frame
    app.blog_seo_frame = ctk.CTkFrame(
        parent_container, 
        fg_color="#161e2e", 
        border_width=1, 
        border_color="#2a364f", 
        corner_radius=10
    )
    app.blog_seo_frame.pack(fill="x", padx=10, pady=5)

    ctk.CTkLabel(app.blog_seo_frame, text="Primary Focus Keyword:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=8, pady=6, sticky="w")
    app.blog_pk_entry = ctk.CTkEntry(app.blog_seo_frame, placeholder_text="e.g. budget student laptops", width=220)
    app.blog_pk_entry.grid(row=0, column=1, padx=8, pady=6, sticky="w")

    ctk.CTkLabel(app.blog_seo_frame, text="Search Intent:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, padx=8, pady=6, sticky="w")
    app.blog_intent_combo = ctk.CTkComboBox(app.blog_seo_frame, values=blog_cfg.get("intents", []), width=200)
    app.blog_intent_combo.set(blog_cfg.get("last_intent", "Informational"))
    app.blog_intent_combo.grid(row=0, column=3, padx=8, pady=6, sticky="w")

    ctk.CTkLabel(app.blog_seo_frame, text="Secondary / LSI Keywords (comma-separated):", font=ctk.CTkFont(weight="bold")).grid(row=1, column=0, columnspan=2, padx=8, pady=(6, 2), sticky="w")
    app.blog_sk_textbox = ctk.CTkTextbox(app.blog_seo_frame, height=45)
    app.blog_sk_textbox.grid(row=2, column=0, columnspan=4, padx=8, pady=(0, 6), sticky="ew")

    ctk.CTkLabel(app.blog_seo_frame, text="Internal Links / Sitemap URLs (one per line):", font=ctk.CTkFont(weight="bold")).grid(row=3, column=0, columnspan=2, padx=8, pady=(6, 2), sticky="w")
    app.blog_internal_links_textbox = ctk.CTkTextbox(app.blog_seo_frame, height=45)
    app.blog_internal_links_textbox.grid(row=4, column=0, columnspan=4, padx=8, pady=(0, 6), sticky="ew")

    app.blog_ext_links_var = ctk.BooleanVar(value=True)
    app.blog_ext_links_check = ctk.CTkCheckBox(app.blog_seo_frame, text="🔗 Auto-Include Outbound Authority Links", variable=app.blog_ext_links_var)
    app.blog_ext_links_check.grid(row=5, column=0, columnspan=2, padx=8, pady=6, sticky="w")

    ctk.CTkLabel(app.blog_seo_frame, text="Competitor Reference URLs (one per line):", font=ctk.CTkFont(weight="bold")).grid(row=6, column=0, columnspan=2, padx=8, pady=(6, 2), sticky="w")
    app.blog_comp_urls_textbox = ctk.CTkTextbox(app.blog_seo_frame, height=45)
    app.blog_comp_urls_textbox.grid(row=7, column=0, columnspan=4, padx=8, pady=(0, 6), sticky="ew")

    # Panel 3: Enhancements & Media Options Frame
    app.blog_enhancements_frame = ctk.CTkFrame(
        parent_container, 
        fg_color="#161e2e", 
        border_width=1, 
        border_color="#2a364f", 
        corner_radius=10
    )
    app.blog_enhancements_frame.pack(fill="x", padx=10, pady=5)

    app.blog_img_prompts_var = ctk.BooleanVar(value=True)
    app.blog_img_prompts_check = ctk.CTkCheckBox(app.blog_enhancements_frame, text="📸 Generate AI Image Prompts & Alt Text", variable=app.blog_img_prompts_var)
    app.blog_img_prompts_check.grid(row=0, column=0, padx=12, pady=8, sticky="w")

    app.blog_tldr_var = ctk.BooleanVar(value=True)
    app.blog_tldr_check = ctk.CTkCheckBox(app.blog_enhancements_frame, text="💡 Include Key Takeaways / TL;DR Box", variable=app.blog_tldr_var)
    app.blog_tldr_check.grid(row=0, column=1, padx=12, pady=8, sticky="w")

    app.blog_faq_var = ctk.BooleanVar(value=True)
    app.blog_faq_check = ctk.CTkCheckBox(app.blog_enhancements_frame, text="❓ Include People Also Ask FAQ Section", variable=app.blog_faq_var)
    app.blog_faq_check.grid(row=0, column=2, padx=12, pady=8, sticky="w")

    ctk.CTkLabel(app.blog_enhancements_frame, text="Call To Action (CTA):", font=ctk.CTkFont(weight="bold")).grid(row=1, column=0, padx=8, pady=6, sticky="w")
    app.blog_cta_entry = ctk.CTkEntry(app.blog_enhancements_frame, placeholder_text="Optional closing CTA (e.g. Subscribe to our newsletter)...", width=450)
    app.blog_cta_entry.grid(row=1, column=1, columnspan=2, padx=8, pady=6, sticky="w")

    ctk.CTkLabel(app.blog_enhancements_frame, text="Custom Outline / Heading Points (Optional):", font=ctk.CTkFont(weight="bold")).grid(row=2, column=0, columnspan=2, padx=8, pady=(6, 2), sticky="w")
    app.blog_outline_textbox = ctk.CTkTextbox(app.blog_enhancements_frame, height=55)
    app.blog_outline_textbox.grid(row=3, column=0, columnspan=3, padx=8, pady=(0, 6), sticky="ew")

    # Panel 4: Export Formats Frame
    app.blog_formats_frame = ctk.CTkFrame(
        parent_container, 
        fg_color="#161e2e", 
        border_width=1, 
        border_color="#2a364f", 
        corner_radius=10
    )
    app.blog_formats_frame.pack(fill="x", padx=10, pady=5)

    ctk.CTkLabel(app.blog_formats_frame, text="SEO Export Formats:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=10, pady=8)
    
    app.blog_html_var = ctk.BooleanVar(value=True)
    app.blog_docx_var = ctk.BooleanVar(value=True)
    app.blog_md_var = ctk.BooleanVar(value=True)
    app.blog_json_var = ctk.BooleanVar(value=True)

    ctk.CTkCheckBox(app.blog_formats_frame, text="WordPress HTML (.html)", variable=app.blog_html_var).pack(side="left", padx=10, pady=8)
    ctk.CTkCheckBox(app.blog_formats_frame, text="Word (.docx)", variable=app.blog_docx_var).pack(side="left", padx=10, pady=8)
    ctk.CTkCheckBox(app.blog_formats_frame, text="Markdown (.md)", variable=app.blog_md_var).pack(side="left", padx=10, pady=8)
    ctk.CTkCheckBox(app.blog_formats_frame, text="Headless CMS JSON (.json)", variable=app.blog_json_var).pack(side="left", padx=10, pady=8)

    # Panel 5: Action & Progress Frame
    app.blog_action_frame = ctk.CTkFrame(
        parent_container, 
        fg_color="#161e2e", 
        border_width=1, 
        border_color="#2a364f", 
        corner_radius=10
    )
    app.blog_action_frame.pack(fill="x", padx=10, pady=5)

    app.blog_start_btn = ctk.CTkButton(
        app.blog_action_frame, 
        text="🚀 Generate SEO Blog Article(s)", 
        font=ctk.CTkFont(size=14, weight="bold"),
        command=app._start_blog_generation,
        height=38,
        fg_color="#10b981",
        hover_color="#059669"
    )
    app.blog_start_btn.pack(fill="x", padx=10, pady=8)

    # 3-Step Process Tracker
    app.blog_step_tracker_frame = ctk.CTkFrame(parent_container, fg_color="transparent")
    app.blog_step_tracker_frame.pack(fill="x", padx=10, pady=2)

    app.blog_step_tracker_label = ctk.CTkLabel(
        app.blog_step_tracker_frame,
        text="[ 1. Meta & Outline ] ➔ [ 2. AI Article Writer ] ➔ [ 3. Multi-Format Exports ]",
        font=ctk.CTkFont(size=11, weight="bold"),
        text_color="#94a3b8"
    )
    app.blog_step_tracker_label.pack(anchor="center")

    app.blog_progress_frame = ctk.CTkFrame(parent_container, fg_color="transparent")
    app.blog_progress_frame.pack(fill="x", padx=10, pady=2)

    app.blog_progress_bar = ctk.CTkProgressBar(app.blog_progress_frame, progress_color="#10b981")
    app.blog_progress_bar.set(0)
    app.blog_progress_bar.pack(fill="x", side="top", pady=2)

    app.blog_status_lbl = ctk.CTkLabel(app.blog_progress_frame, text="Ready", font=ctk.CTkFont(size=12))
    app.blog_status_lbl.pack(side="left")

    # Panel 6: Hero Metric Stat Cards (Analytics Dashboard)
    app.hero_stats_container = ctk.CTkFrame(parent_container, fg_color="transparent")
    app.hero_stats_container.pack(fill="x", padx=10, pady=6)

    # Stat Card 1: Words
    app.stat_card_words = ctk.CTkFrame(app.hero_stats_container, fg_color="#161e2e", border_width=1, border_color="#2a364f", corner_radius=10, width=220)
    app.stat_card_words.pack(side="left", fill="both", expand=True, padx=4)
    ctk.CTkLabel(app.stat_card_words, text="TOTAL WORDS", font=ctk.CTkFont(size=10, weight="bold"), text_color="#94a3b8").pack(anchor="w", padx=12, pady=(8, 0))
    app.stat_val_words = ctk.CTkLabel(app.stat_card_words, text="--", font=ctk.CTkFont(size=20, weight="bold"), text_color="#38bdf8")
    app.stat_val_words.pack(anchor="w", padx=12, pady=(0, 8))

    # Stat Card 2: Keyword Density
    app.stat_card_density = ctk.CTkFrame(app.hero_stats_container, fg_color="#161e2e", border_width=1, border_color="#2a364f", corner_radius=10, width=220)
    app.stat_card_density.pack(side="left", fill="both", expand=True, padx=4)
    ctk.CTkLabel(app.stat_card_density, text="KEYWORD DENSITY", font=ctk.CTkFont(size=10, weight="bold"), text_color="#94a3b8").pack(anchor="w", padx=12, pady=(8, 0))
    app.stat_val_density = ctk.CTkLabel(app.stat_card_density, text="-- %", font=ctk.CTkFont(size=20, weight="bold"), text_color="#4ade80")
    app.stat_val_density.pack(anchor="w", padx=12, pady=(0, 8))

    # Stat Card 3: Readability
    app.stat_card_readability = ctk.CTkFrame(app.hero_stats_container, fg_color="#161e2e", border_width=1, border_color="#2a364f", corner_radius=10, width=220)
    app.stat_card_readability.pack(side="left", fill="both", expand=True, padx=4)
    ctk.CTkLabel(app.stat_card_readability, text="READABILITY SCORE", font=ctk.CTkFont(size=10, weight="bold"), text_color="#94a3b8").pack(anchor="w", padx=12, pady=(8, 0))
    app.stat_val_readability = ctk.CTkLabel(app.stat_card_readability, text="--", font=ctk.CTkFont(size=20, weight="bold"), text_color="#facc15")
    app.stat_val_readability.pack(anchor="w", padx=12, pady=(0, 8))

    # Panel 7: Detailed Meta Badges Card
    app.blog_seo_card_frame = ctk.CTkFrame(parent_container, fg_color="#161e2e", border_width=1, border_color="#2a364f", corner_radius=10)
    app.blog_seo_card_frame.pack(fill="x", padx=10, pady=6)

    ctk.CTkLabel(app.blog_seo_card_frame, text="📊 Meta Tag & Outline Audit Badges:", font=ctk.CTkFont(weight="bold", size=13), text_color="#38bdf8").pack(anchor="w", padx=12, pady=(6, 2))
    
    app.blog_seo_metrics_lbl = ctk.CTkLabel(
        app.blog_seo_card_frame, 
        text="Run generation to view Meta Title & Description pass/fail badges.", 
        font=ctk.CTkFont(size=11),
        text_color="#94a3b8"
    )
    app.blog_seo_metrics_lbl.pack(anchor="w", padx=12, pady=(0, 6))

    # Panel 8: Log Console & Bottom Shortcuts
    app.blog_log_frame = ctk.CTkFrame(parent_container, fg_color="#161e2e", border_width=1, border_color="#2a364f", corner_radius=10)
    app.blog_log_frame.pack(fill="x", padx=10, pady=5)

    ctk.CTkLabel(app.blog_log_frame, text="Blog Generation Activity Logs:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(4, 2))
    app.blog_log_textbox = ctk.CTkTextbox(app.blog_log_frame, height=95, font=ctk.CTkFont(family="Consolas", size=11))
    app.blog_log_textbox.pack(fill="x", padx=10, pady=(0, 6))

    app.blog_bottom_frame = ctk.CTkFrame(parent_container, fg_color="transparent")
    app.blog_bottom_frame.pack(fill="x", padx=10, pady=(5, 10))

    app.blog_open_folder_btn = ctk.CTkButton(
        app.blog_bottom_frame, 
        text="📁 Open Blog Output Folder", 
        command=app._open_blog_folder, 
        state="disabled",
        width=180
    )
    app.blog_open_folder_btn.pack(side="left", padx=(0, 8))

    app.blog_open_report_btn = ctk.CTkButton(
        app.blog_bottom_frame, 
        text="📊 Open Blog Excel Report", 
        command=app._open_blog_report, 
        state="disabled",
        width=180
    )
    app.blog_open_report_btn.pack(side="left")
