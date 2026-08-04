# Web Content Rewriter - macOS Setup & Troubleshooting Guide

A modern desktop GUI application for macOS supporting multi-provider AI (OpenAI, Gemini, Anthropic Claude, DeepSeek, Groq, Ollama), custom prompt instructions, layout preservation, and token/cost tracking.

---

## 🔑 Fixing "Access Privileges" / "Permission Denied" Error on Mac

When macOS unzips downloaded files, it disables script execution permissions by default. 

To fix this with **1 line in Mac Terminal**:

1. Open **Terminal** on your Mac.
2. Navigate to the extracted folder (or drag the folder into Terminal):
   ```bash
   cd /path/to/extracted/folder
   ```
3. Run this command to grant execution permissions:
   ```bash
   chmod +x run_gui.command
   ```

Now double-click **`run_gui.command`** in Finder!

---

## 🛡️ Fixing "Developer Cannot Be Verified" Gatekeeper Error

1. **Right-Click** (or `Control + Click`) on `run_gui.command` in Finder.
2. Click **Open** from the menu.
3. Click **Open** in the dialog box.

*Or run in Terminal:*
```bash
xattr -cr .
```

---

## Quick Launch Options

### Option 1: Double-Click Launcher
Double-click **`run_gui.command`** in Finder.

### Option 2: Build Standalone Mac `.app` Bundle
To compile into a native standalone **`WebRewriterApp.app`** icon on your Mac:
```bash
python3 build_mac_app.py
```
This creates `dist/WebRewriterApp.app` which can be opened directly without Terminal!
