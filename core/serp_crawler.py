"""
Live SERP & Competitor Outline Scraper with SerpAPI and DuckDuckGo Fallback.
Caches snapshots in SQLite to eliminate duplicate API fees and scraping bans.
"""

import os
import json
import requests
from bs4 import BeautifulSoup
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
        clean_kw = primary_keyword.strip()

        # Check SQLite cache first
        cached = self.db.get_serp_snapshot(clean_kw)
        if cached:
            return cached

        intel = {
            "keyword": clean_kw,
            "competitor_urls": [],
            "paa_questions": [],
            "competitor_headings": [],
            "avg_word_count": 1800
        }

        # 1. Try SerpAPI first if key is provided
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
                    intel["competitor_urls"] = [r.get("link") for r in organic[:3] if r.get("link")]
                    intel["paa_questions"] = [q.get("question") for q in data.get("related_questions", []) if q.get("question")]
            except Exception:
                pass

        # 2. Fallback to DuckDuckGo HTML scraping if no SerpAPI key or SerpAPI failed
        if not intel["competitor_urls"]:
            try:
                res = requests.get(
                    f"https://html.duckduckgo.com/html/?q={clean_kw}",
                    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"},
                    timeout=10
                )
                if res.ok:
                    soup = BeautifulSoup(res.content, "html.parser")
                    urls = []
                    for a in soup.find_all("a", class_="result__url"):
                        u = a.get("href", "").strip()
                        if u.startswith("http") and not any(x in u for x in ["youtube.com", "facebook.com", "reddit.com", "twitter.com"]):
                            urls.append(u)
                        if len(urls) >= 3:
                            break
                    intel["competitor_urls"] = urls
            except Exception:
                pass

        # 3. Concurrently scrape competitor headings from URLs
        if intel["competitor_urls"]:
            headings = []
            word_counts = []
            
            def _scrape_url(u):
                try:
                    r = requests.get(u, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"}, timeout=8)
                    if r.ok:
                        s = BeautifulSoup(r.content, "html.parser")
                        body = s.find("main") or s.find("article") or s.find("body")
                        if body:
                            words = len(body.get_text(separator=" ", strip=True).split())
                            h_tags = [h.get_text(strip=True) for h in body.find_all(["h2", "h3"]) if len(h.get_text(strip=True)) > 5]
                            return words, h_tags[:6]
                except Exception:
                    pass
                return 1500, []

            with ThreadPoolExecutor(max_workers=3) as executor:
                futures = [executor.submit(_scrape_url, u) for u in intel["competitor_urls"]]
                for f in futures:
                    wc, h_list = f.result()
                    word_counts.append(wc)
                    headings.extend(h_list)

            if word_counts:
                intel["avg_word_count"] = int(sum(word_counts) / len(word_counts))
            intel["competitor_headings"] = list(dict.fromkeys(headings))[:12]

        # Cache in SQLite
        self.db.save_serp_snapshot(clean_kw, intel)
        return intel
