@echo off
title Multi-Provider Web Content Rewriter GUI Launcher
echo Starting Desktop GUI Application with Token & Costing Metrics...
python gui_app.py
if errorlevel 1 (
    echo.
    echo Error starting application. Please verify dependencies are installed:
    echo python -m pip install -r requirements.txt
    pause
)
