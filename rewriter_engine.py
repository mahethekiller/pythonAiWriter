"""
Backward-compatibility facade module for rewriter_engine.
Re-exports all backend classes and functions from the core/ package.
"""

from core import (
    MODEL_PRICING_USD,
    PROVIDER_MODELS,
    ENV_KEY_MAP,
    DEFAULT_USER_AGENT,
    MultiProviderLLMClient,
    calculate_cost_usd,
    DocxExporter,
    generate_slug,
    WebScraper,
    LayoutPreservingRewriter,
    SemanticRewriter,
    run_batch_process,
    SEOArticleGenerator,
    calculate_flesch_reading_ease,
    count_syllables,
    run_blog_batch_process
)

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
