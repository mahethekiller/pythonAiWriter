# Python AI Content Rewriter & SEO Article Studio

> **Developed by**: [@mahethekiller](https://github.com/mahethekiller)  
> A desktop software built with **Python 3** and **CustomTkinter** for web content rewriting, SEO article generation, multi-provider AI model syncing, and document exports.

---

## 🌟 Key Features

### 🚀 1. Web Content Rewriter Studio
* **Layout-Preserving HTML Mode**: Scrapes web content and rewrites text nodes while preserving exact CSS classes, element IDs, DOM hierarchy, and page formatting.
* **Semantic HTML Clean Rewrite**: Extracts body content (headings, paragraphs, lists) and rewrites it into clean, semantic HTML.
* **Token & Cost Tracking**: Live estimation and logging of prompt/completion tokens and estimated USD costs.
* **Batch URL Processing**: Rewrite multiple web pages in parallel using multi-threaded execution.

### ✍️ 2. SEO Blog Creator & Article Engine
* **Original Article Generation**: Draft long-form, search-optimized articles from scratch.
* **Single & Batch CSV Modes**: Generate individual topics or process multi-topic content clusters using a CSV file.
* **1-Click Strategy Presets**:
  * 🛍️ *Affiliate Product Review* (Commercial Intent, Persuasive Tone)
  * 🎓 *Educational Deep-Dive* (Informational Intent, Authoritative Tone)
  * ⚡ *Quick News Summary* (Short ~800 words format)
* **SEO Keyword & Link Strategy**:
  * Auto-weaves internal site links (`<a href="...">`).
  * Inserts outbound authority reference links.
  * Generates Midjourney / DALL-E AI image prompts with keyword-rich `alt="..."` text.
  * Adds TL;DR summary boxes and Schema-ready FAQ sections.
* **Hero Analytics Stat Cards**: Post-generation analytics for **Total Words**, **Keyword Density %** (~1.5% target with green/amber badges), **Flesch Readability Score**, and **Meta Tag Pass/Fail Badges**.
* **Multi-Format Exports**: Outputs to WordPress HTML (`.html`), Word (`.docx`), Markdown (`.md`), and Headless CMS JSON (`.json`).

### ⚙️ 3. Multi-Provider AI Engine & Custom Settings
* **Supported AI Providers**: OpenAI, Google Gemini, Anthropic Claude, DeepSeek, Groq, and Ollama (Local LLMs).
* **🔄 Live Model Syncing**: Queries provider API endpoints to fetch live available models in background threads.
* **Custom Base URL Overrides**: Support for local Ollama instances (`http://localhost:11434/v1`) or custom proxies.
* **Persistent Preferences**: Custom-typed models, tones, formats, and audiences automatically save to `app_config.json`.

---

## 🎨 Cyber-Dark Glassmorphism Interface

Built with CustomTkinter featuring:
* Deep Obsidian Slate background (`#0b0f19`).
* Translucent Glass-Style Cards (`#161e2e` with `#2a364f` borders and `corner_radius=10`).
* High-visibility Status Pill Badges (`[ 🟢 AI Ready ]`, `[ ⚡ 3 Threads Active ]`).
* Interactive Info Popup Buttons (`ℹ️`) for technical settings explanations.
* 3-Step Process Progress Trackers.

---

## 📁 Repository Structure

```
pythonAiWriter/
├── PROJECT_CONTEXT.md           # 📖 Master AI Context Guide
├── README.md                    # 📖 Project Documentation & Setup Guide
├── gui_app.py                   # 🚀 Desktop Application Main Entry Point
├── rewriter_engine.py           # 🔄 Backward-compatibility facade module
├── requirements.txt             # 📦 Python Dependencies
├── .env.example                 # 🔑 Environment Variables Template
├── .gitignore                   # 🚫 Git Exclusions (Protects API Keys)
│
├── core/                        # 🧠 Core Backend Package
│   ├── config.py               # Pricing tables & provider model defaults
│   ├── llm_client.py           # MultiProviderLLMClient API integration
│   ├── rewriter.py             # Scraper & URL rewriter logic
│   ├── seo_generator.py        # SEOArticleGenerator & Flesch readability engine
│   └── exporters.py            # DocxExporter & URL slug generators
│
└── ui/                          # 🎨 CustomTkinter UI Tab Modules
    ├── config_manager.py       # JSON app_config persistence
    ├── dashboard_tab.py        # Tab 1: Rewriter Dashboard UI
    ├── blog_tab.py             # Tab 2: SEO Blog Creator UI
    └── settings_tab.py         # Tab 3: Configuration & Settings UI
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/mahethekiller/pythonAiWriter.git
cd pythonAiWriter
```

### 2. Create Virtual Environment & Install Dependencies
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure API Keys
Copy `.env.example` to `.env` and fill in your API keys:
```bash
cp .env.example .env
```
*(Note: You can also enter and save your API keys directly inside the **⚙️ Configuration & Settings** tab within the GUI application!)*

---

## 🚀 Running the Application

Launch the desktop application:
```bash
python gui_app.py
```

---

## 🔒 Security & Privacy

* **Zero API Key Exposure**: `.env` and `app_config.json` are excluded via `.gitignore` to ensure private credentials and keys are never pushed to version control.

---

## 👤 Developer & Credits

Developed with ❤️ by **[@mahethekiller](https://github.com/mahethekiller)**.
