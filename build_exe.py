#!/usr/bin/env python3
"""
Automated PyInstaller Build Script for Desktop GUI Application
===============================================================
Locates customtkinter assets and compiles gui_app.py into a standalone Windows executable.
"""

import os
import sys
import subprocess
from pathlib import Path
import customtkinter

def build_executable():
    print("\n=======================================================")
    print("[DISABLED] Executable creation has been temporarily disabled by user command.")
    print("=======================================================\n")
    return

    ctk_path = Path(customtkinter.__file__).parent.resolve()
    print(f"CustomTkinter package path: {ctk_path}")

    # Build PyInstaller command
    # --add-data "ctk_path;customtkinter" bundles customtkinter's theme assets
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--onedir",
        "--windowed",
        "--name=WebRewriterApp",
        f"--add-data={ctk_path};customtkinter/",
        "gui_app.py"
    ]

    print("\nExecuting PyInstaller command:")
    print(" ".join(cmd))
    print("\nCompiling application... Please wait...")

    result = subprocess.run(cmd, cwd=os.path.dirname(__file__) or ".")
    
    if result.returncode == 0:
        print("\n=======================================================")
        print("[SUCCESS] Standalone Windows executable built successfully!")
        print(f"EXE Location: {os.path.abspath('dist/WebRewriterApp/WebRewriterApp.exe')}")
        print("=======================================================\n")


    else:
        print("\n✗ Build failed with exit code:", result.returncode)

if __name__ == "__main__":
    build_executable()
