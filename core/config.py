"""
Configuration constants, pricing tables, and provider model mappings.
Accurate pricing, model definitions, and use-case recommendations.
"""

# Token Pricing per 1M tokens (Prompt, Completion) in USD
MODEL_PRICING_USD = {
    # OpenAI
    "gpt-4o-mini": {"prompt": 0.15, "completion": 0.60},
    "gpt-4o": {"prompt": 2.50, "completion": 10.00},
    "o1": {"prompt": 15.00, "completion": 60.00},
    "o1-mini": {"prompt": 1.10, "completion": 4.40},
    "o3-mini": {"prompt": 1.10, "completion": 4.40},
    "gpt-4-turbo": {"prompt": 10.00, "completion": 30.00},
    "gpt-3.5-turbo": {"prompt": 0.50, "completion": 1.50},

    # Google Gemini
    "gemini-2.0-flash": {"prompt": 0.10, "completion": 0.40},
    "gemini-2.5-flash": {"prompt": 0.10, "completion": 0.40},
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
    "qwen2.5": {"prompt": 0.0, "completion": 0.0},
    "deepseek-r1": {"prompt": 0.0, "completion": 0.0},
}

# Use-Case Recommendations & Performance Tiers
MODEL_USE_CASES = {
    # OpenAI
    "gpt-4o-mini": {"recommendation": "⚡ Fast & Cheap (Best for Bulk Rewriting & Outlines)", "tier": "Fast", "cost": "$0.15 in / $0.60 out per 1M"},
    "gpt-4o": {"recommendation": "🏆 High Ranking (Best for Premium Commercial SEO Articles)", "tier": "Premium", "cost": "$2.50 in / $10.00 out per 1M"},
    "o1": {"recommendation": "🔬 Deep Reasoning (Best for Complex Technical Research)", "tier": "Reasoning", "cost": "$15.00 in / $60.00 out per 1M"},
    "o1-mini": {"recommendation": "🔬 Fast Reasoning (Best for Technical Analysis)", "tier": "Reasoning", "cost": "$1.10 in / $4.40 out per 1M"},
    "o3-mini": {"recommendation": "🔬 High-Speed Reasoning (Best for Technical Articles)", "tier": "Reasoning", "cost": "$1.10 in / $4.40 out per 1M"},
    "gpt-4-turbo": {"recommendation": "🏆 Production Quality (Best for Long-Form Content)", "tier": "Premium", "cost": "$10.00 in / $30.00 out per 1M"},

    # Google Gemini
    "gemini-2.0-flash": {"recommendation": "⚡ Ultra Speed (Best for Instant Bulk Rewriting)", "tier": "Fast", "cost": "$0.10 in / $0.40 out per 1M"},
    "gemini-2.5-flash": {"recommendation": "⚡ Ultra Speed (Best for Instant Bulk Rewriting)", "tier": "Fast", "cost": "$0.10 in / $0.40 out per 1M"},
    "gemini-1.5-flash": {"recommendation": "⚡ High Speed (Best for Rapid Drafts)", "tier": "Fast", "cost": "$0.075 in / $0.30 out per 1M"},
    "gemini-1.5-pro": {"recommendation": "🏆 Long Context (Best for Massive Webpages & Audits)", "tier": "Premium", "cost": "$1.25 in / $5.00 out per 1M"},

    # Anthropic Claude
    "claude-3-5-sonnet-20241022": {"recommendation": "🏆 Human Tone (Best for Natural Human Writing)", "tier": "Premium", "cost": "$3.00 in / $15.00 out per 1M"},
    "claude-3-5-haiku-20241022": {"recommendation": "⚡ Fast & Natural (Best for Concise Articles)", "tier": "Fast", "cost": "$0.80 in / $4.00 out per 1M"},
    "claude-3-opus-20240229": {"recommendation": "🏆 Deep Creative (Best for Advanced Copywriting)", "tier": "Premium", "cost": "$15.00 in / $75.00 out per 1M"},

    # DeepSeek
    "deepseek-chat": {"recommendation": "🔬 DeepSeek V3 (Best High Quality at Ultra Low Cost)", "tier": "Value", "cost": "$0.14 in / $0.28 out per 1M"},
    "deepseek-reasoner": {"recommendation": "🔬 DeepSeek R1 (Best for Logic & Technical Schemas)", "tier": "Reasoning", "cost": "$0.55 in / $2.19 out per 1M"},

    # Groq
    "llama-3.3-70b-versatile": {"recommendation": "🚀 Groq Speed (Best for Ultra Low Latency Generation)", "tier": "Fast", "cost": "$0.59 in / $0.79 out per 1M"},
    "llama-3.1-8b-instant": {"recommendation": "⚡ Micro Speed (Best for Quick Tags & Outlines)", "tier": "Fast", "cost": "$0.05 in / $0.08 out per 1M"},
    "mixtral-8x7b-32768": {"recommendation": "🚀 Open Source (Best for Long Context)", "tier": "Value", "cost": "$0.24 in / $0.24 out per 1M"},

    # Local Ollama
    "llama3": {"recommendation": "🔒 Offline Privacy (Best for 100% Free Local Generation)", "tier": "Local", "cost": "Free ($0.00)"},
    "mistral": {"recommendation": "🔒 Offline Privacy (Best for Fast Local Drafts)", "tier": "Local", "cost": "Free ($0.00)"},
    "qwen2.5": {"recommendation": "🔒 Offline Privacy (Best for Multilingual Text)", "tier": "Local", "cost": "Free ($0.00)"},
    "deepseek-r1": {"recommendation": "🔒 Offline Privacy (Best for Local Reasoning)", "tier": "Local", "cost": "Free ($0.00)"},
}

