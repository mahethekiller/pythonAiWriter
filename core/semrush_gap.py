"""
Keyword & Content Gap Analysis Engine (Semrush Gap Analytics).
Compares user domain/URL against up to 4 competitor URLs to discover missing keywords, missing headings, and content gaps.
"""

import re
import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, List


class SemrushGapAnalyzer:
    """Analyzes keyword and content gap between a target URL and competitor URLs."""

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def _scrape_page_terms(self, url: str) -> Dict[str, Any]:
        """Scrapes webpage to extract title, headings (H1-H3), and prominent keywords."""
        try:
            resp = requests.get(url, headers=self.headers, timeout=self.timeout)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')

            title = soup.title.string.strip() if soup.title and soup.title.string else url
            headings = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3']) if h.get_text(strip=True)]

            text_content = soup.get_text(separator=' ', strip=True).lower()
            words = re.findall(r'\b[a-zA-Z]{4,}\b', text_content)

            # Frequency count of terms length >= 4
            freq: Dict[str, int] = {}
            for w in words:
                freq[w] = freq.get(w, 0) + 1

            # Top 30 terms
            top_terms = set(sorted(freq.keys(), key=lambda k: freq[k], reverse=True)[:30])

            return {
                "url": url,
                "title": title,
                "headings": headings,
                "top_terms": top_terms,
                "word_count": len(words)
            }
        except Exception as exc:
            return {
                "url": url,
                "title": f"Error: {str(exc)}",
                "headings": [],
                "top_terms": set(),
                "word_count": 0
            }

    def analyze_gap(self, target_url: str, competitor_urls: List[str]) -> Dict[str, Any]:
        """
        Executes head-to-head keyword gap analysis comparing target URL against competitors.
        """
        target_data = self._scrape_page_terms(target_url)

        competitor_data_list = []
        all_comp_terms = set()
        all_comp_headings = []

        for comp_url in competitor_urls:
            if comp_url.strip():
                cd = self._scrape_page_terms(comp_url.strip())
                competitor_data_list.append(cd)
                all_comp_terms.update(cd["top_terms"])
                all_comp_headings.extend(cd["headings"])

        # Missing Keywords = Terms competitors use frequently that target URL does not use
        target_terms = target_data["top_terms"]
        missing_terms = list(all_comp_terms - target_terms)

        # Content Gap Headings = Headings competitors use that target site lacks
        target_headings_str = " ".join(target_data["headings"]).lower()
        missing_headings = [h for h in all_comp_headings if h.lower() not in target_headings_str][:15]

        avg_comp_word_count = int(sum(c["word_count"] for c in competitor_data_list) / max(1, len(competitor_data_list)))

        return {
            "target_url": target_url,
            "target_word_count": target_data["word_count"],
            "avg_competitor_word_count": avg_comp_word_count,
            "word_count_gap": max(0, avg_comp_word_count - target_data["word_count"]),
            "missing_keywords": missing_terms[:20],
            "missing_headings": missing_headings,
            "competitors_analyzed": len(competitor_data_list)
        }
