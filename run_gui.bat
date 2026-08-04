@echo off
title Multi-Provider Web Content Rewriter GUI Launcher
echo Starting Desktop GUI Application with Token and Costing Metrics...

if exist venv\Scripts\python.exe (
    venv\Scripts\python.exe gui_app.py
) else (
    python gui_app.py
)

if errorlevel 1 (
    echo.
    echo Error starting application. Please verify dependencies are installed:
    echo .\venv\Scripts\pip install -r requirements.txt
    pause
)

