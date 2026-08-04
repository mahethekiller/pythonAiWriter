#!/usr/bin/env python3
"""
Automated PyInstaller Build Script for macOS (.app bundle & .zip)
===================================================================
Run this script on any Mac computer to compile WebRewriterApp.app and create WebRewriterApp_macOS.zip.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import customtkinter

def build_mac_app():
    print("\n=======================================================")
    print("[DISABLED] macOS Executable creation has been temporarily disabled by user command.")
    print("=======================================================\n")
    return

    ctk_path = Path(customtkinter.__file__).parent.resolve()
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--onedir",
        "--windowed",
        "--name=WebRewriterApp",
        f"--add-data={ctk_path}:customtkinter/",
        "gui_app.py"
    ]

    print("\nExecuting PyInstaller command for macOS:")
    print(" ".join(cmd))
    print("\nCompiling macOS Application... Please wait...")

    result = subprocess.run(cmd, cwd=os.path.dirname(__file__) or ".")
    
    if result.returncode == 0:
        print("\n=======================================================")
        print("[SUCCESS] Standalone macOS application built successfully!")
        print(f"App Location: {os.path.abspath('dist/WebRewriterApp.app')}")
        print("=======================================================\n")
    else:
        print("\n✗ macOS Build failed with exit code:", result.returncode)

if __name__ == "__main__":
    build_mac_app()
