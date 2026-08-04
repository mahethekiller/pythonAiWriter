"""
Core Backend Package for LLM Integration, Web Rewriting, and SEO Generation
"""

from .config import MODEL_PRICING_USD, PROVIDER_MODELS, ENV_KEY_MAP, DEFAULT_USER_AGENT
from .llm_client import MultiProviderLLMClient, calculate_cost_usd
from .exporters import DocxExporter, generate_slug
from .rewriter import WebScraper, LayoutPreservingRewriter, SemanticRewriter, run_batch_process
from .seo_generator import SEOArticleGenerator, calculate_flesch_reading_ease, count_syllables, run_blog_batch_process

__all__ = [
    "MODEL_PRICING_USD",
    "PROVIDER_MODELS",
    "ENV_KEY_MAP",
    "DEFAULT_USER_AGENT",
    "MultiProviderLLMClient",
    "calculate_cost_usd",
    "DocxExporter",
    "generate_slug",
    "WebScraper",
    "LayoutPreservingRewriter",
    "SemanticRewriter",
    "run_batch_process",
    "SEOArticleGenerator",
    "calculate_flesch_reading_ease",
    "count_syllables",
    "run_blog_batch_process"
]
