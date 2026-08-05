"""
Live SERP & Competitor Outline Scraper with SerpAPI and DuckDuckGo Lite Fallbacks.
Caches snapshots in SQLite to eliminate duplicate API fees and scraping bans.
"""

import os
import json
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote, parse_qs, urlparse
from typing import Dict, List, Any, Optional
from concurrent.futures import ThreadPoolExecutor
from core.db import DatabaseManager


class SERPCrawler:
    """Queries live SERP ranking results, scrapes competitor headings, and caches snapshots."""

    def __init__(self, serpapi_key: Optional[str] = None, db_mgr: Optional[DatabaseManager] = None):
        self.serpapi_key = serpapi_key or os.getenv("SERPAPI_KEY")
        self.db = db_mgr or DatabaseManager()

    def fetch_serp_intel(self, primary_keyword: str) -> Dict[str, Any]:
        """Fetches organic search results, competitor headings, and PAA questions (cached in SQLite)."""
        clean_kw = primary_keyword.lower().strip()

        # 1. Check SQLite cache first (ONLY return if cache contains valid non-empty URLs)
        cached = self.db.get_serp_snapshot(clean_kw)
        if cached and cached.get("competitor_urls") and len(cached["competitor_urls"]) > 0:
            return cached

        intel = {
            "keyword": clean_kw,
            "competitor_urls": [],
            "paa_questions": [],
            "competitor_headings": [],
            "avg_word_count": 1800
        }

        # 2. Try SerpAPI first if key is provided
        if self.serpapi_key:
            try:
                res = requests.get(
                    "https://serpapi.com/search",
                    params={"engine": "google", "q": clean_kw, "api_key": self.serpapi_key, "num": 5},
                    timeout=10
                )
                if res.ok:
                    data = res.json()
                    organic = data.get("organic_results", [])
                    intel["competitor_urls"] = [r.get("link") for r in organic[:5] if r.get("link")]
                    intel["paa_questions"] = [q.get("question") for q in data.get("related_questions", []) if q.get("question")]
            except Exception:
                pass

        # 3. Fallback to DuckDuckGo Lite scraping if no SerpAPI key or SerpAPI returned 0 results
        if not intel["competitor_urls"]:
            try:
                res = requests.post(
                    "https://lite.duckduckgo.com/lite/",
                    data={"q": clean_kw},
                    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"},
                    timeout=10
                )
                if res.ok:
                    soup = BeautifulSoup(res.content, "html.parser")
                    urls = []
                    
                    # Parse organic links from DDG Lite HTML
                    for a in soup.find_all("a"):
                        href = a.get("href", "").strip()
                        target_url = None
                        if "uddg=" in href:
                            parsed = parse_qs(urlparse(href).query)
                            if "uddg" in parsed and parsed["uddg"]:
                                target_url = parsed["uddg"][0]
                        elif href.startswith("http"):
                            target_url = href

                        if target_url and not any(x in target_url.lower() for x in ["duckduckgo.com", "youtube.com", "facebook.com", "reddit.com", "twitter.com", "instagram.com", "amazon.com"]):
                            if target_url not in urls:
                                urls.append(target_url)

                        if len(urls) >= 5:
                            break
                    intel["competitor_urls"] = urls

                    # Parse DuckDuckGo related searches as PAA questions
                    rel_questions = []
                    for tr in soup.find_all("tr"):
                        text = tr.get_text(strip=True)
                        if "related" in text.lower() or "searches" in text.lower():
                            for a in tr.find_all("a"):
                                q_txt = a.get_text(strip=True)
                                if len(q_txt) > 5 and q_txt not in rel_questions:
                                    rel_questions.append(q_txt)
                    intel["paa_questions"] = rel_questions[:5]
            except Exception:
                pass

        # 4. Fallback PAA questions if empty
        if not intel["paa_questions"]:
            intel["paa_questions"] = [
                f"What is the best {clean_kw} for high quality treatment?",
                f"How to choose the top {clean_kw}?",
                f"What services and care do leading {clean_kw}s provide?",
                f"What are key factors when evaluating a {clean_kw}?"
            ]

        # 5. Concurrently scrape competitor headings & word counts
        if intel["competitor_urls"]:
            headings = []
            word_counts = []
            
            def _scrape_url(u):
                try:
                    r = requests.get(
                        u, 
                        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}, 
                        timeout=8
                    )
                    if r.ok:
                        s = BeautifulSoup(r.content, "html.parser")
                        # Remove script, style, nav, footer, header tags
                        for element in s(["script", "style", "nav", "footer", "header"]):
                            element.decompose()

                        body = s.find("main") or s.find("article") or s.find("body")
                        if body:
                            words = len(body.get_text(separator=" ", strip=True).split())
                            h_tags = []
                            for h in body.find_all(["h2", "h3"]):
                                txt = h.get_text(strip=True)
                                if len(txt) > 6 and len(txt) < 120 and not any(x in txt.lower() for x in ["cookie", "sign in", "subscribe", "privacy", "copyright", "nav", "share", "menu"]):
                                    h_tags.append(txt)
                            return max(words, 600), h_tags[:6]
                except Exception:
                    pass
                return 1500, []

            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = [executor.submit(_scrape_url, u) for u in intel["competitor_urls"]]
                for f in futures:
                    wc, h_list = f.result()
                    if wc > 0:
                        word_counts.append(wc)
                    headings.extend(h_list)

            if word_counts:
                intel["avg_word_count"] = int(sum(word_counts) / len(word_counts))
            intel["competitor_headings"] = list(dict.fromkeys(headings))[:15]

        # 6. Save in SQLite ONLY if we got actual competitor results
        if intel["competitor_urls"] and len(intel["competitor_urls"]) > 0:
            self.db.save_serp_snapshot(clean_kw, intel)

        return intel