# Predefined provider default model lists
PROVIDER_MODELS = {
    "OpenAI": ["gpt-4o-mini", "gpt-4o", "o1", "o3-mini", "gpt-4-turbo"],
    "Google Gemini": ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
    "Anthropic Claude": ["claude-3-5-sonnet-20241022", "claude-3-5-haiku-20241022", "claude-3-opus-20240229"],
    "DeepSeek": ["deepseek-chat", "deepseek-reasoner"],
    "Groq": ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
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


def get_model_info(model_name: str) -> dict:
    """Returns model recommendation, tier, and pricing string with smart fallbacks."""
    if model_name in MODEL_USE_CASES:
        return MODEL_USE_CASES[model_name]

    m_lower = model_name.lower()
    
    # Smart Fallback Matching for synced/custom models
    if "flash" in m_lower or "mini" in m_lower or "nano" in m_lower or "lite" in m_lower:
        rec = "⚡ High Speed & Low Cost (Best for Bulk Generation & Rapid Drafts)"
        tier = "Fast"
        cost_str = f"${MODEL_PRICING_USD[model_name]['prompt']:.2f} in / ${MODEL_PRICING_USD[model_name]['completion']:.2f} out per 1M" if model_name in MODEL_PRICING_USD else "Low Cost / High Speed Tier"
    elif "pro" in m_lower or "opus" in m_lower or "sonnet" in m_lower or "gpt-4" in m_lower or "gpt-5" in m_lower:
        rec = "🏆 Premium Quality (Best for High-Ranking Commercial Articles)"
        tier = "Premium"
        cost_str = f"${MODEL_PRICING_USD[model_name]['prompt']:.2f} in / ${MODEL_PRICING_USD[model_name]['completion']:.2f} out per 1M" if model_name in MODEL_PRICING_USD else "Standard Commercial API Rates"
    elif "reasoner" in m_lower or "r1" in m_lower or "o1" in m_lower or "o3" in m_lower or "o4" in m_lower:
        rec = "🔬 Deep Reasoning (Best for Technical Content & Logic)"
        tier = "Reasoning"
        cost_str = "Standard Reasoning Rates"
    elif "llama" in m_lower or "mistral" in m_lower or "qwen" in m_lower or "gemma" in m_lower:
        rec = "🔒 Open Source / Offline (Best for Privacy & Custom Deployments)"
        tier = "Local"
        cost_str = "Free / Local Host"
    else:
        rec = "⚡ Standard AI Model (Best for General Article Generation)"
        tier = "Standard"
        cost_str = "Standard API Pricing"

    return {
        "recommendation": rec,
        "tier": tier,
        "cost": cost_str
    }
