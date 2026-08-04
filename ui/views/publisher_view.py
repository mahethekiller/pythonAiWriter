"""
Dedicated CMS & WordPress Direct Publisher View.
Allows users to publish active generated articles, browse saved .html/.json files, or enter custom content to publish to WordPress.
"""

import customtkinter as ctk


def build_publisher_view(app, parent_container):
    """Builds the dedicated CMS Publisher view."""
    colors = app.theme_mgr.colors

    # Card 1: Connection & Credentials Status
    card_conn = ctk.CTkFrame(
        parent_container,
        fg_color=colors["bg_card"],
        border_width=1,
        border_color=colors["border"],
        corner_radius=12
    )
    card_conn.pack(fill="x", padx=14, pady=(14, 8))

    ctk.CTkLabel(
        card_conn,
        text="🌐 WordPress Connection & Credentials",
        font=ctk.CTkFont(size=14, weight="bold"),
        text_color=colors["text_primary"]
    ).pack(anchor="w", padx=18, pady=(16, 4))

    ctk.CTkLabel(
        card_conn,
        text="Configure your WordPress site URL and Application Password under Settings & API Keys to enable 1-click publishing.",
        font=ctk.CTkFont(size=11),
        text_color=colors["text_secondary"]
    ).pack(anchor="w", padx=18, pady=(0, 12))

    row_conn_acts = ctk.CTkFrame(card_conn, fg_color="transparent")
    row_conn_acts.pack(fill="x", padx=18, pady=(0, 14))

    btn_test_conn = ctk.CTkButton(
        row_conn_acts,
        text="🔌 Test WordPress Connection",
        command=app._test_wp_connection,
        height=36,
        font=ctk.CTkFont(size=12, weight="bold"),
        fg_color=colors["bg_card"],
        hover_color=colors["bg_card_hover"],
        border_width=1,
        border_color=colors["border"],
        text_color=colors["text_primary"]
    )
    btn_test_conn.pack(side="left", padx=(0, 10))

    ctk.CTkLabel(row_conn_acts, text="Post Status:", font=ctk.CTkFont(weight="bold"), text_color=colors["text_primary"]).pack(side="left", padx=(16, 8))
    app.wp_status_combo = ctk.CTkComboBox(
        row_conn_acts,
        values=["draft", "publish"],
        width=120,
        height=36,
        fg_color=colors["bg_input"],
        border_color=colors["border"],
        button_color=colors["border"],
        dropdown_fg_color=colors["bg_card"],
        text_color=colors["text_primary"]
    )
    app.wp_status_combo.set("draft")
    app.wp_status_combo.pack(side="left")

    # Card 2: Article Source Selection & Post Manager
    card_source = ctk.CTkFrame(
        parent_container,
        fg_color=colors["bg_card"],
        border_width=1,
        border_color=colors["border"],
        corner_radius=12
    )
    card_source.pack(fill="x", padx=14, pady=8)

    ctk.CTkLabel(
        card_source,
        text="📄 Select Article Content to Publish",
        font=ctk.CTkFont(size=14, weight="bold"),
        text_color=colors["text_primary"]
    ).pack(anchor="w", padx=18, pady=(16, 10))

    # Source Mode Radio Selector
    app.pub_source_mode_var = ctk.StringVar(value="active")

    row_modes = ctk.CTkFrame(card_source, fg_color="transparent")
    row_modes.pack(fill="x", padx=18, pady=(0, 12))

    app.radio_src_active = ctk.CTkRadioButton(
        row_modes,
        text="Current Active Generated Article",
        variable=app.pub_source_mode_var,
        value="active",
        command=app._toggle_pub_source_mode,
        font=ctk.CTkFont(size=12, weight="bold"),
        fg_color=colors["primary"],
        text_color=colors["text_primary"]
    )
    app.radio_src_active.pack(side="left", padx=(0, 16))

    app.radio_src_file = ctk.CTkRadioButton(
        row_modes,
        text="Browse Saved Article File (.html / .json)",
        variable=app.pub_source_mode_var,
        value="file",
        command=app._toggle_pub_source_mode,
        font=ctk.CTkFont(size=12, weight="bold"),
        fg_color=colors["primary"],
        text_color=colors["text_primary"]
    )
    app.radio_src_file.pack(side="left", padx=16)

    app.radio_src_custom = ctk.CTkRadioButton(
        row_modes,
        text="Custom Title & HTML Content",
        variable=app.pub_source_mode_var,
        value="custom",
        command=app._toggle_pub_source_mode,
        font=ctk.CTkFont(size=12, weight="bold"),
        fg_color=colors["primary"],
        text_color=colors["text_primary"]
    )
    app.radio_src_custom.pack(side="left", padx=16)

    # File Picker Row
    app.pub_file_frame = ctk.CTkFrame(card_source, fg_color="transparent")
    app.pub_file_frame.pack(fill="x", padx=18, pady=(0, 10))

    ctk.CTkLabel(app.pub_file_frame, text="Article File:", font=ctk.CTkFont(weight="bold"), text_color=colors["text_primary"]).pack(side="left", padx=(0, 10))
    app.pub_file_entry = ctk.CTkEntry(
        app.pub_file_frame,
        placeholder_text="Path to saved .html or .json file...",
        width=380,
        height=36,
        fg_color=colors["bg_input"],
        border_color=colors["border"],
        text_color=colors["text_primary"]
    )
    app.pub_file_entry.pack(side="left", padx=(0, 10))

    app.btn_browse_pub_file = ctk.CTkButton(
        app.pub_file_frame,
        text="📁 Browse File...",
        command=app._browse_pub_file,
        height=36,
        font=ctk.CTkFont(size=11, weight="bold"),
        fg_color=colors["bg_card"],
        hover_color=colors["bg_card_hover"],
        border_width=1,
        border_color=colors["border"],
        text_color=colors["text_primary"]
    )
    app.btn_browse_pub_file.pack(side="left")

    # Post Title Entry
    app.pub_title_frame = ctk.CTkFrame(card_source, fg_color="transparent")
    app.pub_title_frame.pack(fill="x", padx=18, pady=(0, 10))

    ctk.CTkLabel(app.pub_title_frame, text="WordPress Post Title:", font=ctk.CTkFont(weight="bold"), text_color=colors["text_primary"]).pack(anchor="w", pady=(0, 4))
    app.pub_title_entry = ctk.CTkEntry(
        app.pub_title_frame,
        placeholder_text="Enter post title...",
        height=36,
        fg_color=colors["bg_input"],
        border_color=colors["border"],
        text_color=colors["text_primary"]
    )
    app.pub_title_entry.pack(fill="x")

    # Content Textbox
    app.pub_content_frame = ctk.CTkFrame(card_source, fg_color="transparent")
    app.pub_content_frame.pack(fill="x", padx=18, pady=(0, 14))

    ctk.CTkLabel(app.pub_content_frame, text="Article HTML Body Content:", font=ctk.CTkFont(weight="bold"), text_color=colors["text_primary"]).pack(anchor="w", pady=(0, 4))
    app.pub_content_textbox = ctk.CTkTextbox(
        app.pub_content_frame,
        height=140,
        fg_color=colors["bg_input"],
        border_width=1,
        border_color=colors["border"],
        text_color=colors["text_primary"]
    )
    app.pub_content_textbox.insert("1.0", "<p>Content of the selected article will appear here...</p>")
    app.pub_content_textbox.pack(fill="x")

    # Main Action Button
    row_act_btn = ctk.CTkFrame(card_source, fg_color="transparent")
    row_act_btn.pack(fill="x", padx=18, pady=(0, 16))

    btn_pub_now = ctk.CTkButton(
        row_act_btn,
        text="🌐 Publish Article to WordPress Now",
        command=app._publish_to_wordpress,
        height=42,
        font=ctk.CTkFont(size=13, weight="bold"),
        fg_color=colors["primary"],
        hover_color=colors["primary_hover"],
        text_color="#FFFFFF"
    )
    btn_pub_now.pack(fill="x")
