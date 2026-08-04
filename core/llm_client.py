"""
Multi-provider LLM client integration and costing logic.
"""

import os
from typing import Tuple, List, Optional
from core.config import MODEL_PRICING_USD, PROVIDER_MODELS

# Optional Third-Party LLM SDK Imports
try:
    import openai
except ImportError:
    openai = None

try:
    import anthropic
except ImportError:
    anthropic = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None


def calculate_cost_usd(model_name: str, prompt_tokens: int, completion_tokens: int) -> float:
    """Calculates estimated USD cost for API usage based on pricing tables."""
    pricing = MODEL_PRICING_USD.get(model_name, {"prompt": 0.0, "completion": 0.0})
    cost_prompt = (prompt_tokens / 1_000_000.0) * pricing["prompt"]
    cost_comp = (completion_tokens / 1_000_000.0) * pricing["completion"]
    return cost_prompt + cost_comp


class MultiProviderLLMClient:
    """Unified API client supporting OpenAI, Anthropic, Gemini, DeepSeek, Groq, and Ollama."""

    def __init__(
        self,
        provider: str,
        api_key: str,
        model: str,
        base_url: Optional[str] = None
    ):
        self.provider = provider
        self.api_key = api_key
        self.model = model
        self.base_url = base_url

    def _call_llm(self, system_prompt: str, user_prompt: str) -> Tuple[str, int, int, int]:
        """Dispatches request to appropriate provider API and returns (content, prompt_tokens, completion_tokens, total_tokens)."""
        
        if self.provider in ["OpenAI", "DeepSeek", "Groq", "Ollama / Custom API"]:
            if not openai:
                raise ImportError("`openai` Python package is required. Install with `pip install openai`.")
            
            client_kwargs = {"timeout": 60.0}
            if self.api_key:
                client_kwargs["api_key"] = self.api_key
            else:
                client_kwargs["api_key"] = "dummy_key"

            if self.provider == "DeepSeek":
                client_kwargs["base_url"] = self.base_url or "https://api.deepseek.com"
            elif self.provider == "Groq":
                client_kwargs["base_url"] = self.base_url or "https://api.groq.com/openai/v1"
            elif self.provider == "Ollama / Custom API":
                client_kwargs["base_url"] = self.base_url or "http://localhost:11434/v1"
            elif self.base_url:
                client_kwargs["base_url"] = self.base_url

            client = openai.OpenAI(**client_kwargs)
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7
            )

            content = response.choices[0].message.content or ""
            usage = response.usage
            prompt_tokens = usage.prompt_tokens if usage else 0
            completion_tokens = usage.completion_tokens if usage else 0
            total_tokens = usage.total_tokens if usage else 0
            return content, prompt_tokens, completion_tokens, total_tokens

        elif self.provider == "Anthropic Claude":
            if not anthropic:
                raise ImportError("`anthropic` Python package is required. Install with `pip install anthropic`.")
            
            client = anthropic.Anthropic(api_key=self.api_key, timeout=60.0)
            response = client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            
            content = response.content[0].text if response.content else ""
            prompt_tokens = response.usage.input_tokens
            completion_tokens = response.usage.output_tokens
            total_tokens = prompt_tokens + completion_tokens
            return content, prompt_tokens, completion_tokens, total_tokens

        elif self.provider == "Google Gemini":
            if not genai:
                raise ImportError("`google-generativeai` package is required. Install with `pip install google-generativeai`.")
            
            genai.configure(api_key=self.api_key)
            model_instance = genai.GenerativeModel(
                model_name=self.model,
                system_instruction=system_prompt
            )
            response = model_instance.generate_content(user_prompt)
            content = response.text or ""
            
            usage = getattr(response, "usage_metadata", None)
            if usage:
                prompt_tokens = getattr(usage, "prompt_token_count", 0)
                completion_tokens = getattr(usage, "candidates_token_count", 0)
                total_tokens = getattr(usage, "total_token_count", prompt_tokens + completion_tokens)
            else:
                prompt_tokens, completion_tokens, total_tokens = 0, 0, 0
                
            return content, prompt_tokens, completion_tokens, total_tokens

        else:
            raise ValueError(f"Unsupported provider: '{self.provider}'")

    def list_models(self) -> List[str]:
        """Queries provider API endpoints for available live models."""
        models = []
        if self.provider in ["OpenAI", "DeepSeek", "Groq", "Ollama / Custom API"]:
            if not openai:
                raise ImportError("`openai` Python package is required. Install with `pip install openai`.")
            client_kwargs = {"timeout": 12.0}
            if self.api_key:
                client_kwargs["api_key"] = self.api_key
            else:
                client_kwargs["api_key"] = "dummy_key"

            if self.provider == "DeepSeek":
                client_kwargs["base_url"] = self.base_url or "https://api.deepseek.com"
            elif self.provider == "Groq":
                client_kwargs["base_url"] = self.base_url or "https://api.groq.com/openai/v1"
            elif self.provider == "Ollama / Custom API":
                client_kwargs["base_url"] = self.base_url or "http://localhost:11434/v1"
            elif self.base_url:
                client_kwargs["base_url"] = self.base_url

            client = openai.OpenAI(**client_kwargs)
            res = client.models.list()
            models = [m.id for m in res.data]

        elif self.provider == "Google Gemini":
            if not genai:
                raise ImportError("`google-generativeai` package is required. Install with `pip install google-generativeai`.")
            if not self.api_key:
                raise ValueError("Gemini API Key is required to list models.")
            genai.configure(api_key=self.api_key)
            for m in genai.list_models():
                if hasattr(m, "supported_generation_methods") and "generateContent" in m.supported_generation_methods:
                    clean_id = m.name.replace("models/", "")
                    models.append(clean_id)

        elif self.provider == "Anthropic Claude":
            if not anthropic:
                raise ImportError("`anthropic` Python package is required. Install with `pip install anthropic`.")
            if not self.api_key:
                raise ValueError("Anthropic API Key is required to list models.")
            client = anthropic.Anthropic(api_key=self.api_key, timeout=12.0)
            if hasattr(client, "models"):
                res = client.models.list()
                models = [m.id for m in res.data]
            else:
                models = PROVIDER_MODELS.get("Anthropic Claude", [])

        return models
