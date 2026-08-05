# PROJECT CONTEXT & ARCHITECTURE GUIDE
> **Project Name**: AI Content Rewriter & Master SEO Article Generator Studio  
> **Developer Credit**: Developed by `@mahethekiller`  
> **Technology Stack**: Python 3.10+, CustomTkinter (Native Dark/Light Mode Tuple Theme GUI), SQLite3 (`pythonaiwriter.db`), BeautifulSoup4, Pandas, Python-Docx, OpenAI/Anthropic/Google/DeepSeek/Groq/Ollama APIs  

---

## 📌 Executive Summary

This application is an enterprise-grade desktop software suite built for digital marketers, content creators, and SEO professionals:
1. **SEO Blog Creator**: Generates original, long-form, search-engine-optimized blog articles with XML sitemap link mining, AI image prompts, SERP heading extraction, AI humanization, Flesch readability scoring, JSON-LD Schema injection, and 1-click WordPress REST API publishing.
2. **Web Content Rewriter**: Scrapes target URLs and rewrites webpage content using AI—offering **Layout-Preserving HTML Mode** (retains exact DOM structure, CSS classes, and IDs) and **Semantic HTML Clean Mode**.
3. **Master Semrush Feature Suite**: Head-to-head domain Keyword Gap Analysis, AI Search Citation Tracker (ChatGPT, Gemini, Perplexity), Toxic Backlink Disavow Generator, and Semrush API v4 integration across dedicated navigation sidebar tabs.

---

## 🏗️ Codebase Architecture & Directory Map

The codebase follows a modular architecture separating core backend engine logic (`core/`) from CustomTkinter UI components (`ui/components/`) and dedicated views (`ui/views/`):

```
PythonAiWriter/
├── PROJECT_CONTEXT.md           # 📖 Master AI Context & Architecture Guide (This File)
├── gui_app.py                   # 🚀 Primary desktop GUI entry point with single-page unified views
├── rewriter_engine.py           # 🔄 Backward-compatibility facade module (re-exports core/)
├── app_config.json              # 💾 Local JSON persistence for presets, models & preferences
├── pythonaiwriter.db            # 🗄️ SQLite database (projects, articles, serp_snapshots, agent_runs, cms_credentials)
├── .env                         # 🔑 Saved API key storage (OPENAI_API_KEY, GEMINI_API_KEY, etc.)
├── run_gui.bat                  # ⚡ 1-Click Windows execution script
│
├── core/                        # 🧠 Core Backend & LLM Engine Package
│   ├── __init__.py             # Package API exports
│   ├── config.py               # Model pricing tables, smart pattern matching model recommendations, & provider defaults
│   ├── db.py                   # DatabaseManager for SQLite3 persistent storage
│   ├── router.py               # LLMRouter for intelligent fast/cheap vs premium model routing
│   ├── llm_client.py           # MultiProviderLLMClient (API calls, _call_llm facade, & dynamic model listing)
│   ├── humanizer.py            # AIHumanizer (anti-AI cliché filter & naturalization polish)
│   ├── readability.py          # ReadabilityAuditor (Flesch Reading Ease & keyword density meters)
│   ├── semrush_gap.py          # SemrushGapAnalyzer (domain vs competitor keyword/content gap)
│   ├── disavow_generator.py    # DisavowGenerator (toxic link audit & GSC disavow.txt exporter)
│   ├── ai_citation_tracker.py  # AICitationTracker (checks brand citations in AI model answers)
│   ├── semrush_client.py       # SemrushClient (Semrush API v4 live volume & KD% metrics)
│   ├── wp_publisher.py         # WordPressPublisher (1-click WP REST API direct post publisher)
│   ├── sitemap_miner.py        # SitemapMiner (XML sitemap URL fetcher & internal link weaver)
│   ├── schema_generator.py     # SchemaGenerator (BlogPosting & FAQPage JSON-LD schema builder)
│   ├── serp_crawler.py         # SERPCrawler (SerpAPI & DuckDuckGo competitor heading miner)
│   ├── screaming_frog_client.py# ScreamingFrogClient (CLI & REST API headless site auditor)
│   ├── rewriter.py             # WebScraper, LayoutPreservingRewriter, SemanticRewriter
│   ├── seo_generator.py        # SEOArticleGenerator, Flesch readability calculator, batch runner
│   └── exporters.py            # DocxExporter & URL slug generator
│
├── ui/                          # 🎨 CustomTkinter Graphical User Interface Package
│   ├── __init__.py             # UI Package exports
│   ├── config_manager.py       # ConfigManager for app_config.json deep-merge persistence
│   ├── theme_manager.py        # ThemeManager (Dark/Light mode tuple color management)
│   ├── components/             # Reusable UI Header, Footer & Sidebar Components
│   │   ├── sidebar.py          # Left Navigation Sidebar with 11 dedicated workspace items
│   │   ├── toolbar.py          # Top Toolbar with AI Provider & Presets selector
│   │   ├── statusbar.py        # Bottom Status Bar with live progress meter
│   │   └── preview_panel.py    # Right Live Preview Panel & WP 1-click publisher button
│   └── views/                  # Dedicated Single-Page View Containers
│       ├── blog_view.py        # ✍️ SEO Blog Creator View
│       ├── dashboard_view.py   # 🚀 Rewriter Studio View
│       ├── humanizer_view.py   # 🛡️ AI Humanizer Studio View
│       ├── serp_view.py        # 🔍 SERP Intelligence View
│       ├── gap_view.py         # 📊 Keyword & Content Gap View
│       ├── citation_view.py    # 🤖 AI Citation Tracker View
│       ├── audit_view.py       # 🐸 Technical SEO & Disavow Audit View
│       ├── publisher_view.py   # 🌐 CMS Publisher View (Active, File Picker & Custom modes)
│       ├── templates_view.py   # 📜 AI Templates & Strategy Presets View
│       ├── history_view.py     # 📚 History & File Exports Manager View
│       └── settings_view.py    # ⚙️ Settings & API Keys View
│
└── .agents/skills/              # 🤖 Specialized Agent Skills Catalog
    ├── app-core/               # Backend & Core Application Skills
    │   ├── manage-app-features/
    │   ├── research-new-features/
    │   ├── qa-feature-tester/
    │   ├── add-ai-provider/
    │   ├── build-standalone-executables/
    │   ├── debug-and-enhance-layout-preservation/
    │   ├── seo-optimization-and-analysis/
    │   └── update-llm-pricing-and-models/
    └── ui-ux/                  # UI & UX Modernization Skills
        ├── accessibility-review/
        ├── analyze-existing-ui/
        ├── animation-engine/
        ├── component-library/
        ├── desktop-theme-manager/
        ├── dialog-modernizer/
        ├── form-modernizer/
        ├── performance-review/
        ├── qa-ui/
        ├── screenshot-review/
        ├── sidebar-generator/
        ├── table-modernizer/
        ├── toolbar-generator/
        └── ui-modernization-master/
```

