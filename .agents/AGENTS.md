# Agent Project Rules & Context Reference

> **Developer Credit**: Developed by `@mahethekiller`  
> **Master Project Context**: See [PROJECT_CONTEXT.md](file:///d:/softwares/xampp82new/htdocs/pythonmdfiles_gui/PROJECT_CONTEXT.md) for complete architecture details, API key env maps, and tab feature specs.

## Critical Rules for AI Agents

1. **Read `PROJECT_CONTEXT.md` First**:
   - Before making structural changes, inspect [PROJECT_CONTEXT.md](file:///d:/softwares/xampp82new/htdocs/pythonmdfiles_gui/PROJECT_CONTEXT.md) for the modular package architecture (`core/` for backend engine, `ui/` for CustomTkinter views).

2. **No Automatic Executable Compilation**:
   - DO NOT run `build_exe.py` or `build_mac_app.py` after editing code. Compilation is resource-intensive and should only be triggered when explicitly requested by the user.

3. **Preserve `rewriter_engine.py` Facade**:
   - `rewriter_engine.py` acts as a backward-compatibility facade re-exporting `core/` package elements. Do not break or delete `rewriter_engine.py`.

4. **UI Thread Safety**:
   - All network/LLM calls must run in background threads (`threading.Thread`) and update CustomTkinter widgets via `.after(0, callback)`.

---

## 🧰 Skill Catalog Index (`.agents/skills/`)

### 🧠 Backend & Application Core (`skills/app-core/`)
* **`manage-app-features`**: Orchestrate, build, and maintain new features (WordPress REST API publishing, XML Sitemap Link Miner, JSON-LD Schema.org Generator, SERP Crawler).
* **`research-new-features`**: Perform market analysis, competitive auditing (SurferSEO, Clearscope, Jasper, Cursor IDE), and synthesize feature roadmaps.
* **`qa-feature-tester`**: Automated headless and GUI functional testing, Python execution checks, and API payload validation.
* **`add-ai-provider`**: Add new LLM API integrations (OpenAI, Anthropic, Gemini, Groq, DeepSeek, etc.).
* **`build-standalone-executables`**: Compile Windows `.exe` and macOS `.app` bundles via PyInstaller.
* **`debug-and-enhance-layout-preservation`**: Inspect & refine layout-preserving HTML rewriting & CSS parsers.
* **`seo-optimization-and-analysis`**: SEO metadata generation, Flesch readability, and keyword density rules.
* **`update-llm-pricing-and-models`**: Update model lists, cost calculators, and API endpoint configs.

### 🎨 UI & UX Modernization Suite (`skills/ui-ux/`)
* **`accessibility-review`**: Contrast, font sizes, screen-reader friendliness.
* **`analyze-existing-ui`**: Audit visual layouts, color palettes, and component hierarchy.
* **`animation-engine`**: Dynamic micro-interactions and smooth UI state transitions.
* **`component-library`**: Modular, reusable CustomTkinter UI widgets.
* **`desktop-theme-manager`**: Dark glassmorphism color schemes and theme tokens.
* **`dialog-modernizer`**: Modern dialogs, alerts, and modal popups.
* **`form-modernizer`**: Form controls, inputs, drop-downs, and error badges.
* **`performance-review`**: UI thread safety, widget lifecycle, and rendering optimization.
* **`qa-ui`**: Functional testing of user interface workflows.
* **`screenshot-review`**: Visual inspection & UI comparison.
* **`sidebar-generator`**: Navigation sidebars and collapsible panels.
* **`table-modernizer`**: Data tables, grids, and list views.
* **`toolbar-generator`**: Action toolbars, status bars, and header panels.
* **`ui-modernization-master`**: Master orchestrator for complete UI redesigns.
