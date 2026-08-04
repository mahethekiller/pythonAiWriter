"""
AI Content Humanizer & Anti-Detection Polish Engine.
Filters robotic AI vocabulary clichés and naturalizes tone to improve human readability.
"""

import re
from typing import Tuple, Optional


AI_CLICHE_PATTERNS = [
    r'\bdelve\b', r'\bdelving\b', r'\btapestry\b', r'\btestament\b', r'\bunwavering\b',
    r'\bpivotal\b', r'\bbeacon\b', r'\bfostering\b', r'\bseamlessly\b', r'\bgame-changer\b',
    r'\bcrucial\b', r'\bparamount\b', r'\brealm\b', r'\bunderscores\b', r'\bmultifaceted\b',
    r'\bholistic\b', r'\bsynergy\b', r'\bplethora\b', r'\bmyriad\b', r'\bveritable\b'
]


class AIHumanizer:
    """Naturalizes AI generated text by removing robotic transitions and cliché phrases."""

    def __init__(self, router=None):
        self.router = router

    def contains_ai_cliches(self, text: str) -> bool:
        """Returns True if text contains common AI vocabulary clichés."""
        lower_txt = text.lower()
        return any(re.search(pat, lower_txt) for pat in AI_CLICHE_PATTERNS)

    def humanize_text(self, content_html: str) -> str:
        """Scans content_html and performs a multi-pass naturalization polish."""
        if not content_html:
            return content_html

        clean_html = content_html

        # Step 1: Strip explicit cliché filler phrases using regex rules
        clean_html = re.sub(r'\bin the realm of\b', 'in', clean_html, flags=re.IGNORECASE)
        clean_html = re.sub(r'\bit is important to note that\b', '', clean_html, flags=re.IGNORECASE)
        clean_html = re.sub(r'\bit is worth mentioning that\b', '', clean_html, flags=re.IGNORECASE)
        clean_html = re.sub(r'\bstands as a testament to\b', 'shows', clean_html, flags=re.IGNORECASE)
        clean_html = re.sub(r'\bserves as a beacon of\b', 'represents', clean_html, flags=re.IGNORECASE)

        # Step 2: If router is available, perform LLM naturalization polish pass
        if self.router:
            system_prompt = (
                "You are an expert human editor. Polish the provided HTML body content to sound 100% natural, human, and engaging.\n"
                "RULES:\n"
                "1. Strip repetitive AI vocabulary like 'delve', 'tapestry', 'testament', 'pivotal', 'seamlessly'.\n"
                "2. Vary sentence length for natural rhythm.\n"
                "3. Preserve ALL original HTML structure, <h1>, <h2>, <h3>, <p>, <a>, <ul>, and <li> tags strictly.\n"
                "4. Output ONLY valid body HTML without markdown code blocks."
            )
            user_prompt = f"Polish this HTML content:\n\n{clean_html}"
            try:
                polished, _, _, _ = self.router.call_task("humanizer", system_prompt, user_prompt)
                if polished and "<p>" in polished:
                    clean_html = re.sub(r"^```(html)?\s*", "", polished, flags=re.IGNORECASE)
                    clean_html = re.sub(r"\s*```$", "", clean_html).strip()
            except Exception:
                pass

        return clean_html
