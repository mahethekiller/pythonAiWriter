"""
Configuration manager for app_config.json persistence.
Preserves all top-level configuration keys including AI Presets, Custom Models, Base URLs, and Theme settings across application restarts.
"""

import json
from pathlib import Path
from typing import Dict, Any
from core.config import PROVIDER_MODELS


class ConfigManager:
    """Manages loading, updating, and saving local user preferences in app_config.json."""

    def __init__(self, config_file: Path):
        self.config_file = config_file
        self.data: Dict[str, Any] = {}
        self.load()

    def load(self):
        """Loads configuration from JSON file and preserves all custom user keys."""
        self.data = {
            "last_provider": "OpenAI",
            "theme": "Dark",
            "last_models": {
                "OpenAI": "gpt-4o-mini",
                "Google Gemini": "gemini-2.0-flash",
                "Anthropic Claude": "claude-3-5-haiku-20241022",
                "DeepSeek": "deepseek-chat",
                "Groq": "llama-3.3-70b-versatile",
                "Ollama / Custom API": "llama3"
            },
            "custom_models": {
                "OpenAI": [],
                "Google Gemini": [],
                "Anthropic Claude": [],
                "DeepSeek": [],
                "Groq": [],
                "Ollama / Custom API": []
            },
            "ai_presets": {
                "Fast & Cheap (GPT-4o Mini)": {
                    "provider": "OpenAI",
                    "model": "gpt-4o-mini",
                    "workers": "3"
                },
                "High Quality (GPT-4o)": {
                    "provider": "OpenAI",
                    "model": "gpt-4o",
                    "workers": "3"
                },
                "Ultra Speed (Gemini Flash)": {
                    "provider": "Google Gemini",
                    "model": "gemini-2.0-flash",
                    "workers": "3"
                },
                "Deep Reasoning (DeepSeek Chat)": {
                    "provider": "DeepSeek",
                    "model": "deepseek-chat",
                    "workers": "3"
                }
            },
            "provider_base_urls": {},
            "blog_config": {
                "tones": ["Conversational & Engaging", "Professional & Authoritative", "Technical & Detailed", "Persuasive", "Friendly & Educational"],
                "formats": ["Ultimate Guide", "Listicle / Top N List", "How-To Step-by-Step", "Product Comparison", "Informational Explainer"],
                "audiences": ["General Audience", "College Students", "Software Developers", "Business Executives", "Beginners"],
                "intents": ["Informational", "Commercial", "Transactional", "Navigational"],
                "last_tone": "Conversational & Engaging",
                "last_format": "Ultimate Guide",
                "last_audience": "General Audience",
                "last_intent": "Informational",
                "last_word_count": "Standard (~1,500 words)"
            }
        }

        if self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    if isinstance(loaded, dict):
                        # Deep merge loaded keys so user presets, theme, and custom models persist
                        for key, val in loaded.items():
                            if key == "last_models" and isinstance(val, dict):
                                self.data["last_models"].update(val)
                            elif key == "custom_models" and isinstance(val, dict):
                                for provider, models_list in val.items():
                                    if provider not in self.data["custom_models"]:
                                        self.data["custom_models"][provider] = []
                                    for m in models_list:
                                        if m not in self.data["custom_models"][provider]:
                                            self.data["custom_models"][provider].append(m)
                            elif key == "ai_presets" and isinstance(val, dict):
                                for p_name, p_cfg in val.items():
                                    self.data["ai_presets"][p_name] = p_cfg
                            elif key == "blog_config" and isinstance(val, dict):
                                for k, b_val in val.items():
                                    if isinstance(b_val, list):
                                        if k not in self.data["blog_config"]:
                                            self.data["blog_config"][k] = []
                                        for item in b_val:
                                            if item not in self.data["blog_config"][k]:
                                                self.data["blog_config"][k].append(item)
                                    else:
                                        self.data["blog_config"][k] = b_val
                            else:
                                self.data[key] = val
            except Exception:
                pass

        # Merge custom persisted models into runtime PROVIDER_MODELS
        for provider, custom_list in self.data.get("custom_models", {}).items():
            if provider in PROVIDER_MODELS:
                for model in custom_list:
                    if model not in PROVIDER_MODELS[provider]:
                        PROVIDER_MODELS[provider].append(model)

    def save(self):
        """Saves current configuration to app_config.json."""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2)
        except Exception:
            pass
