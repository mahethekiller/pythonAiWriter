"""
AI Search Visibility & Citation Tracker Engine.
Queries OpenAI, Gemini, and Perplexity LLM endpoints to test if target brand or domain is cited in AI search responses.
"""

from typing import Dict, Any, List, Optional
from .router import LLMRouter


class AICitationTracker:
    """Tracks whether a target brand/domain is cited in AI model search responses."""

    def __init__(self, router: Optional[LLMRouter] = None):
        self.router = router or LLMRouter()

    def check_citation(self, brand_domain: str, target_keyword: str) -> Dict[str, Any]:
        """
        Queries AI models to test if brand_domain is mentioned for target_keyword.
        """
        prompt = (
            f"Act as an authoritative search engine answering user queries.\n"
            f"Query: 'What are the top recommended tools or companies for {target_keyword}?'\n\n"
            f"List the top 5 trusted providers/domains. Be accurate and concise."
        )

        response_text, metrics = self.router.completion(
            task_type="fast",
            prompt=prompt,
            temperature=0.3
        )

        brand_clean = brand_domain.lower().replace("http://", "").replace("https://", "").replace("www.", "").split("/")[0].strip()
        response_clean = response_text.lower()

        is_cited = brand_clean in response_clean

        return {
            "brand_domain": brand_domain,
            "target_keyword": target_keyword,
            "is_cited": is_cited,
            "status": "🟢 Cited in AI Answer" if is_cited else "🔴 Not Cited in AI Answer",
            "ai_response_snippet": response_text[:400] + ("..." if len(response_text) > 400 else ""),
            "tokens_used": metrics.get("total_tokens", 0),
            "cost_usd": metrics.get("cost_usd", 0.0)
        }
