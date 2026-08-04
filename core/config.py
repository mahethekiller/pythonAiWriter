"""
Configuration constants, pricing tables, and provider model mappings.
"""

# Token Pricing per 1M tokens (Prompt, Completion) in USD
MODEL_PRICING_USD = {
    # OpenAI
    "gpt-4o": {"prompt": 2.50, "completion": 10.00},
    "gpt-4o-mini": {"prompt": 0.15, "completion": 0.60},
    "o1": {"prompt": 15.00, "completion": 60.00},
    "o1-mini": {"prompt": 1.10, "completion": 4.40},

    # Google Gemini
    "gemini-2.0-flash": {"prompt": 0.10, "completion": 0.40},
    "gemini-1.5-flash": {"prompt": 0.075, "completion": 0.30},
    "gemini-1.5-pro": {"prompt": 1.25, "completion": 5.00},

    # Anthropic Claude
    "claude-3-5-sonnet-20241022": {"prompt": 3.00, "completion": 15.00},
    "claude-3-5-haiku-20241022": {"prompt": 0.80, "completion": 4.00},
    "claude-3-opus-20240229": {"prompt": 15.00, "completion": 75.00},

    # DeepSeek
    "deepseek-chat": {"prompt": 0.14, "completion": 0.28},
    "deepseek-reasoner": {"prompt": 0.55, "completion": 2.19},

    # Groq (Hosted Open Source Models)
    "llama-3.3-70b-versatile": {"prompt": 0.59, "completion": 0.79},
    "llama-3.1-8b-instant": {"prompt": 0.05, "completion": 0.08},
    "mixtral-8x7b-32768": {"prompt": 0.24, "completion": 0.24},
    "gemma2-9b-it": {"prompt": 0.20, "completion": 0.20},

    # Local Ollama / Custom API (Default zero cost)
    "llama3": {"prompt": 0.0, "completion": 0.0},
    "mistral": {"prompt": 0.0, "completion": 0.0},
}

# Predefined provider default model lists
PROVIDER_MODELS = {
    "OpenAI": ["gpt-4o-mini", "gpt-4o", "o1", "o1-mini"],
    "Google Gemini": ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
    "Anthropic Claude": ["claude-3-5-haiku-20241022", "claude-3-5-sonnet-20241022", "claude-3-opus-20240229"],
    "DeepSeek": ["deepseek-chat", "deepseek-reasoner"],
    "Groq": ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768", "gemma2-9b-it"],
    "Ollama / Custom API": ["llama3", "mistral", "qwen2.5", "deepseek-r1"]
}

# Environment variable keys
ENV_KEY_MAP = {
    "OpenAI": "OPENAI_API_KEY",
    "Google Gemini": "GEMINI_API_KEY",
    "Anthropic Claude": "ANTHROPIC_API_KEY",
    "DeepSeek": "DEEPSEEK_API_KEY",
    "Groq": "GROQ_API_KEY",
    "Ollama / Custom API": "OPENAI_API_KEY"
}

DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
