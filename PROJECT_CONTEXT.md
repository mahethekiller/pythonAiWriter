# PROJECT CONTEXT & ARCHITECTURE GUIDE
> **Project Name**: Multi-Provider Web Content Rewriter & SEO Article Generator  
> **Developer Credit**: Developed by `@mahethekiller`  
> **Technology Stack**: Python 3.10+, CustomTkinter (Dark Mode GUI), BeautifulSoup4, Pandas, Python-Docx, OpenAI/Anthropic/Google/DeepSeek/Groq/Ollama APIs  

---

## 📌 Executive Summary

This application is a dual-capability desktop software designed for digital marketers, content creators, and SEO professionals:
1. **Web Content Rewriter**: Scrapes target URLs and rewrites existing webpage content using AI—offering both **Layout-Preserving Mode** (retains exact DOM structure, CSS classes, and IDs) and **Semantic HTML Mode**.
2. **SEO Blog Creator**: Generates original, long-form, search-engine-optimized blog articles from scratch with internal/outbound link weaving, AI image prompts, keyword density auditing (~1.5% target), Flesch readability scoring, and multi-format exports (`.html`, `.docx`, `.md`, `.json`).

---

## 🏗️ Codebase Architecture & Directory Map

The codebase follows a modular architecture separating core backend engine logic (`core/`) from CustomTkinter UI views (`ui/`):

```
pythonmdfiles_gui/
├── PROJECT_CONTEXT.md           # 📖 Master AI Context Guide (This File)
├── gui_app.py                   # 🚀 Primary desktop GUI entry point (~350 lines)
├── rewriter_engine.py           # 🔄 Backward-compatibility facade module (re-exports core/)
├── app_config.json              # 💾 Local JSON persistence for models & custom settings
├── .env                         # 🔑 Saved API key storage (OPENAI_API_KEY, GEMINI_API_KEY, etc.)
│
├── core/                        # 🧠 Core Backend & LLM Engine Package
│   ├── __init__.py             # Package API exports
│   ├── config.py               # Model pricing tables, provider defaults, & constants
│   ├── llm_client.py           # MultiProviderLLMClient (API calls & live model query)
│   ├── rewriter.py             # WebScraper, LayoutPreservingRewriter, SemanticRewriter
│   ├── seo_generator.py        # SEOArticleGenerator, Flesch readability calculator, batch runner
│   └── exporters.py            # DocxExporter & URL slug generator
│
├── ui/                          # 🎨 CustomTkinter Graphical User Interface Views
│   ├── __init__.py             # UI Package exports
│   ├── config_manager.py       # ConfigManager for app_config.json handling
│   ├── dashboard_tab.py        # Tab 1: Rewriter Dashboard layout & controls
│   ├── blog_tab.py             # Tab 2: SEO Blog Creator layout & controls
│   └── settings_tab.py         # Tab 3: Configuration & Settings layout & controls
│
└── .agents/skills/              # 🤖 Specialized AI Agent Skills
    ├── add-ai-provider/
    ├── build-standalone-executables/
    ├── debug-and-enhance-layout-preservation/
    ├── seo-optimization-and-analysis/
    ├── ui-ux-enhancement-and-design/
    └── update-llm-pricing-and-models/
```

---

## 💻 Tab Layout & Key Features

The application tab bar is organized in the following order:

### 1. 🚀 Rewriter Dashboard (`Tab 1`)
* **Scraping & Rewriting**: Scrapes web content from input URLs and rewrites text nodes.
* **Modes**:
  * `Layout-Preserving HTML`: Extracts text nodes while preserving exact CSS classes, IDs, DOM structure, and styling.
  * `Semantic HTML Clean rewrite`: Extracts body content into clean semantic HTML (`<h1>`, `<h2>`, `<p>`, `<ul>`).
* **Cost & Token Tracking**: Logs prompt/completion tokens and calculates USD cost based on model pricing tables.
* **Export Formats**: Outputs files into timestamped `output_results/Run_YYYY-MM-DD_HH-MM-SS/` folders in WordPress HTML and Word `.docx` formats.

### 2. ✍️ SEO Blog Creator (`Tab 2`)
* **Execution Modes**:
  * `Single Article Mode`: Single topic title and custom focus keyword inputs.
  * `Batch CSV Cluster Mode`: Uploads `.csv` / `.txt` files to process multi-topic article clusters in background worker threads.
  * `📥 Sample CSV Download`: Generates `sample_batch_topics.csv` template file with 1-click.
* **1-Click Strategy Presets**:
  * 🛍️ *Affiliate Product Review* (Commercial Intent, Persuasive Tone, Comparison Format)
  * 🎓 *Educational Deep-Dive* (Informational Intent, Authoritative Tone, Ultimate Guide Format)
  * ⚡ *Quick News Summary* (Informational Intent, Short ~800 words)
* **Linking & Media Enhancements**:
  * Contextually weaves internal sitemap URLs (`<a href="...">`).
  * Auto-inserts outbound authority reference links.
  * Auto-places Midjourney / DALL-E AI Image Callout Prompts with keyword-rich `alt="..."` text.
  * Adds TL;DR summary boxes and Schema-ready FAQ sections.
* **Hero Metric Analytics**:
  * Live stat cards for **Total Word Count**, **Keyword Density %** (~1.5% target with green/amber badges), **Flesch Readability Ease grade**, and **Meta Title/Description length badges**.
* **Multi-Format Exports**: Exports into `blog_articles/` (`.html`), `docx_articles/` (`.docx`), `md_articles/` (`.md`), and `json_cms_payloads/` (`.json`).

### 3. ⚙️ Configuration & Settings (`Tab 3`)
* **AI Provider Selector**: Switch between OpenAI, Google Gemini, Anthropic Claude, DeepSeek, Groq, and Ollama.
* **API Key Management**: Saves keys securely into `.env` file.
* **Base URL Override**: Allows custom endpoints for local Ollama (`http://localhost:11434/v1`) or proxies.
* **🔄 Sync Models Button**: Queries provider API endpoints in background thread to refresh available live models.
* **Worker Threads**: Select 1 to 10 concurrent threads for parallel URL/article generation.
* **Developer Credit Footer**: Features `⚡ Application Developed by @mahethekiller`.

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
   - PyInstaller build scripts exist in `build_exe.py` (Windows) and `build_mac_app.py` (macOS).
   - **Rule**: Never run compilation or generate zip archives automatically after making feature edits. Executable compilation takes significant CPU time and should ONLY be executed when explicitly requested by the user.

2. **Preserve Backward Compatibility**:
   - `gui_app.py` is the main desktop entry point.
   - `rewriter_engine.py` is a facade module re-exporting `core/` package elements. Do not remove `rewriter_engine.py` as build scripts depend on it.

3. **Thread Safety**:
   - Always run network calls or AI generations inside background threads (`threading.Thread`).
   - Always update CustomTkinter UI widgets from background threads using `.after(0, callback)`.

4. **Custom Options Persistence**:
   - User-typed custom dropdown choices (models, tones, formats, audiences) MUST be saved to `app_config.json` via `ConfigManager` to persist across app restarts.
