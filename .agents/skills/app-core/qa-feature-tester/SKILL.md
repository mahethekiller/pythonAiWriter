---
name: qa-feature-tester
description: Conducts automated headless and GUI functional testing, Python execution checks, API integration tests, and output payload validation (HTML, JSON-LD, Docx, WordPress REST API) to guarantee 100% bug-free feature releases.
---

# QA & Automated Feature Testing Skill (`qa-feature-tester`)

This skill defines the quality assurance, automated testing, and validation protocol for the **PythonAiWriter** desktop application.

## 🧪 Testing Verification Protocols

1. **Python Interpreter Sanity Test**:
   - Run python code execution check in virtual environment:
     ```powershell
     .\venv\Scripts\python.exe -c "import gui_app; app = gui_app.RewriterGUI(); print('OK')"
     ```

2. **GUI Launch Test**:
   - Test application launch script in non-blocking mode:
     ```powershell
     .\run_gui.bat
     ```

3. **Feature Payload Validation**:
   - **WordPress REST API**: Test endpoint authorization (`/wp-json/wp/v2/users/me`) and post creation payload formatting.
   - **XML Sitemap Miner**: Verify XML parsing of `<loc>` elements without crashing on malformed sitemaps.
   - **JSON-LD Schema**: Validate syntax of `@type: BlogPosting` and `@type: FAQPage` JSON-LD tags.
   - **SERP Crawler**: Verify DuckDuckGo / HTML scraper error handling and fallback behavior when offline.

4. **UI Thread & Contrast Checks**:
   - Ensure background thread callbacks use `.after(0, callback)`.
   - Verify high contrast for text and button states across both Light Mode and Dark Mode.
