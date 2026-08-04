#!/usr/bin/env python3
"""
Desktop GUI Application for Web Content Rewriting & Document Generation
========================================================================
Built with CustomTkinter. Features a modular architecture, responsive scrollable
tabs, multi-provider AI support, live model syncing, and an SEO Blog Creator.
"""

import os
import sys
import json
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
    ENV_KEY_MAP
)
from ui import (
    ConfigManager, 
    build_dashboard_tab, 
    build_settings_tab, 
    build_blog_tab
)

# Set theme and appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class RewriterGUI(ctk.CTk):
    """Main Application Window for Web Rewriter and SEO Blog Creator."""

    def __init__(self):
        super().__init__()

        self.title("AI Content Rewriter & SEO Article Generator")
        self.geometry("960, 780")
        self.minsize(800, 600)

        # Load environment variables
        self.env_file = Path(__file__).parent / ".env"
        if not self.env_file.exists():
            self.env_file.touch()
        load_dotenv(self.env_file)

        # Config Manager initialization
        self.config_file = Path(__file__).parent / "app_config.json"
        self.config_mgr = ConfigManager(self.config_file)
        self.config_data = self.config_mgr.data

        # Runtime State
        self.output_dir = None
        self.excel_path = None
        self.cost_report_path = None
        self.blog_output_dir = None
        self.blog_excel_path = None
        self.is_processing = False

        self._build_ui()

    def _save_config(self):
        """Saves active configuration via config manager."""
        self.config_mgr.save()

    def _build_ui(self):
        """Constructs top header bar and tabview layout."""
        
        # Header Title
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=15, pady=(15, 5))

        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="Multi-Provider Web Content Rewriter & SEO Studio", 
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.title_label.pack(side="left")

        # Developer Credit Badge
        self.dev_credit_label = ctk.CTkLabel(
            self.header_frame,
            text="⚡ Developed by @mahethekiller",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#38bdf8"
        )
        self.dev_credit_label.pack(side="right", padx=(0, 5))

        # Tabview
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=5)

        self.tabview.add("🚀 Rewriter Dashboard")
        self.tabview.add("✍️ SEO Blog Creator")
        self.tabview.add("⚙️ Configuration & Settings")

        # Scrollable Frame Containers
        self.dashboard_container = ctk.CTkScrollableFrame(self.tabview.tab("🚀 Rewriter Dashboard"), fg_color="transparent")
        self.dashboard_container.pack(fill="both", expand=True, padx=2, pady=2)

        self.blog_container = ctk.CTkScrollableFrame(self.tabview.tab("✍️ SEO Blog Creator"), fg_color="transparent")
        self.blog_container.pack(fill="both", expand=True, padx=2, pady=2)

        self.settings_container = ctk.CTkScrollableFrame(self.tabview.tab("⚙️ Configuration & Settings"), fg_color="transparent")
        self.settings_container.pack(fill="both", expand=True, padx=2, pady=2)

        # Build individual UI tabs from UI package
        build_dashboard_tab(self, self.dashboard_container)
        build_blog_tab(self, self.blog_container)
        build_settings_tab(self, self.settings_container)

        # Initial provider update
        last_provider = self.config_data.get("last_provider", "OpenAI")
        self.provider_combo.set(last_provider)
        self._on_provider_change(last_provider)

    def show_info_popup(self, title: str, description: str):
        """Displays an interactive help popup dialog for UI features."""
        win = ctk.CTkToplevel(self)
        win.title(title)
        win.geometry("480x280")
        win.transient(self)
        win.grab_set()

        frame = ctk.CTkFrame(win, fg_color="#161e2e", corner_radius=10, border_width=1, border_color="#2a364f")
        frame.pack(fill="both", expand=True, padx=12, pady=12)

        ctk.CTkLabel(frame, text=f"ℹ️ {title}", font=ctk.CTkFont(size=16, weight="bold"), text_color="#38bdf8").pack(anchor="w", padx=14, pady=(12, 6))
        
        textbox = ctk.CTkTextbox(frame, fg_color="transparent", font=ctk.CTkFont(size=12), wrap="word")
        textbox.insert("1.0", description)
        textbox.configure(state="disabled")
        textbox.pack(fill="both", expand=True, padx=12, pady=6)

        ctk.CTkButton(frame, text="Got It!", command=win.destroy, width=100, fg_color="#10b981", hover_color="#059669").pack(pady=(0, 10))

    # =========================================================================
    # SETTINGS TAB EVENT HANDLERS
    # =========================================================================

    def _on_provider_change(self, provider: str):
        models = PROVIDER_MODELS.get(provider, ["custom"])
        self.model_combo.configure(values=models)
        
        last_model = self.config_data.get("last_models", {}).get(provider)
        if last_model and last_model in models:
            self.model_combo.set(last_model)
        else:
            self.model_combo.set(models[0] if models else "")

        env_var = ENV_KEY_MAP.get(provider, "OPENAI_API_KEY")
        existing_key = os.getenv(env_var, "")
        self.api_key_entry.delete(0, "end")
        if existing_key:
            self.api_key_entry.insert(0, existing_key)

        if provider == "Ollama / Custom API":
            base_url_val = os.getenv("OPENAI_BASE_URL", "http://localhost:11434/v1")
            self.base_url_entry.delete(0, "end")
            self.base_url_entry.insert(0, base_url_val)

        self._update_config_status_label()

    def _save_api_key(self):
        provider = self.provider_combo.get()
        key_val = self.api_key_entry.get().strip()
        env_var = ENV_KEY_MAP.get(provider, "OPENAI_API_KEY")

        if not key_val:
            messagebox.showwarning("Warning", "API Key entry is empty!")
            return

        set_key(self.env_file, env_var, key_val)
        os.environ[env_var] = key_val

        base_url_val = self.base_url_entry.get().strip()
        if base_url_val:
            set_key(self.env_file, "OPENAI_BASE_URL", base_url_val)
            os.environ["OPENAI_BASE_URL"] = base_url_val

        messagebox.showinfo("Success", f"Saved API Key for {provider} to .env file!")

    def _sync_models(self):
        provider = self.provider_combo.get()
        api_key = self.api_key_entry.get().strip()
        base_url = self.base_url_entry.get().strip() or None

        if "Ollama" not in provider and not api_key:
            messagebox.showwarning("API Key Required", f"Please enter your {provider} API Key before syncing models.")
            return

        self.sync_models_btn.configure(state="disabled", text="⏳ Syncing...")
        self._log(f"Querying live models from {provider} API...")

        threading.Thread(
            target=self._sync_models_worker,
            args=(provider, api_key, base_url),
            daemon=True
        ).start()

    def _sync_models_worker(self, provider: str, api_key: str, base_url: Optional[str]):
        try:
            client = MultiProviderLLMClient(provider=provider, api_key=api_key, model="", base_url=base_url)
            fetched_models = client.list_models()

            if not fetched_models:
                raise ValueError("No models returned from API.")

            def _success():
                if provider not in PROVIDER_MODELS:
                    PROVIDER_MODELS[provider] = []
                for m in fetched_models:
                    if m not in PROVIDER_MODELS[provider]:
                        PROVIDER_MODELS[provider].append(m)

                if provider not in self.config_data["custom_models"]:
                    self.config_data["custom_models"][provider] = []
                for m in fetched_models:
                    if m not in self.config_data["custom_models"][provider]:
                        self.config_data["custom_models"][provider].append(m)

                self.model_combo.configure(values=PROVIDER_MODELS[provider])
                if fetched_models:
                    self.model_combo.set(fetched_models[0])
                    self.config_data["last_models"][provider] = fetched_models[0]
                    self._save_config()
                
                self._update_config_status_label()

                self.sync_models_btn.configure(state="normal", text="🔄 Sync Models")
                self._log(f"✓ Success: Synced {len(fetched_models)} models for {provider}.")
                messagebox.showinfo("Sync Success", f"Successfully synced {len(fetched_models)} models for {provider}!")

            self.after(0, _success)

        except Exception as exc:
            def _error():
                self.sync_models_btn.configure(state="normal", text="🔄 Sync Models")
                self._log(f"✗ Sync failed for {provider}: {exc}")
                messagebox.showerror("Sync Error", f"Failed to sync models for {provider}:\n{str(exc)}")

            self.after(0, _error)

    def _update_config_status_label(self):
        provider = self.provider_combo.get()
        model = self.model_combo.get().strip()
        threads = self.workers_combo.get()
        mode_str = self.mode_combo.get()
        mode = "Layout-Preserving" if "Layout" in mode_str else "Semantic HTML"
        
        status_text = f"Active Config: [{provider}] {model}  |  Mode: {mode}  |  Threads: {threads}"
        self.config_status_label.configure(text=status_text)

        blog_status_text = f"Active AI Provider: [{provider}] {model}  |  Threads: {threads}"
        if hasattr(self, 'blog_config_status_label'):
            self.blog_config_status_label.configure(text=blog_status_text)

    def _browse_save_folder(self):
        folder = filedialog.askdirectory(title="Select Output Save Directory")
        if folder:
            self.save_folder_entry.delete(0, "end")
            self.save_folder_entry.insert(0, folder)

    # =========================================================================
    # REWRITER DASHBOARD TAB EVENT HANDLERS
    # =========================================================================

    def _toggle_custom_prompt(self):
        if self.custom_prompt_var.get():
            self.custom_prompt_textbox.configure(state="normal")
        else:
            self.custom_prompt_textbox.configure(state="disabled")

    def _log(self, message: str):
        def _update():
            self.log_textbox.insert("end", f"{message}\n")
            self.log_textbox.see("end")
        self.after(0, _update)

    def _start_processing(self):
        if self.is_processing:
            return

        urls_raw = self.urls_textbox.get("1.0", "end").strip()
        urls = [u.strip() for u in urls_raw.splitlines() if u.strip()]

        if not urls:
            messagebox.showwarning("Warning", "Please enter at least one URL to process.")
            return

        provider = self.provider_combo.get()
        api_key = self.api_key_entry.get().strip()
        base_url = self.base_url_entry.get().strip() or None

        if "Ollama" not in provider and not api_key:
            messagebox.showwarning("API Key Required", f"Please enter your {provider} API Key in Settings.")
            return

        model = self.model_combo.get().strip()
        if not model:
            messagebox.showwarning("Model Required", "Please select or type a model ID.")
            return

        # Save provider & model preference
        self.config_data["last_provider"] = provider
        if "last_models" not in self.config_data:
            self.config_data["last_models"] = {}
        self.config_data["last_models"][provider] = model

        if provider not in self.config_data.get("custom_models", {}):
            self.config_data.setdefault("custom_models", {})[provider] = []
        if model not in self.config_data["custom_models"][provider]:
            self.config_data["custom_models"][provider].append(model)
            if provider in PROVIDER_MODELS and model not in PROVIDER_MODELS[provider]:
                PROVIDER_MODELS[provider].append(model)
                self.model_combo.configure(values=PROVIDER_MODELS[provider])

        self._save_config()

        mode = self.mode_combo.get()
        gen_html = self.html_var.get()
        gen_docx = self.docx_var.get()

        if not gen_html and not gen_docx:
            messagebox.showwarning("Warning", "Please select at least one output format (HTML or Word).")
            return

        main_save_folder = self.save_folder_entry.get().strip()
        if not main_save_folder:
            messagebox.showwarning("Warning", "Please select a valid Main Save Folder in Settings.")
            return

        max_workers = int(self.workers_combo.get())
        custom_inst = self.custom_prompt_textbox.get("1.0", "end").strip() if self.custom_prompt_var.get() else None

        self.is_processing = True
        self.start_btn.configure(state="disabled", text="⏳ Rewriting Content...")
        self.open_folder_btn.configure(state="disabled")
        self.open_excel_btn.configure(state="disabled")
        self.open_cost_btn.configure(state="disabled")
        self.progress_bar.set(0)
        self.log_textbox.delete("1.0", "end")

        threading.Thread(
            target=self._processing_worker_thread,
            args=(urls, provider, api_key, model, mode, gen_html, gen_docx, Path(main_save_folder), max_workers, custom_inst, base_url),
            daemon=True
        ).start()

    def _processing_worker_thread(self, urls, provider, api_key, model, mode, gen_html, gen_docx, main_save_folder, max_workers, custom_inst, base_url):
        def _progress_cb(completed, total, current_msg):
            frac = completed / total
            def _update():
                self.progress_bar.set(frac)
                self.status_lbl.configure(text=f"Processed {completed}/{total} URLs")
            self.after(0, _update)

        try:
            df, excel_path, run_output_dir, metrics = run_batch_process(
                urls=urls,
                provider=provider,
                api_key=api_key,
                model=model,
                mode=mode,
                generate_html=gen_html,
                generate_docx=gen_docx,
                main_save_folder=main_save_folder,
                max_workers=max_workers,
                custom_instruction=custom_inst,
                base_url=base_url,
                progress_cb=_progress_cb,
                log_cb=self._log
            )

            self.output_dir = run_output_dir
            self.excel_path = excel_path
            self.cost_report_path = run_output_dir / "batch_cost_summary.txt"

            def _on_complete():
                self.is_processing = False
                self.start_btn.configure(state="normal", text="🚀 Start Batch Rewriting")
                self.status_lbl.configure(text=f"Completed! Total Tokens: {metrics['total_tokens']:,} | Cost: ${metrics['total_cost_usd']:.6f} USD")
                self.open_folder_btn.configure(state="normal")
                if self.excel_path and self.excel_path.exists():
                    self.open_excel_btn.configure(state="normal")
                if self.cost_report_path and self.cost_report_path.exists():
                    self.open_cost_btn.configure(state="normal")

                summary_msg = (
                    f"Processed {len(urls)} URLs ({metrics['successful']} Success, {metrics['failed']} Failed)\n\n"
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
                self.status_lbl.configure(text="Error during processing!")
                messagebox.showerror("Execution Error", str(exc))

            self.after(0, _on_error)

    def _open_output_folder(self):
        if self.output_dir and self.output_dir.exists():
            os.startfile(self.output_dir)
        else:
            messagebox.showwarning("Folder Not Found", "Output folder does not exist yet.")

    def _open_excel_file(self):
        if self.excel_path and self.excel_path.exists():
            os.startfile(self.excel_path)
        else:
            messagebox.showwarning("File Not Found", "Excel status file does not exist yet.")

    def _open_cost_file(self):
        if self.cost_report_path and self.cost_report_path.exists():
            os.startfile(self.cost_report_path)
        else:
            messagebox.showwarning("File Not Found", "Cost summary report file does not exist yet.")

    # =========================================================================
    # SEO BLOG CREATOR TAB EVENT HANDLERS
    # =========================================================================

    def _toggle_blog_mode(self):
        mode = self.blog_mode_var.get()
        if mode == "single":
            self.blog_topic_label.grid_configure(row=1, column=0)
            self.blog_topic_entry.grid_configure(row=1, column=1)
            self.blog_csv_label.grid_forget()
            self.blog_csv_entry.grid_forget()
            self.blog_csv_browse_btn.grid_forget()
            self.blog_csv_sample_btn.grid_forget()
        else:
            self.blog_topic_label.grid_forget()
            self.blog_topic_entry.grid_forget()
            self.blog_csv_label.grid_configure(row=1, column=0, padx=8, pady=6, sticky="w")
            self.blog_csv_entry.grid_configure(row=1, column=1, padx=8, pady=6, sticky="w")
            self.blog_csv_browse_btn.grid_configure(row=1, column=2, padx=4, pady=6, sticky="w")
            self.blog_csv_sample_btn.grid_configure(row=1, column=3, padx=4, pady=6, sticky="w")

    def _browse_blog_csv(self):
        filename = filedialog.askopenfilename(
            title="Select Batch Topics CSV/Text File",
            filetypes=[("CSV / Text Files", "*.csv *.txt"), ("All Files", "*.*")]
        )
        if filename:
            self.blog_csv_entry.delete(0, "end")
            self.blog_csv_entry.insert(0, filename)
            self._blog_log(f"Selected Batch CSV File: {filename}")

    def _download_sample_csv(self):
        filepath = filedialog.asksaveasfilename(
            title="Save Sample Batch Topics CSV",
            initialfile="sample_batch_topics.csv",
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if filepath:
            sample_content = (
                "topic,primary_keyword\n"
                "10 Best Budget Laptops for College Students in 2026,budget student laptops\n"
                "Complete Guide to Python Desktop App Development,python desktop app development\n"
                "Top AI Content Rewriter Tools for SEO Professionals,ai content rewriter tools\n"
                "How to Optimize Web Content for Featured Snippets,web content seo optimization\n"
            )
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(sample_content)
                self._blog_log(f"Saved Sample Batch CSV Template to: {filepath}")
                messagebox.showinfo("Sample Saved", f"Successfully saved Sample Batch CSV Template to:\n{filepath}")
            except Exception as exc:
                messagebox.showerror("Save Error", f"Failed to save sample CSV: {exc}")

    def _blog_log(self, message: str):
        def _update():
            self.blog_log_textbox.insert("end", f"{message}\n")
            self.blog_log_textbox.see("end")
        self.after(0, _update)

    def _start_blog_generation(self):
        if self.is_processing:
            return

        provider = self.provider_combo.get()
        api_key = self.api_key_entry.get().strip()
        base_url = self.base_url_entry.get().strip() or None

        if "Ollama" not in provider and not api_key:
            messagebox.showwarning("API Key Required", f"Please enter your {provider} API Key in Settings.")
            return

        main_save_folder = self.save_folder_entry.get().strip()
        if not main_save_folder:
            messagebox.showwarning("Save Folder Required", "Please enter a Main Save Folder in Settings.")
            return

        mode = self.blog_mode_var.get()
        topics_data = []

        if mode == "single":
            topic = self.blog_topic_entry.get().strip()
            if not topic:
                messagebox.showwarning("Topic Required", "Please enter an Article Topic / Title.")
                return
            
            pk = self.blog_pk_entry.get().strip() or topic
            sk_raw = self.blog_sk_textbox.get("1.0", "end").strip()
            sec_keywords = [k.strip() for k in sk_raw.split(",") if k.strip()]
            
            int_links_raw = self.blog_internal_links_textbox.get("1.0", "end").strip().splitlines()
            internal_links = [l.strip() for l in int_links_raw if l.strip()]

            comp_urls_raw = self.blog_comp_urls_textbox.get("1.0", "end").strip().splitlines()
            comp_urls = [u.strip() for u in comp_urls_raw if u.strip()]

            topics_data.append({
                "topic": topic,
                "primary_keyword": pk,
                "secondary_keywords": sec_keywords,
                "search_intent": self.blog_intent_combo.get().strip(),
                "tone": self.blog_tone_combo.get().strip(),
                "format_type": self.blog_format_combo.get().strip(),
                "target_audience": self.blog_audience_combo.get().strip(),
                "word_count_target": self.blog_wordcount_combo.get().strip(),
                "internal_links": internal_links,
                "include_external_links": self.blog_ext_links_var.get(),
                "include_image_prompts": self.blog_img_prompts_var.get(),
                "custom_outline": self.blog_outline_textbox.get("1.0", "end").strip(),
                "include_tldr": self.blog_tldr_var.get(),
                "include_faq": self.blog_faq_var.get(),
                "cta_text": self.blog_cta_entry.get().strip(),
                "competitor_urls": comp_urls
            })
        else:
            csv_path = self.blog_csv_entry.get().strip()
            if not csv_path or not Path(csv_path).exists():
                messagebox.showwarning("CSV File Required", "Please select a valid Batch Topics CSV file.")
                return
            try:
                if csv_path.endswith(".csv"):
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
                                "include_faq": True
                            })
                else:
                    with open(csv_path, "r", encoding="utf-8") as f:
                        lines = f.read().splitlines()
                    for line in lines:
                        t = line.strip()
                        if t and not t.startswith("#"):
                            topics_data.append({
                                "topic": t,
                                "primary_keyword": t,
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
                                "include_faq": True
                            })
            except Exception as exc:
                messagebox.showerror("CSV Read Error", str(exc))
                return

        if not topics_data:
            messagebox.showwarning("No Topics Found", "No valid topics were found to process.")
            return

        b_cfg = self.config_data["blog_config"]
        tone_val = self.blog_tone_combo.get().strip()
        format_val = self.blog_format_combo.get().strip()
        audience_val = self.blog_audience_combo.get().strip()
        intent_val = self.blog_intent_combo.get().strip()
        wordcount_val = self.blog_wordcount_combo.get().strip()

        if tone_val and tone_val not in b_cfg["tones"]:
            b_cfg["tones"].append(tone_val)
        if format_val and format_val not in b_cfg["formats"]:
            b_cfg["formats"].append(format_val)
        if audience_val and audience_val not in b_cfg["audiences"]:
            b_cfg["audiences"].append(audience_val)
        if intent_val and intent_val not in b_cfg["intents"]:
            b_cfg["intents"].append(intent_val)

        b_cfg["last_tone"] = tone_val
        b_cfg["last_format"] = format_val
        b_cfg["last_audience"] = audience_val
        b_cfg["last_intent"] = intent_val
        b_cfg["last_word_count"] = wordcount_val
        self._save_config()

        gen_html = self.blog_html_var.get()
        gen_docx = self.blog_docx_var.get()
        gen_md = self.blog_md_var.get()
        gen_json = self.blog_json_var.get()

        if not any([gen_html, gen_docx, gen_md, gen_json]):
            messagebox.showwarning("No Export Selected", "Please select at least one SEO Export Format.")
            return

        model = self.model_combo.get().strip()
        max_workers = int(self.workers_combo.get())

        self.is_processing = True
        self.blog_start_btn.configure(state="disabled", text="⏳ Generating SEO Article(s)...")
        self.blog_open_folder_btn.configure(state="disabled")
        self.blog_open_report_btn.configure(state="disabled")
        self.blog_progress_bar.set(0)
        self.blog_log_textbox.delete("1.0", "end")

        threading.Thread(
            target=self._blog_worker_thread,
            args=(topics_data, provider, api_key, model, gen_html, gen_docx, gen_md, gen_json, Path(main_save_folder), max_workers, base_url),
            daemon=True
        ).start()

    def _blog_worker_thread(self, topics_data, provider, api_key, model, gen_html, gen_docx, gen_md, gen_json, main_save_folder, max_workers, base_url):
        def _progress_cb(completed, total, current_msg):
            frac = completed / total
            def _update():
                self.blog_progress_bar.set(frac)
                self.blog_status_lbl.configure(text=f"Generated {completed}/{total} Articles")
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

            def _on_complete():
                self.is_processing = False
                self.blog_start_btn.configure(state="normal", text="🚀 Generate SEO Blog Article(s)")
                self.blog_status_lbl.configure(text=f"Completed! Total Tokens: {metrics['total_tokens']:,} | Cost: ${metrics['total_cost_usd']:.6f} USD")
                self.blog_open_folder_btn.configure(state="normal")
                if self.blog_excel_path and self.blog_excel_path.exists():
                    self.blog_open_report_btn.configure(state="normal")

                if metrics.get("last_article_metrics"):
                    self._update_blog_seo_card(metrics["last_article_metrics"])

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
                self.blog_status_lbl.configure(text="Error during blog generation!")
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

    def _update_blog_seo_card(self, m: Dict[str, Any]):
        title_badge = "✅ PASS (<=60 chars)" if m.get("meta_title_pass") else "⚠️ LONG (>60 chars)"
        desc_badge = "✅ PASS (<=160 chars)" if m.get("meta_desc_pass") else "⚠️ LONG (>160 chars)"

        # Populate Hero Stat Cards
        self.stat_val_words.configure(text=f"{m.get('word_count', 0):,}")
        
        density = m.get('pk_density', 0)
        density_color = "#4ade80" if 1.0 <= density <= 2.5 else "#facc15"
        self.stat_val_density.configure(text=f"{density}%", text_color=density_color)
        
        readability_str = m.get('readability_label', 'N/A')
        self.stat_val_readability.configure(text=readability_str.split()[0] if readability_str != 'N/A' else '--')

        card_text = (
            f"Topic: '{m.get('topic', '')}'\n"
            f"• Meta Title ({len(m.get('meta_title', ''))} chars): {title_badge}\n"
            f"• Meta Description ({len(m.get('meta_description', ''))} chars): {desc_badge}\n"
            f"• Structure: {m.get('h2_count', 0)} H2s  |  {m.get('h3_count', 0)} H3s  |  {m.get('img_prompt_count', 0)} AI Image Prompts"
        )
        self.blog_seo_metrics_lbl.configure(text=card_text, text_color="#f8fafc")

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
