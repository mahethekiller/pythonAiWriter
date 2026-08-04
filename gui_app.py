#!/usr/bin/env python3
"""
Desktop GUI Application for Web Content Rewriting & Document Generation
========================================================================
Built with CustomTkinter featuring single-page unified views, AI Provider & Model Presets system,
consolidated Settings & API Keys navigation, top toolbar preset selector, right live preview panel,
bottom status bar, and native Light/Dark mode tuple colors.
"""

import os
import sys
import json
import time
import threading
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple, Callable
from dotenv import load_dotenv, set_key

# Import core backend and UI package modules
from core import (
    run_batch_process, 
    MultiProviderLLMClient, 
    run_blog_batch_process, 
    PROVIDER_MODELS, 
    ENV_KEY_MAP,
    MODEL_PRICING_USD,
    DatabaseManager,
    LLMRouter,
    AIHumanizer,
    WordPressPublisher,
    SitemapMiner,
    SERPCrawler,
    ScreamingFrogClient,
    ReadabilityAuditor,
    SemrushGapAnalyzer,
    DisavowGenerator,
    AICitationTracker,
    SemrushClient
)
from ui import (
    ConfigManager,
    ThemeManager,
    SidebarComponent,
    ToolbarComponent,
    StatusBarComponent,
    PreviewPanelComponent,
    build_dashboard_view,
    build_blog_view,
    build_settings_view,
    build_templates_view,
    build_history_view,
    build_humanizer_view,
    build_serp_view,
    build_audit_view,
    build_publisher_view,
    build_gap_view,
    build_citation_view
)


