"""
Tab 1: Rewriter Dashboard UI view construction with Cyber-Dark glassmorphism styling.
"""

import customtkinter as ctk

def build_dashboard_tab(app, parent_container):
    """Builds all UI frames for the Rewriter Dashboard tab."""
    
    # Active Config Status Banner
    app.status_info_frame = ctk.CTkFrame(
        parent_container, 
        fg_color="#161e2e", 
        border_width=1, 
        border_color="#2a364f", 
        corner_radius=10
    )
    app.status_info_frame.pack(fill="x", padx=10, pady=(6, 4))

    app.config_status_label = ctk.CTkLabel(
        app.status_info_frame, 
        text="Active Config: Loading...", 
        font=ctk.CTkFont(size=12, weight="bold"),
        text_color="#38bdf8"
    )
    app.config_status_label.pack(side="left", padx=14, pady=8)

    # Cost Estimate Badge
    app.dash_cost_badge = ctk.CTkLabel(
        app.status_info_frame,
        text="Estimated Cost: ~$0.001 USD",
        font=ctk.CTkFont(size=11, weight="bold"),
        text_color="#4ade80"
    )
    app.dash_cost_badge.pack(side="right", padx=14, pady=8)

    # Input URLs Section Panel
    app.input_frame = ctk.CTkFrame(
        parent_container, 
        fg_color="#161e2e", 
        border_width=1, 
        border_color="#2a364f", 
        corner_radius=10
    )
    app.input_frame.pack(fill="x", padx=10, pady=5)

    header_subframe = ctk.CTkFrame(app.input_frame, fg_color="transparent")
    header_subframe.pack(fill="x", padx=10, pady=(6, 2))

    ctk.CTkLabel(
        header_subframe, 
        text="🌐 Target Webpage URLs (one per line):", 
        font=ctk.CTkFont(weight="bold", size=13)
    ).pack(side="left")

    info_urls_btn = ctk.CTkButton(
        header_subframe, 
        text="ℹ️", 
        width=28, 
        height=24, 
        fg_color="#334155", 
        hover_color="#475569",
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

    app.urls_textbox = ctk.CTkTextbox(app.input_frame, height=110, font=ctk.CTkFont(family="Consolas", size=11))
    app.urls_textbox.pack(fill="x", padx=10, pady=(0, 8))

    # Custom Instructions Section Panel
    app.instruction_frame = ctk.CTkFrame(
        parent_container, 
        fg_color="#161e2e", 
        border_width=1, 
        border_color="#2a364f", 
        corner_radius=10
    )
    app.instruction_frame.pack(fill="x", padx=10, pady=5)

    app.custom_prompt_var = ctk.BooleanVar(value=False)
    app.custom_prompt_checkbox = ctk.CTkCheckBox(
        app.instruction_frame, 
        text="💡 Add Custom Prompt Instructions", 
        variable=app.custom_prompt_var,
        command=app._toggle_custom_prompt,
        font=ctk.CTkFont(weight="bold")
    )
    app.custom_prompt_checkbox.pack(anchor="w", padx=10, pady=6)

    app.custom_prompt_textbox = ctk.CTkTextbox(app.instruction_frame, height=60)
    app.custom_prompt_textbox.insert("1.0", "Focus on technical clarity, punchy headers, and concise sentences.")
    app.custom_prompt_textbox.configure(state="disabled")
    app.custom_prompt_textbox.pack(fill="x", padx=10, pady=(0, 8))

    # Action & Export Formats Frame Panel
    app.action_frame = ctk.CTkFrame(
        parent_container, 
        fg_color="#161e2e", 
        border_width=1, 
        border_color="#2a364f", 
        corner_radius=10
    )
    app.action_frame.pack(fill="x", padx=10, pady=5)

    # Formats Selection
    app.formats_subframe = ctk.CTkFrame(app.action_frame, fg_color="transparent")
    app.formats_subframe.pack(fill="x", padx=10, pady=(6, 2))

    ctk.CTkLabel(app.formats_subframe, text="SEO Export Formats:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=(0, 10))

    app.html_var = ctk.BooleanVar(value=True)
    app.docx_var = ctk.BooleanVar(value=True)

    app.html_checkbox = ctk.CTkCheckBox(app.formats_subframe, text="WordPress HTML (.html)", variable=app.html_var)
    app.html_checkbox.pack(side="left", padx=10)

    app.docx_checkbox = ctk.CTkCheckBox(app.formats_subframe, text="Word (.docx)", variable=app.docx_var)
    app.docx_checkbox.pack(side="left", padx=10)

    # Action Button
    app.start_btn = ctk.CTkButton(
        app.action_frame, 
        text="🚀 Start Batch Rewriting", 
        font=ctk.CTkFont(size=14, weight="bold"),
        command=app._start_processing,
        height=38,
        fg_color="#10b981",
        hover_color="#059669"
    )
    app.start_btn.pack(fill="x", padx=10, pady=8)

    # 3-Step Visual Process Tracker Frame
    app.step_tracker_frame = ctk.CTkFrame(parent_container, fg_color="transparent")
    app.step_tracker_frame.pack(fill="x", padx=10, pady=4)

    app.step_tracker_label = ctk.CTkLabel(
        app.step_tracker_frame,
        text="[ 1. Web Scraping ] ➔ [ 2. AI Rewriting ] ➔ [ 3. Document Exports ]",
        font=ctk.CTkFont(size=11, weight="bold"),
        text_color="#94a3b8"
    )
    app.step_tracker_label.pack(anchor="center")

    # Progress Bar & Status Label
    app.progress_frame = ctk.CTkFrame(parent_container, fg_color="transparent")
    app.progress_frame.pack(fill="x", padx=10, pady=2)

    app.progress_bar = ctk.CTkProgressBar(app.progress_frame, progress_color="#10b981")
    app.progress_bar.set(0)
    app.progress_bar.pack(fill="x", side="top", pady=2)

    app.status_lbl = ctk.CTkLabel(app.progress_frame, text="Ready", font=ctk.CTkFont(size=12))
    app.status_lbl.pack(side="left")

    # Logging Console Panel
    app.log_frame = ctk.CTkFrame(
        parent_container, 
        fg_color="#161e2e", 
        border_width=1, 
        border_color="#2a364f", 
        corner_radius=10
    )
    app.log_frame.pack(fill="x", padx=10, pady=5)

    ctk.CTkLabel(app.log_frame, text="Activity Logs:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(4, 2))
    app.log_textbox = ctk.CTkTextbox(app.log_frame, height=95, font=ctk.CTkFont(family="Consolas", size=11))
    app.log_textbox.pack(fill="x", padx=10, pady=(0, 6))

    # Bottom Shortcut Buttons
    app.bottom_frame = ctk.CTkFrame(parent_container, fg_color="transparent")
    app.bottom_frame.pack(fill="x", padx=10, pady=(5, 10))

    app.open_folder_btn = ctk.CTkButton(
        app.bottom_frame, 
        text="📁 Open Dated Folder", 
        command=app._open_output_folder, 
        state="disabled",
        width=150
    )
    app.open_folder_btn.pack(side="left", padx=(0, 8))

    app.open_excel_btn = ctk.CTkButton(
        app.bottom_frame, 
        text="📊 Open Excel Report", 
        command=app._open_excel_file, 
        state="disabled",
        width=150
    )
    app.open_excel_btn.pack(side="left", padx=(0, 8))

    app.open_cost_btn = ctk.CTkButton(
        app.bottom_frame, 
        text="📄 Open Cost Report", 
        command=app._open_cost_file, 
        state="disabled",
        width=150
    )
    app.open_cost_btn.pack(side="left")
