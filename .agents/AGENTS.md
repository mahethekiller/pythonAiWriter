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
