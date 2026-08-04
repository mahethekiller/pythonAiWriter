---
name: build-standalone-executables
description: Compile and package the desktop GUI application into standalone Windows .exe and macOS .app bundles.
---
# Build Standalone Executables Skill

This skill explains how to build, troubleshoot, and package the CustomTkinter GUI application as a standalone executable.

## Applicable Files
- [build_exe.py](file:///d:/softwares/xampp82new/htdocs/pythonmdfiles_gui/build_exe.py) (compilation for Windows)
- [build_mac_app.py](file:///d:/softwares/xampp82new/htdocs/pythonmdfiles_gui/build_mac_app.py) (compilation for macOS)
- [create_mac_zip.py](file:///d:/softwares/xampp82new/htdocs/pythonmdfiles_gui/create_mac_zip.py) (source packaging for macOS)

## Instructions

> [!WARNING]
> **DO NOT automatically compile the executable or create zip archives after making changes or adding features.** Compiling takes significant time and resources. Executable compilation and archiving should only be run when explicitly requested by the user.

1. **Verify CustomTkinter Assets**:
   - Ensure the build script locates the `customtkinter` directory using `import customtkinter` and bundles its assets.
   - For Windows, check `build_exe.py` passes `f"--add-data={ctk_path};customtkinter/"` to PyInstaller.
   - For macOS, check `build_mac_app.py` passes `f"--add-data={ctk_path}:customtkinter/"` to PyInstaller.

2. **Trigger Compilation**:
   - Compile the executable only when specifically requested.
   - Run `python build_exe.py` on Windows to output the binary to `dist/WebRewriterApp/WebRewriterApp.exe`.
   - Run `python3 build_mac_app.py` on macOS to output the app bundle to `dist/WebRewriterApp.app`.
   - Note: Automatic `.zip` packaging of build folders has been disabled to prevent unnecessary disk overhead during incremental development.

3. **Packaging Sources**:
   - Run `python create_mac_zip.py` to generate a developer source zip containing code scripts and instructions.
