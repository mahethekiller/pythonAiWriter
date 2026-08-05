"""
Configuration & Settings View construction with AI Provider Presets, WordPress REST API Credentials, and SERP/Screaming Frog Integrations.
"""

import os
import customtkinter as ctk
from core.config import PROVIDER_MODELS, get_model_info


def build_settings_view(app, parent_container):
    """Builds all UI cards and controls for the Configuration & Settings view."""
    colors = app.theme_mgr.colors
    
    # =========================================================================
    # CARD 1: AI PROVIDER & API CREDENTIALS
    # =========================================================================
    app.settings_frame = ctk.CTkFrame(
        parent_container, 
        fg_color=colors["bg_card"], 
        border_width=1, 
        border_color=colors["border"], 
        corner_radius=12
    )
    app.settings_frame.pack(fill="x", padx=14, pady=10)

    # Provider Selection Row
    ctk.CTkLabel(app.settings_frame, text="AI Provider:", font=ctk.CTkFont(weight="bold"), text_color=colors["text_primary"]).grid(row=0, column=0, padx=16, pady=12, sticky="w")
    app.provider_combo = ctk.CTkComboBox(
        app.settings_frame, 
        values=list(PROVIDER_MODELS.keys()),
        command=app._on_provider_change,
        width=240,
        fg_color=colors["bg_input"],
        border_color=colors["border"],
        button_color=colors["border"],
        dropdown_fg_color=colors["bg_card"],
        text_color=colors["text_primary"]
    )
    app.provider_combo.grid(row=0, column=1, padx=10, pady=12, sticky="w")

    info_provider_btn = ctk.CTkButton(
        app.settings_frame, 
        text="ℹ️", 
        width=32, 
        height=28, 
        fg_color=colors["bg_card_hover"], 
        hover_color=colors["border"],
        text_color=colors["text_primary"],
        command=lambda: app.show_info_popup(
            "AI API Providers",
            "Select your AI Service Provider.\n\n"
            "• OpenAI: gpt-4o, gpt-4o-mini, o1\n"
            "• Google Gemini: gemini-2.0-flash, gemini-1.5-pro\n"
            "• Anthropic Claude: claude-3-5-haiku, claude-3-5-sonnet\n"
            "• DeepSeek: deepseek-chat, deepseek-reasoner\n"
            "• Groq: ultra-fast open source models\n"
            "• Ollama: local offline LLMs running on localhost:11434"
        )
    )
    info_provider_btn.grid(row=0, column=2, padx=5, pady=12, sticky="w")

    # API Key Entry Row
    app.api_key_label = ctk.CTkLabel(app.settings_frame, text="API Key:", font=ctk.CTkFont(weight="bold"), text_color=colors["text_primary"])
    app.api_key_label.grid(row=1, column=0, padx=16, pady=10, sticky="w")

    app.api_key_entry = ctk.CTkEntry(app.settings_frame, show="•", width=340, fg_color=colors["bg_input"], border_color=colors["border"], text_color=colors["text_primary"])
    app.api_key_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    app.save_key_btn = ctk.CTkButton(
        app.settings_frame, 
        text="💾 Save Key", 
        command=app._save_api_key, 
        width=100, 
        height=32,
        font=ctk.CTkFont(weight="bold"),
        fg_color=colors["success"], 
        hover_color=colors["primary_hover"],
        text_color="#FFFFFF"
    )
    app.save_key_btn.grid(row=1, column=2, padx=5, pady=10, sticky="w")

    # Custom Base URL Row
    app.base_url_label = ctk.CTkLabel(app.settings_frame, text="Base URL (Optional):", font=ctk.CTkFont(weight="bold"), text_color=colors["text_primary"])
    app.base_url_label.grid(row=2, column=0, padx=16, pady=10, sticky="w")

    app.base_url_entry = ctk.CTkEntry(app.settings_frame, placeholder_text="e.g. http://localhost:11434/v1", width=340, fg_color=colors["bg_input"], border_color=colors["border"], text_color=colors["text_primary"])
    app.base_url_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    # Model Selection & Sync Models Row
    ctk.CTkLabel(app.settings_frame, text="Model:", font=ctk.CTkFont(weight="bold"), text_color=colors["text_primary"]).grid(row=3, column=0, padx=16, pady=10, sticky="w")

    app.model_combo_frame = ctk.CTkFrame(app.settings_frame, fg_color="transparent")
    app.model_combo_frame.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky="w")

    app.model_combo = ctk.CTkComboBox(
        app.model_combo_frame, 
        values=PROVIDER_MODELS["OpenAI"],
        command=lambda selected: app._update_config_status_label(),
        width=230,
        fg_color=colors["bg_input"],
        border_color=colors["border"],
        button_color=colors["border"],
        dropdown_fg_color=colors["bg_card"],
        text_color=colors["text_primary"]
    )
    app.model_combo.pack(side="left", padx=(0, 8))

    app.sync_models_btn = ctk.CTkButton(
        app.model_combo_frame, 
        text="🔄 Sync Models", 
        command=app._sync_models, 
        width=120,
        height=30,
        font=ctk.CTkFont(weight="bold"),
        fg_color=colors["primary"],
        hover_color=colors["primary_hover"],
        text_color="#FFFFFF",
        text_color_disabled="#E5E7EB"
    )
    app.sync_models_btn.pack(side="left")

    # Dynamic Model Recommendation & Pricing Info Pill Card
    app.model_info_card = ctk.CTkFrame(
        app.settings_frame,
        fg_color=colors["bg_card_hover"],
        border_width=1,
        border_color=colors["border"],
        corner_radius=8
    )
    app.model_info_card.grid(row=4, column=0, columnspan=3, padx=16, pady=(2, 10), sticky="ew")

    app.model_rec_label = ctk.CTkLabel(
        app.model_info_card,
        text="💡 Recommended Use: ⚡ Fast & Cheap (Best for Bulk Rewriting & Outlines)",
        font=ctk.CTkFont(size=11, weight="bold"),
        text_color=colors["text_accent"]
    )
    app.model_rec_label.pack(anchor="w", padx=12, pady=(6, 2))

    app.model_cost_label = ctk.CTkLabel(
        app.model_info_card,
        text="📊 Est. Token Rate: $0.15 in / $0.60 out per 1M tokens",
        font=ctk.CTkFont(size=10),
        text_color=colors["text_secondary"]
    )
    app.model_cost_label.pack(anchor="w", padx=12, pady=(0, 6))

    # Concurrent Threads Row
    ctk.CTkLabel(app.settings_frame, text="Worker Threads:", font=ctk.CTkFont(weight="bold"), text_color=colors["text_primary"]).grid(row=5, column=0, padx=16, pady=10, sticky="w")
    app.workers_combo = ctk.CTkComboBox(
        app.settings_frame, 
        values=["1", "2", "3", "5", "8", "10"],
        command=lambda selected: app._update_config_status_label(),
        width=100,
        fg_color=colors["bg_input"],
        border_color=colors["border"],
        button_color=colors["border"],
        dropdown_fg_color=colors["bg_card"],
        text_color=colors["text_primary"]
    )
    app.workers_combo.set("3")
    app.workers_combo.grid(row=5, column=1, padx=10, pady=10, sticky="w")

    # Main Output Save Folder Row
    ctk.CTkLabel(app.settings_frame, text="Main Save Folder:", font=ctk.CTkFont(weight="bold"), text_color=colors["text_primary"]).grid(row=6, column=0, padx=16, pady=10, sticky="w")
    app.save_folder_entry = ctk.CTkEntry(app.settings_frame, width=340, fg_color=colors["bg_input"], border_color=colors["border"], text_color=colors["text_primary"])
    app.save_folder_entry.insert(0, os.path.join(os.getcwd(), "output_results"))
    app.save_folder_entry.grid(row=6, column=1, padx=10, pady=10, sticky="w")

    app.browse_btn = ctk.CTkButton(
        app.settings_frame, 
        text="Browse...", 
        command=app._browse_save_folder, 
        width=100,
        font=ctk.CTkFont(weight="bold"),
        fg_color=colors["bg_card"],
        hover_color=colors["bg_card_hover"],
        border_width=1,
        border_color=colors["border"],
        text_color=colors["text_primary"]
    )
    app.browse_btn.grid(row=6, column=2, padx=5, pady=10, sticky="w")

    # =========================================================================
    # CARD 2: AI PROVIDER & MODEL PRESETS MANAGEMENT
    # =========================================================================
    app.preset_mgmt_frame = ctk.CTkFrame(
        parent_container,
        fg_color=colors["bg_card"],
        border_width=1,
        border_color=colors["border"],
        corner_radius=12
    )
    app.preset_mgmt_frame.pack(fill="x", padx=14, pady=10)

    ctk.CTkLabel(
        app.preset_mgmt_frame,
        text="🎛️ AI Provider & Model Presets",
        font=ctk.CTkFont(size=14, weight="bold"),
        text_color=colors["text_primary"]
    ).pack(anchor="w", padx=16, pady=(14, 2))

    ctk.CTkLabel(
        app.preset_mgmt_frame,
        text="Save your active AI Provider, Model, and Threads as a Preset to switch instantly from the top toolbar dropdown.",
        font=ctk.CTkFont(size=11),
        text_color=colors["text_secondary"]
    ).pack(anchor="w", padx=16, pady=(0, 12))

    # Row 1: Save New Preset
    row_save_preset = ctk.CTkFrame(app.preset_mgmt_frame, fg_color="transparent")
    row_save_preset.pack(fill="x", padx=16, pady=(0, 10))

    ctk.CTkLabel(row_save_preset, text="Preset Name:", font=ctk.CTkFont(weight="bold"), text_color=colors["text_primary"]).pack(side="left", padx=(0, 10))

    app.new_preset_name_entry = ctk.CTkEntry(
        row_save_preset,
        placeholder_text="e.g. ⚡ Fast Gemini (gemini-2.0-flash)",
        width=320,
        fg_color=colors["bg_input"],
        border_color=colors["border"],
        text_color=colors["text_primary"]
    )
    app.new_preset_name_entry.pack(side="left", padx=(0, 10))

    app.btn_save_ai_preset = ctk.CTkButton(
        row_save_preset,
        text="💾 Save Current Configuration as Preset",
        command=app._save_ai_preset,
        height=36,
        font=ctk.CTkFont(size=11, weight="bold"),
        fg_color=colors["primary"],
        hover_color=colors["primary_hover"],
        text_color="#FFFFFF"
    )
    app.btn_save_ai_preset.pack(side="left")

    # Row 2: Manage / Delete Existing Presets
    row_del_preset = ctk.CTkFrame(app.preset_mgmt_frame, fg_color="transparent")
    row_del_preset.pack(fill="x", padx=16, pady=(0, 16))

    ctk.CTkLabel(row_del_preset, text="Manage Saved Presets:", font=ctk.CTkFont(weight="bold"), text_color=colors["text_primary"]).pack(side="left", padx=(0, 10))

    app.settings_preset_combo = ctk.CTkComboBox(
        row_del_preset,
        values=["No Presets"],
        width=320,
        height=36,
        fg_color=colors["bg_input"],
        border_color=colors["border"],
        button_color=colors["border"],
        dropdown_fg_color=colors["bg_card"],
        text_color=colors["text_primary"]
    )
    app.settings_preset_combo.pack(side="left", padx=(0, 10))

    app.btn_delete_ai_preset = ctk.CTkButton(
        row_del_preset,
        text="🗑️ Delete Selected Preset",
        command=app._delete_ai_preset,
        height=36,
        font=ctk.CTkFont(size=11, weight="bold"),
        fg_color="transparent",
        border_width=1,
        border_color=colors["danger"],
        text_color=colors["danger"],
        hover_color=colors["bg_card_hover"]
    )
    app.btn_delete_ai_preset.pack(side="left")

    # =========================================================================
    # CARD 3: 🌐 WORDPRESS REST API INTEGRATION CREDENTIALS
    # =========================================================================
    app.wp_frame = ctk.CTkFrame(
        parent_container,
        fg_color=colors["bg_card"],
        border_width=1,
        border_color=colors["border"],
        corner_radius=12
    )
    app.wp_frame.pack(fill="x", padx=14, pady=10)

    ctk.CTkLabel(
        app.wp_frame,
        text="🌐 WordPress REST API Publishing Credentials",
        font=ctk.CTkFont(size=14, weight="bold"),
        text_color=colors["text_primary"]
    ).pack(anchor="w", padx=16, pady=(14, 2))

    ctk.CTkLabel(
        app.wp_frame,
        text="Connect your WordPress site via Application Password to enable 1-click direct publishing.",
        font=ctk.CTkFont(size=11),
        text_color=colors["text_secondary"]
    ).pack(anchor="w", padx=16, pady=(0, 12))

    wp_grid = ctk.CTkFrame(app.wp_frame, fg_color="transparent")
    wp_grid.pack(fill="x", padx=16, pady=(0, 14))

    ctk.CTkLabel(wp_grid, text="Site URL:", font=ctk.CTkFont(weight="bold"), text_color=colors["text_primary"]).grid(row=0, column=0, pady=6, sticky="w")
    app.wp_url_entry = ctk.CTkEntry(wp_grid, placeholder_text="e.g. https://myblog.com", width=340, fg_color=colors["bg_input"], border_color=colors["border"], text_color=colors["text_primary"])
    app.wp_url_entry.grid(row=0, column=1, padx=10, pady=6, sticky="w")

    ctk.CTkLabel(wp_grid, text="Username:", font=ctk.CTkFont(weight="bold"), text_color=colors["text_primary"]).grid(row=1, column=0, pady=6, sticky="w")
    app.wp_user_entry = ctk.CTkEntry(wp_grid, placeholder_text="WordPress Admin Username", width=340, fg_color=colors["bg_input"], border_color=colors["border"], text_color=colors["text_primary"])
    app.wp_user_entry.grid(row=1, column=1, padx=10, pady=6, sticky="w")

    ctk.CTkLabel(wp_grid, text="App Password:", font=ctk.CTkFont(weight="bold"), text_color=colors["text_primary"]).grid(row=2, column=0, pady=6, sticky="w")
    app.wp_pass_entry = ctk.CTkEntry(wp_grid, show="•", placeholder_text="abcd 1234 efgh 5678", width=340, fg_color=colors["bg_input"], border_color=colors["border"], text_color=colors["text_primary"])
    app.wp_pass_entry.grid(row=2, column=1, padx=10, pady=6, sticky="w")

    btn_wp_test = ctk.CTkButton(
        wp_grid,
        text="🔌 Test Connection",
        command=app._test_wp_connection,
        width=140,
        height=32,
        font=ctk.CTkFont(weight="bold"),
        fg_color=colors["primary"],
        hover_color=colors["primary_hover"],
        text_color="#FFFFFF"
    )
    btn_wp_test.grid(row=2, column=2, padx=8, pady=6, sticky="w")

    # =========================================================================
    # CARD 4: 🔍 SERP & SCREAMING FROG TOOL INTEGRATIONS
    # =========================================================================
    app.tools_frame = ctk.CTkFrame(
        parent_container,
        fg_color=colors["bg_card"],
        border_width=1,
        border_color=colors["border"],
        corner_radius=12
    )
    app.tools_frame.pack(fill="x", padx=14, pady=10)

    ctk.CTkLabel(
        app.tools_frame,
        text="🛠️ SerpAPI & Screaming Frog SEO Integrations",
        font=ctk.CTkFont(size=14, weight="bold"),
        text_color=colors["text_primary"]
    ).pack(anchor="w", padx=16, pady=(14, 2))

    tools_grid = ctk.CTkFrame(app.tools_frame, fg_color="transparent")
    tools_grid.pack(fill="x", padx=16, pady=(0, 14))

    ctk.CTkLabel(tools_grid, text="SerpAPI Key:", font=ctk.CTkFont(weight="bold"), text_color=colors["text_primary"]).grid(row=0, column=0, pady=6, sticky="w")
    app.serpapi_entry = ctk.CTkEntry(tools_grid, show="•", placeholder_text="SerpAPI Key (Optional for Google SERP JSON)", width=340, fg_color=colors["bg_input"], border_color=colors["border"], text_color=colors["text_primary"])
    app.serpapi_entry.grid(row=0, column=1, padx=10, pady=6, sticky="w")

    ctk.CTkLabel(tools_grid, text="Screaming Frog Path:", font=ctk.CTkFont(weight="bold"), text_color=colors["text_primary"]).grid(row=1, column=0, pady=6, sticky="w")
    app.sf_path_entry = ctk.CTkEntry(tools_grid, placeholder_text=r"C:\Program Files (x86)\Screaming Frog SEO Spider\ScreamingFrogSEOSpiderCli.exe", width=340, fg_color=colors["bg_input"], border_color=colors["border"], text_color=colors["text_primary"])
    app.sf_path_entry.grid(row=1, column=1, padx=10, pady=6, sticky="w")

    # About Card
    app.about_frame = ctk.CTkFrame(
        parent_container,
        fg_color=colors["bg_card"],
        border_width=1,
        border_color=colors["border"],
        corner_radius=12
    )
    app.about_frame.pack(fill="x", padx=14, pady=(10, 14))

    ctk.CTkLabel(
        app.about_frame, 
        text="⚡ Application Developed by @mahethekiller", 
        font=ctk.CTkFont(size=13, weight="bold"),
        text_color=colors["text_accent"]
    ).pack(anchor="w", padx=16, pady=14)
