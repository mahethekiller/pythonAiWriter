"""
Configuration manager for app_config.json persistence.
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
        self.data = {
            "last_provider": "OpenAI",
            "last_models": {
                "OpenAI": "gpt-4o-mini",
                "Google Gemini": "gemini-1.5-flash",
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
                    if "last_provider" in loaded:
                        self.data["last_provider"] = loaded["last_provider"]
                    if "last_models" in loaded:
                        self.data["last_models"].update(loaded["last_models"])
                    if "custom_models" in loaded:
                        for provider, models_list in loaded["custom_models"].items():
                            if provider not in self.data["custom_models"]:
                                self.data["custom_models"][provider] = []
                            for m in models_list:
                                if m not in self.data["custom_models"][provider]:
                                    self.data["custom_models"][provider].append(m)
                    if "blog_config" in loaded:
                        b_loaded = loaded["blog_config"]
                        for k in ["last_tone", "last_format", "last_audience", "last_intent", "last_word_count"]:
                            if k in b_loaded:
                                self.data["blog_config"][k] = b_loaded[k]
                        for k in ["tones", "formats", "audiences", "intents"]:
                            if k in b_loaded:
                                for item in b_loaded[k]:
                                    if item not in self.data["blog_config"][k]:
                                        self.data["blog_config"][k].append(item)
            except Exception:
                pass

        # Merge custom persisted models into runtime PROVIDER_MODELS
        for provider, custom_list in self.data.get("custom_models", {}).items():
            if provider in PROVIDER_MODELS:
                for model in custom_list:
                    if model not in PROVIDER_MODELS[provider]:
                        PROVIDER_MODELS[provider].append(model)

    def save(self):
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2)
        except Exception:
            pass
