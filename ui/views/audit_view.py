"""
Dedicated Technical SEO Audit & Toxic Disavow View (Screaming Frog & Disavow Generator).
Executes Screaming Frog CLI and REST API audits, audits toxic backlinks, and exports disavow.txt files.
"""

import customtkinter as ctk


def build_audit_view(app, parent_container):
    """Builds the dedicated Technical SEO Audit view."""
    colors = app.theme_mgr.colors

    # Card 1: Screaming Frog Site Audit
    card_audit = ctk.CTkFrame(
        parent_container,
        fg_color=colors["bg_card"],
        border_width=1,
        border_color=colors["border"],
        corner_radius=12
    )
    card_audit.pack(fill="x", padx=14, pady=(14, 8))

    ctk.CTkLabel(
        card_audit,
        text="🐸 Technical SEO Site Audit Suite (Screaming Frog Integration)",
        font=ctk.CTkFont(size=14, weight="bold"),
        text_color=colors["text_primary"]
    ).pack(anchor="w", padx=18, pady=(16, 4))

    ctk.CTkLabel(
        card_audit,
        text="Run automated technical SEO site audits via Screaming Frog CLI / local REST API (http://localhost:28018) to discover broken links (404s), missing meta tags, and H1/H2 issues.",
        font=ctk.CTkFont(size=11),
        text_color=colors["text_secondary"]
    ).pack(anchor="w", padx=18, pady=(0, 12))

    row_url = ctk.CTkFrame(card_audit, fg_color="transparent")
    row_url.pack(fill="x", padx=18, pady=(0, 14))

    ctk.CTkLabel(row_url, text="Target Website URL:", font=ctk.CTkFont(weight="bold"), text_color=colors["text_primary"]).pack(side="left", padx=(0, 10))
    app.tab_audit_url_entry = ctk.CTkEntry(row_url, placeholder_text="e.g. https://myblog.com", width=340, height=36, fg_color=colors["bg_input"], border_color=colors["border"], text_color=colors["text_primary"])
    app.tab_audit_url_entry.pack(side="left", padx=(0, 10))

    btn_run = ctk.CTkButton(
        row_url,
        text="🚀 Run Technical Audit Now",
        command=lambda: app._run_screaming_frog_audit(),
        height=36,
        font=ctk.CTkFont(size=12, weight="bold"),
        fg_color=colors["primary"],
        hover_color=colors["primary_hover"],
        text_color="#FFFFFF"
    )
    btn_run.pack(side="left")

    # Card 2: Toxic Backlink Audit & 1-Click Disavow Generator
    card_disavow = ctk.CTkFrame(
        parent_container,
        fg_color=colors["bg_card"],
        border_width=1,
        border_color=colors["border"],
        corner_radius=12
    )
    card_disavow.pack(fill="x", padx=14, pady=8)

    ctk.CTkLabel(
        card_disavow,
        text="🛡️ Toxic Backlink Audit & Google Search Console Disavow Exporter",
        font=ctk.CTkFont(size=14, weight="bold"),
        text_color=colors["text_primary"]
    ).pack(anchor="w", padx=18, pady=(16, 4))

    ctk.CTkLabel(
        card_disavow,
        text="Paste backlink URLs or referring domains below to scan for toxic spam TLDs and export a 1-click Google Search Console disavow.txt file.",
        font=ctk.CTkFont(size=11),
        text_color=colors["text_secondary"]
    ).pack(anchor="w", padx=18, pady=(0, 12))

    app.disavow_input_textbox = ctk.CTkTextbox(
        card_disavow,
        height=100,
        fg_color=colors["bg_input"],
        border_width=1,
        border_color=colors["border"],
        text_color=colors["text_primary"]
    )
    app.disavow_input_textbox.insert("1.0", "http://spammy-pbn-site.xyz\nhttp://casino-cheap-loans.top\nhttp://normal-blog.com")
    app.disavow_input_textbox.pack(fill="x", padx=18, pady=(0, 10))

    row_dis_acts = ctk.CTkFrame(card_disavow, fg_color="transparent")
    row_dis_acts.pack(fill="x", padx=18, pady=(0, 14))

    btn_audit_links = ctk.CTkButton(
        row_dis_acts,
        text="🔍 Scan Toxic Backlinks & Generate disavow.txt",
        command=app._run_toxic_backlink_audit,
        height=36,
        font=ctk.CTkFont(size=12, weight="bold"),
        fg_color=colors["primary"],
        hover_color=colors["primary_hover"],
        text_color="#FFFFFF"
    )
    btn_audit_links.pack(side="left")
