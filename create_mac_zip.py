#!/usr/bin/env python3
"""
Creates a clean, lightweight macOS Zip Archive (WebRewriterApp_macOS_Package.zip)
"""
import zipfile
from pathlib import Path

def zip_mac_package():
    root = Path(__file__).parent.resolve()
    zip_filename = root / "WebRewriterApp_macOS_Package.zip"

    files_to_include = [
        "gui_app.py",
        "rewriter_engine.py",
        "build_mac_app.py",
        "run_gui.command",
        "requirements.txt",
        "README_macOS.md",
        ".env.example",
        "test_urls.txt"
    ]

    print("Creating WebRewriterApp_macOS_Package.zip...")
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as z:
        for fname in files_to_include:
            fpath = root / fname
            if fpath.exists():
                z.write(fpath, arcname=fname)
                print(f"  + Added: {fname}")

    print(f"\n[SUCCESS] Created clean macOS Zip Package at: {zip_filename.resolve()}")

if __name__ == "__main__":
    zip_mac_package()
