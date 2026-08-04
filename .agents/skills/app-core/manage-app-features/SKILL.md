---
name: manage-app-features
description: Orchestrates, builds, and maintains new backend and UI features for PythonAiWriter including WordPress REST API publishing, XML sitemap mining, JSON-LD schema generation, and SERP competitive crawling while maintaining thread safety and backward compatibility.
---

# Feature Management & Architecture Skill (`manage-app-features`)

This skill defines the technical workflow and architectural rules for managing, building, and extending features in the **PythonAiWriter** desktop application.

## 🏗️ Architectural Guidelines

1. **Modular Separation**:
   - Backend Engine Logic $\rightarrow$ `core/` package (e.g. `core/wp_publisher.py`, `core/sitemap_miner.py`, `core/schema_generator.py`, `core/serp_crawler.py`).
   - UI Views & Cards $\rightarrow$ `ui/views/` package (e.g. `blog_view.py`, `settings_view.py`, `history_view.py`).
   - UI Reusable Widgets $\rightarrow$ `ui/components/` package (`sidebar.py`, `toolbar.py`, `preview_panel.py`, `statusbar.py`).

2. **Thread Safety Enforcement**:
   - ALL network requests, AI API queries, web scraping, and file exports MUST run inside background threads (`threading.Thread`).
   - ALL widget UI updates from background threads MUST use `.after(0, callback)` to avoid main loop crashes.

3. **Persistent State Management**:
   - Saved configurations (API keys, base URLs, preset models, default worker threads) MUST be persisted to `.env` or `app_config.json` via `ConfigManager`.

4. **Preserve Compatibility**:
   - Preserve `rewriter_engine.py` facade re-exporting `core/` package elements.
   - Do NOT run automated PyInstaller executable compilation (`build_exe.py`).

---

## 🛠️ Core Feature Management Workflows

### 🌐 1. WordPress REST API Publishing Integration
- Credentials stored securely in `.env` (`WP_URL`, `WP_USERNAME`, `WP_APP_PASSWORD`).
- Connection test endpoints hit `/wp-json/wp/v2/users/me`.
- Post creation posts JSON payload to `/wp-json/wp/v2/posts`.

### 🗺️ 2. XML Sitemap Mining Integration
- Downloads XML from target URL (`https://site.com/sitemap.xml`).
- Parses `<loc>` elements and automatically inserts anchor tags into generated articles.

### 🏷️ 3. JSON-LD Schema.org Generator Integration
- Constructs `@type: BlogPosting` and `@type: FAQPage` JSON-LD schemas.
- Injects `<script type="application/ld+json">` into HTML output, `.json` CMS exports, and WordPress payloads.

### 🔍 4. Live SERP & Competitor Mining Integration
- Queries search engine results for primary keywords.
- Mines competitor headings and PAA questions to enrich prompt outlines.
