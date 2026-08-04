"""
Persistent SQLite Data Layer for PythonAiWriter.
Handles SERP caching, article persistence, token/cost accounting, and CMS credentials.
"""

import os
import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple


class DatabaseManager:
    """Manages SQLite database operations, schema migrations, caching, and audit logging."""

    def __init__(self, db_path: Optional[Path] = None):
        if db_path is None:
            db_path = Path(__file__).parent.parent / "pythonaiwriter.db"
        self.db_path = db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Initializes database schema tables if they do not exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 1. Projects / Workspaces
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                domain_url TEXT,
                sitemap_url TEXT,
                target_audience TEXT DEFAULT 'General Audience',
                default_tone TEXT DEFAULT 'Conversational & Engaging',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

            # 2. Articles & Drafts
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                topic TEXT NOT NULL,
                primary_keyword TEXT NOT NULL,
                status TEXT DEFAULT 'draft',
                content_html TEXT,
                content_md TEXT,
                word_count INTEGER DEFAULT 0,
                seo_score INTEGER DEFAULT 0,
                readability_score REAL DEFAULT 0.0,
                keyword_density REAL DEFAULT 0.0,
                cms_post_id TEXT,
                cms_post_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

            # 3. SERP Snapshots (Cached to avoid duplicate scraping / API costs)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS serp_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT UNIQUE NOT NULL,
                serp_data_json TEXT NOT NULL,
                fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

            # 4. Agent Audit Runs (Token & Cost Accounting)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_type TEXT NOT NULL,
                provider TEXT NOT NULL,
                model TEXT NOT NULL,
                prompt_tokens INTEGER DEFAULT 0,
                completion_tokens INTEGER DEFAULT 0,
                total_tokens INTEGER DEFAULT 0,
                cost_usd REAL DEFAULT 0.0,
                latency_sec REAL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

            # 5. CMS Credentials
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS cms_credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL UNIQUE,
                site_url TEXT NOT NULL,
                username TEXT,
                api_key TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

            conn.commit()

    # =========================================================================
    # SERP SNAPSHOT CACHING METHODS
    # =========================================================================

    def save_serp_snapshot(self, keyword: str, serp_data: Dict[str, Any]):
        """Caches SERP organic results and PAA questions for a keyword."""
        clean_kw = keyword.lower().strip()
        json_str = json.dumps(serp_data)
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO serp_snapshots (keyword, serp_data_json, fetched_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(keyword) DO UPDATE SET
                serp_data_json = excluded.serp_data_json,
                fetched_at = CURRENT_TIMESTAMP;
            """, (clean_kw, json_str))
            conn.commit()

    def get_serp_snapshot(self, keyword: str) -> Optional[Dict[str, Any]]:
        """Retrieves cached SERP data for a keyword if available."""
        clean_kw = keyword.lower().strip()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT serp_data_json FROM serp_snapshots WHERE keyword = ?", (clean_kw,))
            row = cursor.fetchone()
            if row:
                try:
                    return json.loads(row["serp_data_json"])
                except Exception:
                    return None
        return None

    # =========================================================================
    # TOKEN & COST ACCOUNTING LOGGING
    # =========================================================================

    def log_agent_run(
        self, 
        task_type: str, 
        provider: str, 
        model: str, 
        prompt_tokens: int, 
        completion_tokens: int, 
        cost_usd: float, 
        latency_sec: float
    ):
        """Logs granular token consumption, USD cost, and latency for debugging and cost tracking."""
        total_tokens = prompt_tokens + completion_tokens
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO agent_runs (task_type, provider, model, prompt_tokens, completion_tokens, total_tokens, cost_usd, latency_sec)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """, (task_type, provider, model, prompt_tokens, completion_tokens, total_tokens, cost_usd, latency_sec))
            conn.commit()

    def get_cost_summary(self) -> Dict[str, Any]:
        """Returns total aggregate token and cost usage across all agent runs."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT 
                COUNT(*) as total_runs,
                SUM(prompt_tokens) as prompt_tokens,
                SUM(completion_tokens) as completion_tokens,
                SUM(total_tokens) as total_tokens,
                SUM(cost_usd) as total_cost
            FROM agent_runs;
            """)
            row = cursor.fetchone()
            return {
                "total_runs": row["total_runs"] or 0,
                "prompt_tokens": row["prompt_tokens"] or 0,
                "completion_tokens": row["completion_tokens"] or 0,
                "total_tokens": row["total_tokens"] or 0,
                "total_cost_usd": round(row["total_cost"] or 0.0, 6)
            }

    # =========================================================================
    # CMS CREDENTIALS MANAGEMENT
    # =========================================================================

    def save_cms_credentials(self, platform: str, site_url: str, username: str, api_key: str):
        """Saves CMS platform credentials."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO cms_credentials (platform, site_url, username, api_key, created_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(platform) DO UPDATE SET
                site_url = excluded.site_url,
                username = excluded.username,
                api_key = excluded.api_key,
                created_at = CURRENT_TIMESTAMP;
            """, (platform.lower(), site_url, username, api_key))
            conn.commit()

    def get_cms_credentials(self, platform: str) -> Optional[Dict[str, str]]:
        """Retrieves credentials for a CMS platform (e.g. 'wordpress')."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT site_url, username, api_key FROM cms_credentials WHERE platform = ?", (platform.lower(),))
            row = cursor.fetchone()
            if row:
                return {
                    "site_url": row["site_url"],
                    "username": row["username"],
                    "api_key": row["api_key"]
                }
        return None