---

## 💻 Dedicated Sidebar Navigation & Workspaces

The left navigation sidebar ([ui/components/sidebar.py](file:///e:/xampp82/htdocs/PythonAiWriter/ui/components/sidebar.py)) provides 1-click access to 11 dedicated workspaces:

1. **✍️ SEO Blog Creator** (`blog`): Core article generator with Single Topic & Batch CSV modes.
2. **🚀 Rewriter Studio** (`rewriter`): Webpage scraper & DOM layout-preserving HTML rewriter.
3. **🛡️ AI Humanizer Studio** (`humanizer`): Flesch readability auditor & anti-AI cliché filter.
4. **🔍 SERP Intelligence** (`serp`): Keyword Magic Tool, search intent classifier, & PAA question miner.
5. **📊 Keyword & Content Gap** (`gap`): Head-to-head domain keyword gap matrix (You vs 4 Competitors).
6. **🤖 AI Citation Tracker** (`citation`): Test brand/domain citations in ChatGPT, Gemini, & Perplexity.
7. **🐸 Technical SEO & Disavow** (`audit`): Screaming Frog technical crawler & GSC `disavow.txt` exporter.
8. **🌐 CMS Publisher** (`publisher`): WordPress REST API connection tester, file picker (`.html`/`.json`), & publisher.
9. **📜 AI Templates** (`templates`): Strategy presets (Affiliate, Educational, News).
10. **📚 History & Exports** (`history`): Output file manager for `.html`, `.docx`, `.md`, & `.json` files.
11. **⚙️ Settings & API Keys** (`settings`): API keys, base URLs, WordPress credentials, Semrush API v4 key, and AI model presets.

---

## 🤖 Supported AI Providers & Model Defaults

| AI Provider | Default Predefined Models | API Key Env Var |
| :--- | :--- | :--- |
| **OpenAI** | `gpt-4o-mini`, `gpt-4o`, `o1`, `o1-mini` | `OPENAI_API_KEY` |
| **Google Gemini** | `gemini-2.0-flash`, `gemini-1.5-flash`, `gemini-1.5-pro` | `GEMINI_API_KEY` |
| **Anthropic Claude** | `claude-3-5-haiku-20241022`, `claude-3-5-sonnet-20241022` | `ANTHROPIC_API_KEY` |
| **DeepSeek** | `deepseek-chat`, `deepseek-reasoner` | `DEEPSEEK_API_KEY` |
| **Groq** | `llama-3.3-70b-versatile`, `llama-3.1-8b-instant`, `mixtral-8x7b-32768` | `GROQ_API_KEY` |
| **Ollama / Custom API**| `llama3`, `mistral`, `qwen2.5`, `deepseek-r1` | `OPENAI_API_KEY` (Base URL: `http://localhost:11434/v1`) |

---

## ⚠️ Important Developer & AI Agent Guidelines

1. **DO NOT Automatically Compile Executables**:
   - Never run compilation or generate zip archives automatically after making code edits. Executable compilation is resource-intensive and should ONLY be executed when explicitly requested by the user.

2. **Preserve Backward Compatibility**:
   - `gui_app.py` is the main desktop entry point.
   - `rewriter_engine.py` is a facade module re-exporting `core/` package elements. Do not remove `rewriter_engine.py`.

3. **Thread Safety & Error Handling**:
   - Always run network calls, AI generations, or API checks inside background threads (`threading.Thread`).
   - Always update CustomTkinter UI widgets from background threads using `.after(0, callback)`.
   - Store error messages (`err_msg = str(exc)`) before defining error callbacks to avoid Python free variable deletion scope issues.

4. **Custom Options Persistence**:
   - User configurations and presets MUST be saved to `app_config.json` via `ConfigManager` to persist permanently across app restarts.