class RewriterGUI(ctk.CTk):
    """Main Application Window with AI Provider & Model Presets system."""

    def __init__(self):
        super().__init__()

        self.title("AI Content Rewriter & SEO Article Generator Studio")
        self.geometry("1340, 860")
        self.minsize(1024, 700)

        # Load environment variables
        self.env_file = Path(__file__).parent / ".env"
        if not self.env_file.exists():
            self.env_file.touch()
        load_dotenv(self.env_file)

        # Config Manager initialization
        self.config_file = Path(__file__).parent / "app_config.json"
        self.config_mgr = ConfigManager(self.config_file)
        self.config_data = self.config_mgr.data

        # Database Manager initialization
        self.db_mgr = DatabaseManager()

        # Theme Manager Initialization
        saved_theme = self.config_data.get("theme", "Dark")
        self.theme_mgr = ThemeManager(initial_mode=saved_theme)

        # Runtime State
        self.output_dir = None
        self.excel_path = None
        self.cost_report_path = None
        self.blog_output_dir = None
        self.blog_excel_path = None
        self.is_processing = False
        self.active_view_id = "blog"
        self.last_generated_html = ""

        self.view_containers: Dict[str, ctk.CTkScrollableFrame] = {}

        self._build_ui()

    def _save_config(self):
        """Saves active configuration via config manager."""
        self.config_mgr.save()

    def _toggle_theme(self):
        """Toggles between Dark Mode and Light Mode natively via CustomTkinter."""
        new_mode = self.theme_mgr.toggle_theme()
        self.config_data["theme"] = new_mode
        self._save_config()

    def _build_ui(self):
        """Constructs layout with consolidated navigation and unified single-page views."""
        colors = self.theme_mgr.colors
        self.configure(fg_color=colors["bg_app"])

        # 1. Left Sidebar
        self.sidebar = SidebarComponent(
            self, 
            self.theme_mgr, 
            on_nav_change=self._show_view
        )
        self.sidebar.pack(side="left", fill="y")

        # 2. Main Content Wrapper Frame
        self.main_wrapper = ctk.CTkFrame(self, fg_color=colors["bg_app"], corner_radius=0)
        self.main_wrapper.pack(side="left", fill="both", expand=True)

        # 3. Top Toolbar
        self.toolbar = ToolbarComponent(
            self.main_wrapper, 
            self.theme_mgr, 
            on_theme_toggle=self._toggle_theme,
            on_primary_action=self._handle_primary_action,
            on_preset_change=self._apply_ai_preset
        )
        self.toolbar.pack(fill="x", side="top")

        # 4. Bottom Status Bar
        self.statusbar = StatusBarComponent(
            self.main_wrapper, 
            self.theme_mgr
        )
        self.statusbar.pack(fill="x", side="bottom")

        # 5. Right Live Preview & SEO Score Sidebar
        callbacks = {
            "open_folder": self._open_output_folder,
            "open_excel": self._open_excel_file,
            "open_cost": self._open_cost_file,
            "on_wp_publish": self._publish_to_wordpress
        }
        self.preview_panel = PreviewPanelComponent(
            self.main_wrapper, 
            self.theme_mgr, 
            callbacks=callbacks
        )
        self.preview_panel.pack(side="right", fill="y")

        # 6. Center View Switcher Area
        self.center_area = ctk.CTkFrame(self.main_wrapper, fg_color=colors["bg_app"])
        self.center_area.pack(side="left", fill="both", expand=True, padx=4, pady=4)

        # Build View Containers for all Navigation items
        views = ["dashboard", "rewriter", "blog", "humanizer", "serp", "gap", "citation", "audit", "publisher", "templates", "history", "settings"]
        for v in views:
            container = ctk.CTkScrollableFrame(
                self.center_area, 
                fg_color=colors["bg_app"]
            )
            self.view_containers[v] = container

        # Populate View Layouts
        build_dashboard_view(self, self.view_containers["dashboard"])
        build_dashboard_view(self, self.view_containers["rewriter"])
        build_blog_view(self, self.view_containers["blog"])
        build_humanizer_view(self, self.view_containers["humanizer"])
        build_serp_view(self, self.view_containers["serp"])
        build_gap_view(self, self.view_containers["gap"])
        build_citation_view(self, self.view_containers["citation"])
        build_audit_view(self, self.view_containers["audit"])
        build_publisher_view(self, self.view_containers["publisher"])
        build_templates_view(self, self.view_containers["templates"])
        build_history_view(self, self.view_containers["history"])
        build_settings_view(self, self.view_containers["settings"])

        # Initial provider & view setup
        last_provider = self.config_data.get("last_provider", "OpenAI")
        self.provider_combo.set(last_provider)
        self._on_provider_change(last_provider)

        # Populate AI Presets Dropdowns
        self._refresh_ai_presets_list()

        self._show_view("blog")

    def _show_view(self, view_id: str):
        """Switches active view container and updates toolbar/sidebar states."""
        self.active_view_id = view_id
        for v_id, container in self.view_containers.items():
            container.pack_forget()

        target_container = self.view_containers.get(view_id)
        if target_container:
            target_container.pack(fill="both", expand=True)

        self.sidebar.set_active(view_id)
        self.toolbar.set_view_title(view_id)

    def _handle_primary_action(self):
        """Executes current view's primary start button."""
        if self.active_view_id == "blog":
            self._start_blog_generation()
        elif self.active_view_id == "humanizer":
            self._run_standalone_humanizer()
        elif self.active_view_id == "serp":
            self._run_standalone_serp_research()
        elif self.active_view_id == "gap":
            self._run_semrush_gap_analysis()
        elif self.active_view_id == "citation":
            self._run_ai_citation_check()
        elif self.active_view_id == "audit":
            self._run_screaming_frog_audit()
        elif self.active_view_id == "publisher":
            self._publish_to_wordpress()
        else:
            self._start_processing()

    def show_info_popup(self, title: str, message: str):
        """Shows informative dialog popups."""
        messagebox.showinfo(title, message)

    def _on_provider_change(self, selected_provider: str):
        """Handles provider change and updates model combobox dropdown options."""
        self.config_data["last_provider"] = selected_provider
        self._save_config()

        env_var = ENV_KEY_MAP.get(selected_provider, "")
        saved_key = os.getenv(env_var, "")
        self.api_key_entry.delete(0, "end")
        if saved_key:
            self.api_key_entry.insert(0, saved_key)

        models = PROVIDER_MODELS.get(selected_provider, [])
        self.model_combo.configure(values=models)
        if models:
            saved_model = self.config_data.get("last_models", {}).get(selected_provider, models[0])
            if saved_model in models:
                self.model_combo.set(saved_model)
            else:
                self.model_combo.set(models[0])

        base_url_map = self.config_data.get("provider_base_urls", {})
        saved_base_url = base_url_map.get(selected_provider, "")
        self.base_url_entry.delete(0, "end")
        if saved_base_url:
            self.base_url_entry.insert(0, saved_base_url)

        self._update_config_status_label()

    def _save_api_key(self):
        """Saves active API key into .env file."""
        provider = self.provider_combo.get()
        key_val = self.api_key_entry.get().strip()
        env_var = ENV_KEY_MAP.get(provider, "")
        base_url = self.base_url_entry.get().strip()

        if env_var:
            set_key(str(self.env_file), env_var, key_val)
            os.environ[env_var] = key_val

        if "provider_base_urls" not in self.config_data:
            self.config_data["provider_base_urls"] = {}
        self.config_data["provider_base_urls"][provider] = base_url

        self._save_config()
        self._update_config_status_label()
        messagebox.showinfo("Key Saved", f"Successfully saved API key for {provider}!")

    def _update_config_status_label(self):
        """Updates internal state config."""
        provider = self.provider_combo.get()
        model = self.model_combo.get()
        if "last_models" not in self.config_data:
            self.config_data["last_models"] = {}
        self.config_data["last_models"][provider] = model
        self._save_config()

    def _sync_models(self):
        """Queries AI Provider API endpoints in background thread to refresh available models."""
        provider = self.provider_combo.get()
        api_key = self.api_key_entry.get().strip()
        base_url = self.base_url_entry.get().strip() or None

        if not api_key:
            env_var = ENV_KEY_MAP.get(provider, "")
            api_key = os.getenv(env_var, "").strip()

        if not api_key and provider != "Ollama":
            messagebox.showwarning("API Key Required", f"Please enter an API Key for {provider} before syncing models.")
            return

        self.sync_models_btn.configure(state="disabled", text="⏳ Syncing...")
        self.statusbar.set_status(f"Syncing {provider} models...", is_running=True)

        def _worker():
            try:
                fetched_models = MultiProviderLLMClient.list_models(provider, api_key, base_url)
                def _update_ui():
                    self.sync_models_btn.configure(state="normal", text="🔄 Sync Models")
                    self.statusbar.set_status("Ready", is_running=False)
                    if fetched_models:
                        PROVIDER_MODELS[provider] = fetched_models
                        self.model_combo.configure(values=fetched_models)
                        self.model_combo.set(fetched_models[0])
                        self._update_config_status_label()
                        messagebox.showinfo("Sync Success", f"Found {len(fetched_models)} models for {provider}!\n\nModels: {', '.join(fetched_models[:5])}...")
                    else:
                        messagebox.showwarning("Sync Warning", f"No dynamic models returned for {provider}. Keeping defaults.")
                self.after(0, _update_ui)
            except Exception as exc:
                err_msg = str(exc)
                def _show_err():
                    self.sync_models_btn.configure(state="normal", text="🔄 Sync Models")
                    self.statusbar.set_status("Error", is_running=False)
                    messagebox.showerror("Sync Failed", f"Failed to sync models for {provider}:\n{err_msg}")
                self.after(0, _show_err)

        threading.Thread(target=_worker, daemon=True).start()

    def _refresh_ai_presets_list(self):
        """Refreshes saved AI Presets list in both top bar and Settings dropdowns."""
        presets_dict = self.config_data.get("ai_presets", {})
        preset_names = list(presets_dict.keys())
        if not preset_names:
            preset_names = ["No Saved Presets"]

        self.toolbar.update_preset_list(preset_names)
        self.settings_preset_combo.configure(values=preset_names)
        if preset_names:
            self.settings_preset_combo.set(preset_names[0])

    def _save_ai_preset(self):
        """Saves current AI Provider, Model, and Threads as a named Preset."""
        name = self.new_preset_name_entry.get().strip()
        if not name:
            messagebox.showwarning("Preset Name Required", "Please enter a descriptive name for your new preset.")
            return

        provider = self.provider_combo.get()
        model = self.model_combo.get()
        workers = self.workers_combo.get()

        if "ai_presets" not in self.config_data:
            self.config_data["ai_presets"] = {}

        self.config_data["ai_presets"][name] = {
            "provider": provider,
            "model": model,
            "workers": workers
        }
        self._save_config()
        self.new_preset_name_entry.delete(0, "end")
        self._refresh_ai_presets_list()
        self.toolbar.update_preset_list(list(self.config_data["ai_presets"].keys()), current_preset=name)
        messagebox.showinfo("Preset Saved", f"Successfully saved preset '{name}'!")

    def _delete_ai_preset(self):
        """Deletes selected preset from config data."""
        preset_name = self.settings_preset_combo.get()
        if not preset_name or preset_name == "No Saved Presets":
            messagebox.showwarning("No Preset Selected", "Please select a valid preset to delete.")
            return

        if "ai_presets" in self.config_data and preset_name in self.config_data["ai_presets"]:
            del self.config_data["ai_presets"][preset_name]
            self._save_config()
            self._refresh_ai_presets_list()
            messagebox.showinfo("Preset Deleted", f"Deleted preset '{preset_name}'.")

    def _apply_ai_preset(self, preset_name: str):
        """Applies configuration from selected preset name."""
        presets_dict = self.config_data.get("ai_presets", {})
        if preset_name in presets_dict:
            cfg = presets_dict[preset_name]
            p = cfg.get("provider", "OpenAI")
            m = cfg.get("model", "gpt-4o-mini")
            w = cfg.get("workers", "3")

            self.provider_combo.set(p)
            self._on_provider_change(p)
            self.model_combo.set(m)
            self.workers_combo.set(w)
            self._update_config_status_label()
            self.statusbar.set_task(f"Active Preset: {preset_name}")

    def _run_standalone_humanizer(self):
        """Runs standalone AI Humanizer polish pass."""
        text = self.humanizer_input_textbox.get("1.0", "end").strip()
        if not text:
            messagebox.showwarning("Text Required", "Please paste HTML or text to humanize.")
            return

        provider = self.provider_combo.get()
        api_key = self.api_key_entry.get().strip() or os.getenv(ENV_KEY_MAP.get(provider, ""), "")
        model = self.model_combo.get().strip()
        base_url = self.base_url_entry.get().strip() or None

        self.statusbar.set_status("Humanizing Content...", is_running=True)

        def _worker():
            try:
                router = LLMRouter(active_provider=provider, active_model=model, api_key=api_key, base_url=base_url, db_mgr=self.db_mgr)
                humanizer = AIHumanizer(router=router)
                result = humanizer.humanize_text(text)

                readability_stats = ReadabilityAuditor.calculate_flesch_reading_ease(result)

                def _update():
                    self.statusbar.set_status("Ready", is_running=False)
                    self.humanizer_output_textbox.delete("1.0", "end")
                    out_msg = (
                        f"--- READABILITY & CONTENT AUDIT ---\n"
                        f"• Flesch Reading Ease : {readability_stats['flesch_score']}/100 ({readability_stats['reading_ease']})\n"
                        f"• Grade Level        : {readability_stats['grade_level']}\n"
                        f"• Word Count         : {readability_stats['word_count']} words\n\n"
                        f"--- HUMANIZED TEXT CONTENT ---\n{result}"
                    )
                    self.humanizer_output_textbox.insert("1.0", out_msg)
                    messagebox.showinfo("Humanizer Complete", "Content successfully polished and humanized!")

                self.after(0, _update)

            except Exception as exc:
                err_msg = str(exc)
                def _show_err():
                    self.statusbar.set_status("Error", is_running=False)
                    messagebox.showerror("Humanizer Error", f"Failed to humanize content:\n{err_msg}")
                self.after(0, _show_err)

        threading.Thread(target=_worker, daemon=True).start()

    def _run_standalone_serp_research(self):
        """Runs standalone SERP Intelligence crawler."""
        kw = self.serp_kw_entry.get().strip()
        if not kw:
            messagebox.showwarning("Keyword Required", "Please enter a primary keyword to search.")
            return

        serpapi_key = getattr(self, 'serpapi_entry', None) and self.serpapi_entry.get().strip() or os.getenv("SERPAPI_KEY", "")
        self.statusbar.set_status(f"Fetching SERP intel for '{kw}'...", is_running=True)

        def _worker():
            try:
                crawler = SERPCrawler(serpapi_key=serpapi_key, db_mgr=self.db_mgr)
                intel = crawler.fetch_serp_intel(kw)
                def _update():
                    self.statusbar.set_status("Ready", is_running=False)
                    out_lines = [
                        f"🔍 SERP RESEARCH RESULTS FOR: '{kw.upper()}'\n",
                        f"• Competitor Avg Word Count: ~{intel.get('avg_word_count', 1800)} words",
                        f"\n• Top Competitor URLs Found ({len(intel.get('competitor_urls', []))}):"
                    ]
                    for u in intel.get("competitor_urls", []):
                        out_lines.append(f"  - {u}")

                    out_lines.append(f"\n• Competitor Headings Extracted ({len(intel.get('competitor_headings', []))}):")
                    for h in intel.get("competitor_headings", []):
                        out_lines.append(f"  - {h}")

                    out_lines.append(f"\n• People Also Ask (PAA) Questions ({len(intel.get('paa_questions', []))}):")
                    for q in intel.get("paa_questions", []):
                        out_lines.append(f"  - {q}")

                    self.serp_output_textbox.delete("1.0", "end")
                    self.serp_output_textbox.insert("1.0", "\n".join(out_lines))
                    messagebox.showinfo("SERP Mining Complete", f"Successfully extracted intel for '{kw}'!")
                self.after(0, _update)

            except Exception as exc:
                err_msg = str(exc)
                def _show_err():
                    self.statusbar.set_status("Error", is_running=False)
                    messagebox.showerror("SERP Research Error", f"Failed to fetch SERP intel:\n{err_msg}")
                self.after(0, _show_err)

        threading.Thread(target=_worker, daemon=True).start()

    def _run_semrush_gap_analysis(self):
        """Runs head-to-head Keyword & Content Gap analysis in background thread."""
        target_url = getattr(self, 'gap_target_url_entry', None) and self.gap_target_url_entry.get().strip() or ""
        if not target_url:
            messagebox.showwarning("Target URL Required", "Please enter your target website URL.")
            return

        comp_text = getattr(self, 'gap_comp_urls_textbox', None) and self.gap_comp_urls_textbox.get("1.0", "end").strip() or ""
        comp_urls = [u.strip() for u in comp_text.splitlines() if u.strip()]

        if not comp_urls:
            messagebox.showwarning("Competitors Required", "Please enter at least one competitor URL.")
            return

        self.statusbar.set_status("Analyzing Keyword & Content Gap...", is_running=True)

        def _worker():
            try:
                analyzer = SemrushGapAnalyzer()
                res = analyzer.analyze_gap(target_url, comp_urls)
                def _update():
                    self.statusbar.set_status("Ready", is_running=False)
                    out_lines = [
                        f"📊 SEMRUSH KEYWORD & CONTENT GAP ANALYSIS\n",
                        f"• Target URL: {res['target_url']}",
                        f"• Target Word Count: {res['target_word_count']} words",
                        f"• Avg Competitor Word Count: {res['avg_competitor_word_count']} words",
                        f"• Word Count Deficit: {res['word_count_gap']} words needed\n",
                        f"--- MISSING KEYWORDS COMPETITORS RANK FOR ({len(res['missing_keywords'])}) ---"
                    ]
                    for kw in res["missing_keywords"]:
                        out_lines.append(f"  • {kw}")

                    out_lines.append(f"\n--- MISSING CONTENT HEADINGS ({len(res['missing_headings'])}) ---")
                    for h in res["missing_headings"]:
                        out_lines.append(f"  • {h}")

                    self.gap_output_textbox.delete("1.0", "end")
                    self.gap_output_textbox.insert("1.0", "\n".join(out_lines))
                    messagebox.showinfo("Gap Analysis Complete", f"Identified {len(res['missing_keywords'])} missing keywords and {len(res['missing_headings'])} missing headings!")

                self.after(0, _update)

            except Exception as exc:
                err_msg = str(exc)
                def _show_err():
                    self.statusbar.set_status("Error", is_running=False)
                    messagebox.showerror("Gap Analysis Error", f"Failed to analyze keyword gap:\n{err_msg}")
                self.after(0, _show_err)

        threading.Thread(target=_worker, daemon=True).start()

    def _run_ai_citation_check(self):
        """Runs AI Search Visibility & Citation Check in background thread."""
        brand = getattr(self, 'cit_brand_entry', None) and self.cit_brand_entry.get().strip() or ""
        kw = getattr(self, 'cit_kw_entry', None) and self.cit_kw_entry.get().strip() or ""

        if not brand or not kw:
            messagebox.showwarning("Input Required", "Please enter both your Brand/Domain and Target Keyword.")
            return

        provider = self.provider_combo.get()
        api_key = self.api_key_entry.get().strip() or os.getenv(ENV_KEY_MAP.get(provider, ""), "")
        model = self.model_combo.get().strip()
        base_url = self.base_url_entry.get().strip() or None

        if not api_key and provider != "Ollama":
            messagebox.showwarning("API Key Required", f"Please enter an API Key for {provider} under Settings & API Keys.")
            return

        self.statusbar.set_status(f"Testing AI Citation for '{brand}'...", is_running=True)

        def _worker():
            try:
                router = LLMRouter(active_provider=provider, active_model=model, api_key=api_key, base_url=base_url, db_mgr=self.db_mgr)
                tracker = AICitationTracker(router=router)
                res = tracker.check_citation(brand, kw)

                def _update():
                    self.statusbar.set_status("Ready", is_running=False)
                    out_lines = [
                        f"🤖 AI SEARCH VISIBILITY REPORT\n",
                        f"• Brand / Domain : {res['brand_domain']}",
                        f"• Target Keyword : {res['target_keyword']}",
                        f"• Citation Status : {res['status']}\n",
                        f"--- AI MODEL RESPONSE SNIPPET ---",
                        res["ai_response_snippet"]
                    ]
                    self.cit_output_textbox.delete("1.0", "end")
                    self.cit_output_textbox.insert("1.0", "\n".join(out_lines))
                    messagebox.showinfo("AI Citation Test", f"Result: {res['status']}")

                self.after(0, _update)

            except Exception as exc:
                err_msg = str(exc)
                def _show_err():
                    self.statusbar.set_status("Error", is_running=False)
                    messagebox.showerror("AI Citation Error", f"Failed to test AI citation:\n{err_msg}")
                self.after(0, _show_err)

        threading.Thread(target=_worker, daemon=True).start()

    def _run_toxic_backlink_audit(self):
        """Audits toxic backlinks and exports a disavow.txt file."""
        text = getattr(self, 'disavow_input_textbox', None) and self.disavow_input_textbox.get("1.0", "end").strip() or ""
        if not text:
            messagebox.showwarning("Input Required", "Please enter backlink URLs or domain names to audit.")
            return

        urls = [u.strip() for u in text.splitlines() if u.strip()]
        audit_results, disavow_lines = DisavowGenerator.audit_url_list(urls)

        out_path = Path(getattr(self, 'save_folder_entry', None) and self.save_folder_entry.get() or os.getcwd()) / "disavow.txt"
        DisavowGenerator.export_disavow_file(disavow_lines, out_path)

        toxic_count = sum(1 for a in audit_results if a["is_toxic"])
        summary_msg = (
            f"Successfully audited {len(urls)} domain(s)!\n\n"
            f"🔴 Toxic Domains Flagged : {toxic_count}\n"
            f"🟢 Clean Domains         : {len(urls) - toxic_count}\n\n"
            f"📄 Google Search Console Disavow file generated at:\n{out_path}"
        )
        messagebox.showinfo("Toxic Disavow Audit Complete", summary_msg)

    def _toggle_pub_source_mode(self):
        """Swaps source mode input elements on CMS Publisher view."""
        mode = getattr(self, 'pub_source_mode_var', None) and self.pub_source_mode_var.get() or "active"
        if mode == "active":
            t = getattr(self, 'blog_topic_entry', None) and self.blog_topic_entry.get().strip() or "Generated Article"
            c = self.last_generated_html or self.preview_panel.preview_textbox.get("1.0", "end").strip()
            if hasattr(self, 'pub_title_entry'):
                self.pub_title_entry.delete(0, "end")
                self.pub_title_entry.insert(0, t)
            if hasattr(self, 'pub_content_textbox'):
                self.pub_content_textbox.delete("1.0", "end")
                self.pub_content_textbox.insert("1.0", c)

    def _browse_pub_file(self):
        """Opens file picker to select .html or .json article file to publish."""
        f_path = filedialog.askopenfilename(filetypes=[("HTML Files", "*.html"), ("JSON Files", "*.json"), ("All Files", "*.*")])
        if f_path:
            if hasattr(self, 'pub_file_entry'):
                self.pub_file_entry.delete(0, "end")
                self.pub_file_entry.insert(0, f_path)
            p = Path(f_path)
            title = p.stem.replace("-", " ").replace("_", " ").title()
            try:
                if f_path.endswith(".json"):
                    with open(f_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        title = data.get("title") or data.get("meta_title") or title
                        html_content = data.get("content_html") or ""
                else:
                    with open(f_path, "r", encoding="utf-8") as f:
                        html_content = f.read()
                
                if hasattr(self, 'pub_title_entry'):
                    self.pub_title_entry.delete(0, "end")
                    self.pub_title_entry.insert(0, title)
                if hasattr(self, 'pub_content_textbox'):
                    self.pub_content_textbox.delete("1.0", "end")
                    self.pub_content_textbox.insert("1.0", html_content)
                if hasattr(self, 'pub_source_mode_var'):
                    self.pub_source_mode_var.set("file")
            except Exception as exc:
                messagebox.showerror("File Error", f"Failed to read file: {str(exc)}")

    def _test_wp_connection(self):
        """Tests WordPress REST API credentials."""
        url = getattr(self, 'wp_url_entry', None) and self.wp_url_entry.get().strip() or ""
        user = getattr(self, 'wp_user_entry', None) and self.wp_user_entry.get().strip() or ""
        passwd = getattr(self, 'wp_pass_entry', None) and self.wp_pass_entry.get().strip() or ""
        
        if not url or not user or not passwd:
            messagebox.showwarning("Missing Credentials", "Please enter Site URL, Username, and Application Password.")
            return

        pub = WordPressPublisher(url, user, passwd)
        ok, msg = pub.test_connection()
        if ok:
            self.db_mgr.save_cms_credentials("wordpress", url, user, passwd)
            messagebox.showinfo("WordPress Connection", msg)
        else:
            messagebox.showerror("WordPress Error", msg)

    def _publish_to_wordpress(self):
        """Publishes selected article directly to WordPress REST API."""
        url = getattr(self, 'wp_url_entry', None) and self.wp_url_entry.get().strip() or ""
        user = getattr(self, 'wp_user_entry', None) and self.wp_user_entry.get().strip() or ""
        passwd = getattr(self, 'wp_pass_entry', None) and self.wp_pass_entry.get().strip() or ""

        if not url or not user or not passwd:
            creds = self.db_mgr.get_cms_credentials("wordpress")
            if creds:
                url, user, passwd = creds["site_url"], creds["username"], creds["api_key"]
            else:
                messagebox.showwarning("WordPress Config", "Please configure WordPress URL, Username, and App Password under Settings & API Keys.")
                return

        mode = getattr(self, 'pub_source_mode_var', None) and self.pub_source_mode_var.get() or "active"
        
        if mode == "custom" or mode == "file":
            title = getattr(self, 'pub_title_entry', None) and self.pub_title_entry.get().strip() or "Untitled Article"
            html_content = getattr(self, 'pub_content_textbox', None) and self.pub_content_textbox.get("1.0", "end").strip() or ""
        else:
            title = getattr(self, 'blog_topic_entry', None) and self.blog_topic_entry.get().strip() or "Generated Article"
            html_content = self.last_generated_html or self.preview_panel.preview_textbox.get("1.0", "end").strip()

        if not html_content or "Your generated article" in html_content:
            messagebox.showwarning("No Article Content", "Please select a valid article file or generate an article first.")
            return

        status = getattr(self, 'wp_status_combo', None) and self.wp_status_combo.get().strip() or "draft"

        pub = WordPressPublisher(url, user, passwd)
        res = pub.publish_post(title, html_content, status=status)
        if res.get("success"):
            messagebox.showinfo("WordPress Publish Success", res["message"])
        else:
            messagebox.showerror("Publish Error", res["message"])

    def _fetch_sitemap_links(self):
        """Fetches internal URLs from target XML sitemap."""
        url = getattr(self, 'blog_sitemap_entry', None) and self.blog_sitemap_entry.get().strip() or ""
        if not url:
            messagebox.showwarning("Missing Sitemap URL", "Please enter an XML Sitemap URL (e.g. https://myblog.com/sitemap.xml).")
            return

        def _worker():
            miner = SitemapMiner()
            urls = miner.fetch_internal_urls(url, max_urls=10)
            def _update():
                if urls:
                    self.blog_internal_links_textbox.delete("1.0", "end")
                    self.blog_internal_links_textbox.insert("1.0", "\n".join(urls))
                    messagebox.showinfo("Sitemap Miner", f"Successfully fetched {len(urls)} internal page URLs!")
                else:
                    messagebox.showwarning("Sitemap Miner", f"No valid page URLs found at '{url}'.")
            self.after(0, _update)

        threading.Thread(target=_worker, daemon=True).start()

    def _run_screaming_frog_audit(self):
        """Executes Screaming Frog technical SEO audit crawl in background thread."""
        site_url = getattr(self, 'tab_audit_url_entry', None) and self.tab_audit_url_entry.get().strip() or getattr(self, 'sf_audit_url_entry', None) and self.sf_audit_url_entry.get().strip() or ""
        cli_path = getattr(self, 'sf_path_entry', None) and self.sf_path_entry.get().strip() or ""

        if not site_url:
            messagebox.showwarning("Missing Target Site", "Please enter a target site URL to audit.")
            return

        def _worker():
            client = ScreamingFrogClient(cli_path=cli_path)
            out_dir = Path(getattr(self, 'save_folder_entry', None) and self.save_folder_entry.get() or os.getcwd()) / "sf_audit_reports"
            ok, msg = client.run_headless_crawl(site_url, out_dir)
            def _update():
                if ok:
                    messagebox.showinfo("Screaming Frog Audit", msg)
                else:
                    messagebox.showerror("Audit Error", msg)
            self.after(0, _update)

        threading.Thread(target=_worker, daemon=True).start()

    def _toggle_custom_prompt(self):
        """Toggles state of custom prompt text box in Rewriter Dashboard."""
        if self.custom_prompt_var.get():
            self.custom_prompt_textbox.configure(state="normal")
        else:
            self.custom_prompt_textbox.configure(state="disabled")

    def _browse_save_folder(self):
        """Opens folder browser to select output directory."""
        folder = filedialog.askdirectory()
        if folder:
            self.save_folder_entry.delete(0, "end")
            self.save_folder_entry.insert(0, folder)

    def _toggle_blog_mode(self):
        """Swaps UI layout elements between Single Article Mode and Batch CSV Mode."""
        mode = self.blog_mode_var.get()
        if mode == "single":
            self.blog_csv_label.grid_forget()
            self.blog_csv_entry.grid_forget()
            self.blog_csv_browse_btn.grid_forget()
            self.blog_csv_sample_btn.grid_forget()

            self.blog_topic_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 4))
            self.blog_topic_entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=(0, 10), pady=(0, 12))
        else:
            self.blog_topic_label.grid_forget()
            self.blog_topic_entry.grid_forget()

            self.blog_csv_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 4))
            self.blog_csv_entry.grid(row=1, column=0, sticky="ew", padx=(0, 4), pady=(0, 12))
            self.blog_csv_browse_btn.grid(row=1, column=1, sticky="w", padx=(0, 4), pady=(0, 12))
            self.blog_csv_sample_btn.grid(row=1, column=1, sticky="e", padx=(116, 10), pady=(0, 12))

    def _browse_blog_csv(self):
        """Opens file browser to select batch topics CSV file."""
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            self.blog_csv_entry.delete(0, "end")
            self.blog_csv_entry.insert(0, file_path)

    def _download_sample_csv(self):
        """Generates sample_batch_topics.csv template file in workspace root with 1 click."""
        sample_path = Path(os.getcwd()) / "sample_batch_topics.csv"
        df_sample = pd.DataFrame([
            {
                "topic": "10 Best Budget Laptops for College Students in 2026",
                "primary_keyword": "budget student laptops",
                "search_intent": "Commercial",
                "tone": "Conversational & Engaging",
                "format_type": "Product Comparison",
                "target_audience": "Beginners"
            },
            {
                "topic": "How to Start a Software Development Agency with Python",
                "primary_keyword": "start software agency python",
                "search_intent": "Informational",
                "tone": "Professional & Authoritative",
                "format_type": "Ultimate Guide",
                "target_audience": "Professionals"
            }
        ])
        df_sample.to_csv(sample_path, index=False)
        self.blog_csv_entry.delete(0, "end")
        self.blog_csv_entry.insert(0, str(sample_path))
        messagebox.showinfo("Sample CSV Created", f"Sample CSV file created successfully at:\n{sample_path}\n\nPath automatically populated into CSV File input!")

    def _log(self, message: str):
        """Appends log message to log text box."""
        def _append():
            self.log_textbox.insert("end", f"[{time.strftime('%H:%M:%S')}] {message}\n")
            self.log_textbox.see("end")
        self.after(0, _append)

    def _blog_log(self, message: str):
        """Appends log message to Rewriter log text box."""
        self._log(f"[SEO Blog] {message}")

    def _open_output_folder(self):
        """Opens active dated output directory in OS File Explorer."""
        target = self.blog_output_dir or self.output_dir
        if target and target.exists():
            os.startfile(target)
        else:
            messagebox.showwarning("Folder Not Found", "Output folder does not exist yet.")

    def _open_excel_file(self):
        """Opens active Excel report file."""
        target = self.blog_excel_path or self.excel_path
        if target and target.exists():
            os.startfile(target)
        else:
            messagebox.showwarning("File Not Found", "Excel report file does not exist yet.")

    def _open_cost_file(self):
        """Opens active Cost Report file."""
        if self.cost_report_path and self.cost_report_path.exists():
            os.startfile(self.cost_report_path)
        elif self.blog_output_dir and (self.blog_output_dir / "blog_generation_report.csv").exists():
            os.startfile(self.blog_output_dir / "blog_generation_report.csv")
        else:
            messagebox.showwarning("File Not Found", "Cost report file does not exist yet.")

    def _start_processing(self):
        """Starts batch webpage rewriting execution in background thread."""
        urls_text = self.urls_textbox.get("1.0", "end").strip()
        if not urls_text:
            messagebox.showwarning("Input Required", "Please enter at least one webpage URL.")
            return

        urls = [u.strip() for u in urls_text.splitlines() if u.strip()]
        provider = self.provider_combo.get()
        api_key = self.api_key_entry.get().strip()
        base_url = self.base_url_entry.get().strip() or None

        if not api_key:
            env_var = ENV_KEY_MAP.get(provider, "")
            api_key = os.getenv(env_var, "").strip()

        if not api_key and provider != "Ollama":
            messagebox.showwarning("API Key Required", f"Please enter an API Key for {provider}.")
            return

        main_save_folder = self.save_folder_entry.get().strip() or os.path.join(os.getcwd(), "output_results")
        mode = self.mode_combo.get()
        model = self.model_combo.get().strip()
        max_workers = int(self.workers_combo.get())

        custom_prompt = ""
        if self.custom_prompt_var.get():
            custom_prompt = self.custom_prompt_textbox.get("1.0", "end").strip()

        gen_html = self.html_var.get()
        gen_docx = self.docx_var.get()

        self.is_processing = True
        self.start_time = time.time()
        self.start_btn.configure(state="disabled", text="⏳ Rewriting Content...")

        self.statusbar.set_status("Processing URLs...", is_running=True)
        self.statusbar.set_task(f"Rewriting {len(urls)} page(s)")

        threading.Thread(
            target=self._worker_thread,
            args=(urls, provider, api_key, model, mode, custom_prompt, gen_html, gen_docx, Path(main_save_folder), max_workers, base_url),
            daemon=True
        ).start()

    def _worker_thread(self, urls, provider, api_key, model, mode, custom_prompt, gen_html, gen_docx, main_save_folder, max_workers, base_url):
        def _progress_cb(completed, total, current_url):
            frac = completed / total
            def _update():
                self.statusbar.set_progress(frac)
            self.after(0, _update)

        try:
            df, excel_path, cost_file, run_output_dir, metrics = run_batch_process(
                urls=urls,
                provider=provider,
                api_key=api_key,
                model=model,
                mode=mode,
                custom_prompt=custom_prompt,
                generate_html=gen_html,
                generate_docx=gen_docx,
                main_save_folder=main_save_folder,
                max_workers=max_workers,
                base_url=base_url,
                progress_cb=_progress_cb,
                log_cb=self._log
            )

            self.output_dir = run_output_dir
            self.excel_path = excel_path
            self.cost_report_path = cost_file
            duration_sec = int(time.time() - self.start_time)

            def _on_complete():
                self.is_processing = False
                self.start_btn.configure(state="normal", text="🚀 Start Batch Rewriting")
                self.open_folder_btn.configure(state="normal")
                self.open_excel_btn.configure(state="normal")
                self.open_cost_btn.configure(state="normal")

                self.statusbar.set_status("Ready", is_running=False)
                self.statusbar.set_task("Completed rewriting run")
                self.toolbar.update_cost_badge(f"Est. Cost  ${metrics['total_cost_usd']:.3f} USD")

                summary_msg = (
                    f"Successfully processed {len(urls)} webpage URL(s)!\n\n"
                    f"📊 TOKEN CONSUMPTION & COSTING:\n"
                    f"• Prompt Tokens     : {metrics['total_prompt_tokens']:,}\n"
                    f"• Completion Tokens : {metrics['total_completion_tokens']:,}\n"
                    f"• Total Tokens      : {metrics['total_tokens']:,}\n"
                    f"• Estimated Cost    : ${metrics['total_cost_usd']:.6f} USD\n\n"
                    f"📁 Saved to dated folder:\n{self.output_dir}"
                )
                messagebox.showinfo("Processing Complete", summary_msg)

            self.after(0, _on_complete)

        except Exception as exc:
            def _on_error():
                self.is_processing = False
                self.start_btn.configure(state="normal", text="🚀 Start Batch Rewriting")
                self.statusbar.set_status("Error", is_running=False)
                messagebox.showerror("Execution Error", str(exc))

            self.after(0, _on_error)

    def _start_blog_generation(self):
        """Starts SEO Blog Article Generation execution in background thread."""
        provider = self.provider_combo.get()
        api_key = self.api_key_entry.get().strip()
        base_url = self.base_url_entry.get().strip() or None

        if not api_key:
            env_var = ENV_KEY_MAP.get(provider, "")
            api_key = os.getenv(env_var, "").strip()

        if not api_key and provider != "Ollama":
            messagebox.showwarning("API Key Required", f"Please enter an API Key for {provider}.")
            return

        main_save_folder = self.save_folder_entry.get().strip() or os.path.join(os.getcwd(), "output_results")
        mode = self.blog_mode_var.get()

        topics_data = []
        if mode == "single":
            topic = self.blog_topic_entry.get().strip()
            if not topic:
                messagebox.showwarning("Topic Required", "Please enter an Article Topic or Title.")
                return

            pk = self.blog_pk_entry.get().strip() or topic
            sk_raw = self.blog_sk_textbox.get("1.0", "end").strip()
            sk_list = [k.strip() for k in sk_raw.split(",") if k.strip()]

            links_raw = self.blog_internal_links_textbox.get("1.0", "end").strip()
            links_list = [u.strip() for u in links_raw.splitlines() if u.strip()]

            comp_raw = self.blog_comp_urls_textbox.get("1.0", "end").strip()
            comp_list = [u.strip() for u in comp_raw.splitlines() if u.strip()]

            sitemap_url = getattr(self, 'blog_sitemap_entry', None) and self.blog_sitemap_entry.get().strip() or None

            topics_data.append({
                "topic": topic,
                "primary_keyword": pk,
                "secondary_keywords": sk_list,
                "search_intent": self.blog_intent_combo.get().strip(),
                "tone": self.blog_tone_combo.get().strip(),
                "format_type": self.blog_format_combo.get().strip(),
                "target_audience": self.blog_audience_combo.get().strip(),
                "word_count_target": self.blog_wordcount_combo.get().strip(),
                "internal_links": links_list,
                "include_external_links": self.blog_ext_links_var.get(),
                "include_image_prompts": self.blog_img_prompts_var.get(),
                "custom_outline": self.blog_outline_textbox.get("1.0", "end").strip(),
                "include_tldr": self.blog_tldr_var.get(),
                "include_faq": self.blog_faq_var.get(),
                "cta_text": self.blog_cta_entry.get().strip(),
                "competitor_urls": comp_list,
                "enable_serp_mining": self.blog_serp_var.get(),
                "enable_humanizer": self.blog_humanizer_var.get(),
                "sitemap_url": sitemap_url
            })
        else:
            csv_path = self.blog_csv_entry.get().strip()
            if not csv_path or not Path(csv_path).exists():
                messagebox.showwarning("CSV File Required", "Please select a valid Batch Topics CSV file.")
                return
            try:
                if csv_path.endswith(".csv") or csv_path.endswith(".txt"):
                    df_in = pd.read_csv(csv_path)
                    for _, row in df_in.iterrows():
                        t = str(row.get("topic", "") or row.get("Topic", "")).strip()
                        if t:
                            pk = str(row.get("primary_keyword", "") or t).strip()
                            topics_data.append({
                                "topic": t,
                                "primary_keyword": pk,
                                "secondary_keywords": [],
                                "search_intent": self.blog_intent_combo.get().strip(),
                                "tone": self.blog_tone_combo.get().strip(),
                                "format_type": self.blog_format_combo.get().strip(),
                                "target_audience": self.blog_audience_combo.get().strip(),
                                "word_count_target": self.blog_wordcount_combo.get().strip(),
                                "internal_links": [],
                                "include_external_links": True,
                                "include_image_prompts": True,
                                "include_tldr": True,
                                "include_faq": True,
                                "enable_serp_mining": self.blog_serp_var.get(),
                                "enable_humanizer": self.blog_humanizer_var.get()
                            })
            except Exception as exc:
                messagebox.showerror("CSV Read Error", str(exc))
                return

        if not topics_data:
            messagebox.showwarning("No Topics Found", "No valid topics were found to process.")
            return

        gen_html = self.blog_html_var.get()
        gen_docx = self.blog_docx_var.get()
        gen_md = self.blog_md_var.get()
        gen_json = self.blog_json_var.get()

        model = self.model_combo.get().strip()
        max_workers = int(self.workers_combo.get())

        self.is_processing = True
        self.start_time = time.time()
        self.blog_start_btn.configure(state="disabled", text="⏳ Generating SEO Article(s)...")

        self.statusbar.set_status("Generating SEO Article...", is_running=True)
        self.statusbar.set_task(f"Generating article via {provider}")

        threading.Thread(
            target=self._blog_worker_thread,
            args=(topics_data, provider, api_key, model, gen_html, gen_docx, gen_md, gen_json, Path(main_save_folder), max_workers, base_url),
            daemon=True
        ).start()

    def _blog_worker_thread(self, topics_data, provider, api_key, model, gen_html, gen_docx, gen_md, gen_json, main_save_folder, max_workers, base_url):
        def _progress_cb(completed, total, current_msg):
            frac = completed / total
            def _update():
                self.statusbar.set_progress(frac)
            self.after(0, _update)

        try:
            df, excel_path, run_output_dir, metrics = run_blog_batch_process(
                topics_data=topics_data,
                provider=provider,
                api_key=api_key,
                model=model,
                generate_html=gen_html,
                generate_docx=gen_docx,
                generate_md=gen_md,
                generate_json=gen_json,
                main_save_folder=main_save_folder,
                max_workers=max_workers,
                base_url=base_url,
                progress_cb=_progress_cb,
                log_cb=self._blog_log
            )

            self.blog_output_dir = run_output_dir
            self.blog_excel_path = excel_path
            duration_sec = int(time.time() - getattr(self, 'start_time', time.time()))

            def _on_complete():
                self.is_processing = False
                self.blog_start_btn.configure(state="normal", text="🚀 Generate SEO Blog Article(s)")
                self.statusbar.set_status("Ready", is_running=False)
                self.statusbar.set_task("Completed SEO article generation")
                self.toolbar.update_cost_badge(f"Est. Cost  ${metrics['total_cost_usd']:.3f} USD")

                if metrics.get("last_article_metrics"):
                    m = metrics["last_article_metrics"]
                    self.last_generated_html = m.get("content_html_body", "")
                    self.preview_panel.update_metrics(
                        words=m.get('word_count', 0),
                        reading_time_min=m.get('reading_time_min', 1),
                        seo_score=m.get('seo_score', 85),
                        density=m.get('pk_density', 1.5),
                        readability=int(m.get('readability_score', 70)),
                        cost_str=f"${metrics['total_cost_usd']:.3f}",
                        provider_str=f"{provider} {model}",
                        duration_sec=duration_sec,
                        status_str="🟢 Completed"
                    )

                    if m.get("content_html_body"):
                        self.preview_panel.set_preview_content(m["content_html_body"])

                summary_msg = (
                    f"Successfully generated {len(topics_data)} SEO Blog Article(s)!\n\n"
                    f"📊 TOKEN CONSUMPTION & COSTING:\n"
                    f"• Prompt Tokens     : {metrics['total_prompt_tokens']:,}\n"
                    f"• Completion Tokens : {metrics['total_completion_tokens']:,}\n"
                    f"• Total Tokens      : {metrics['total_tokens']:,}\n"
                    f"• Estimated Cost    : ${metrics['total_cost_usd']:.6f} USD\n\n"
                    f"📁 Saved to dated folder:\n{self.blog_output_dir}"
                )
                messagebox.showinfo("Blog Generation Complete", summary_msg)

            self.after(0, _on_complete)

        except Exception as exc:
            def _on_error():
                self.is_processing = False
                self.blog_start_btn.configure(state="normal", text="🚀 Generate SEO Blog Article(s)")
                self.statusbar.set_status("Error", is_running=False)
                messagebox.showerror("Execution Error", str(exc))

            self.after(0, _on_error)

    def _apply_blog_preset(self, preset_name: str):
        if "Affiliate" in preset_name:
            self.blog_intent_combo.set("Commercial")
            self.blog_tone_combo.set("Persuasive")
            self.blog_format_combo.set("Product Comparison")
            self.blog_wordcount_combo.set("Standard (~1,500 words)")
            self._blog_log("Applied Strategy Preset: Affiliate Product Review")
        elif "Educational" in preset_name:
            self.blog_intent_combo.set("Informational")
            self.blog_tone_combo.set("Professional & Authoritative")
            self.blog_format_combo.set("Ultimate Guide")
            self.blog_wordcount_combo.set("Long-form (~2,500+ words)")
            self._blog_log("Applied Strategy Preset: Educational Deep-Dive")
        elif "News" in preset_name:
            self.blog_intent_combo.set("Informational")
            self.blog_tone_combo.set("Conversational & Engaging")
            self.blog_format_combo.set("Informational Explainer")
            self.blog_wordcount_combo.set("Short (~800 words)")
            self._blog_log("Applied Strategy Preset: Quick News Summary")

    def _open_blog_folder(self):
        if hasattr(self, 'blog_output_dir') and self.blog_output_dir and self.blog_output_dir.exists():
            os.startfile(self.blog_output_dir)
        else:
            messagebox.showwarning("Folder Not Found", "Blog output folder does not exist yet.")

    def _open_blog_report(self):
        if hasattr(self, 'blog_excel_path') and self.blog_excel_path and self.blog_excel_path.exists():
            os.startfile(self.blog_excel_path)
        else:
            messagebox.showwarning("File Not Found", "Blog Excel report file does not exist yet.")


if __name__ == "__main__":
    app = RewriterGUI()
    app.mainloop()
