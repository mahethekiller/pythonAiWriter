"""
Tab 3: Configuration & Settings UI view construction with Cyber-Dark glassmorphism styling.
"""

import os
import customtkinter as ctk
from core.config import PROVIDER_MODELS

def build_settings_tab(app, parent_container):
    """Builds all UI frames for the Configuration & Settings tab."""
    
    app.settings_frame = ctk.CTkFrame(
        parent_container, 
        fg_color="#161e2e", 
        border_width=1, 
        border_color="#2a364f", 
        corner_radius=10
    )
    app.settings_frame.pack(fill="x", padx=10, pady=8)

    # Provider Selection Row
    ctk.CTkLabel(app.settings_frame, text="AI Provider:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=10, sticky="w")
    app.provider_combo = ctk.CTkComboBox(
        app.settings_frame, 
        values=list(PROVIDER_MODELS.keys()),
        command=app._on_provider_change,
        width=220
    )
    app.provider_combo.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    info_provider_btn = ctk.CTkButton(
        app.settings_frame, 
        text="ℹ️", 
        width=32, 
        height=28, 
        fg_color="#334155", 
        hover_color="#475569",
        command=lambda: app.show_info_popup(
            "AI API Providers",
            "Select your AI Service Provider.\n\n"
            "• OpenAI: gpt-4o, gpt-4o-mini, o1\n"
            "• Google Gemini: gemini-1.5-flash, gemini-1.5-pro\n"
            "• Anthropic Claude: claude-3-5-haiku, claude-3-5-sonnet\n"
            "• DeepSeek: deepseek-chat, deepseek-reasoner\n"
            "• Groq: ultra-fast open source models\n"
            "• Ollama: local offline LLMs running on localhost:11434"
        )
    )
    info_provider_btn.grid(row=0, column=2, padx=5, pady=10, sticky="w")

    # API Key Entry Row
    app.api_key_label = ctk.CTkLabel(app.settings_frame, text="API Key:", font=ctk.CTkFont(weight="bold"))
    app.api_key_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    app.api_key_entry = ctk.CTkEntry(app.settings_frame, show="•", width=320)
    app.api_key_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    app.save_key_btn = ctk.CTkButton(app.settings_frame, text="Save Key", command=app._save_api_key, width=90, fg_color="#10b981", hover_color="#059669")
    app.save_key_btn.grid(row=1, column=2, padx=5, pady=10, sticky="w")

    # Custom Base URL Row (for Ollama / OpenAI Compatible APIs)
    app.base_url_label = ctk.CTkLabel(app.settings_frame, text="Base URL (Optional):", font=ctk.CTkFont(weight="bold"))
    app.base_url_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    app.base_url_entry = ctk.CTkEntry(app.settings_frame, placeholder_text="e.g. http://localhost:11434/v1", width=320)
    app.base_url_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    info_baseurl_btn = ctk.CTkButton(
        app.settings_frame, 
        text="ℹ️", 
        width=32, 
        height=28, 
        fg_color="#334155", 
        hover_color="#475569",
        command=lambda: app.show_info_popup(
            "Base URL Configuration",
            "Overrides standard API endpoints.\n\n"
            "Use this for custom proxies or local API servers:\n"
            "• Ollama Local: http://localhost:11434/v1\n"
            "• vLLM / LocalAI: http://localhost:8000/v1"
        )
    )
    info_baseurl_btn.grid(row=2, column=2, padx=5, pady=10, sticky="w")

    # Model Selection & Sync Models Row
    ctk.CTkLabel(app.settings_frame, text="Model:", font=ctk.CTkFont(weight="bold")).grid(row=3, column=0, padx=10, pady=10, sticky="w")

    app.model_combo_frame = ctk.CTkFrame(app.settings_frame, fg_color="transparent")
    app.model_combo_frame.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky="w")

    app.model_combo = ctk.CTkComboBox(
        app.model_combo_frame, 
        values=PROVIDER_MODELS["OpenAI"],
        command=lambda selected: app._update_config_status_label(),
        width=230
    )
    app.model_combo.pack(side="left", padx=(0, 8))
    app.model_combo.bind("<KeyRelease>", lambda e: app._update_config_status_label())

    app.sync_models_btn = ctk.CTkButton(
        app.model_combo_frame, 
        text="🔄 Sync Models", 
        command=app._sync_models, 
        width=110,
        fg_color="#2563eb",
        hover_color="#1d4ed8"
    )
    app.sync_models_btn.pack(side="left")

    # Concurrent Threads Row
    ctk.CTkLabel(app.settings_frame, text="Worker Threads:", font=ctk.CTkFont(weight="bold")).grid(row=4, column=0, padx=10, pady=10, sticky="w")
    app.workers_combo = ctk.CTkComboBox(
        app.settings_frame, 
        values=["1", "2", "3", "5", "8", "10"],
        command=lambda selected: app._update_config_status_label(),
        width=90
    )
    app.workers_combo.set("3")
    app.workers_combo.grid(row=4, column=1, padx=10, pady=10, sticky="w")

    # Main Output Save Folder Row
    ctk.CTkLabel(app.settings_frame, text="Main Save Folder:", font=ctk.CTkFont(weight="bold")).grid(row=5, column=0, padx=10, pady=10, sticky="w")
    app.save_folder_entry = ctk.CTkEntry(app.settings_frame, width=320)
    app.save_folder_entry.insert(0, os.path.join(os.getcwd(), "output_results"))
    app.save_folder_entry.grid(row=5, column=1, padx=10, pady=10, sticky="w")

    app.browse_btn = ctk.CTkButton(app.settings_frame, text="Browse...", command=app._browse_save_folder, width=90)
    app.browse_btn.grid(row=5, column=2, padx=5, pady=10, sticky="w")

    # About & Developer Credits Frame
    app.about_frame = ctk.CTkFrame(
        parent_container,
        fg_color="#161e2e",
        border_width=1,
        border_color="#2a364f",
        corner_radius=10
    )
    app.about_frame.pack(fill="x", padx=10, pady=(10, 5))

    ctk.CTkLabel(
        app.about_frame, 
        text="⚡ Application Developed by @mahethekiller", 
        font=ctk.CTkFont(size=12, weight="bold"),
        text_color="#38bdf8"
    ).pack(anchor="w", padx=14, pady=10)
