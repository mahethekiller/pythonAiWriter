#!/bin/bash
# macOS Double-Click GUI Launcher Script
cd "$(dirname "$0")"
echo "======================================================="
echo "   Starting Web Content Rewriter Desktop GUI for Mac   "
echo "======================================================="

# Ensure dependencies are installed
python3 -m pip install -r requirements.txt

# Launch GUI Application
python3 gui_app.py
