"""
XML Sitemap Link Miner for PythonAiWriter.
Crawls site sitemaps (/sitemap.xml) to automatically discover internal site links.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Optional


class SitemapMiner:
    """Crawls XML sitemaps to extract internal URLs for automated internal linking."""

    def __init__(self, user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"):
        self.user_agent = user_agent

    def fetch_internal_urls(self, sitemap_url: str, max_urls: int = 50) -> List[str]:
        """Downloads XML sitemap and extracts clean internal page URLs."""
        url = sitemap_url.strip()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url

        urls = []
        try:
            res = requests.get(url, headers={"User-Agent": self.user_agent}, timeout=12)
            if res.ok:
                soup = BeautifulSoup(res.content, "xml")
                loc_tags = soup.find_all("loc")
                for loc in loc_tags:
                    u = loc.get_text().strip()
                    if u and u.startswith("http") and not any(ext in u.lower() for ext in [".jpg", ".png", ".pdf", ".xml", "/category/", "/tag/", "/author/"]):
                        if u not in urls:
                            urls.append(u)
                    if len(urls) >= max_urls:
                        break
        except Exception:
            pass

        return urls
