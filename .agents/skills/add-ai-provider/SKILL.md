---
name: add-ai-provider
description: Add a new AI API provider integration to the Web Content Rewriter application.
---
# Add AI Provider Skill

This skill guides the developer/agent in adding a completely new AI API provider (e.g. Cohere, Mistral, xAI, etc.) to the rewriting engine and the GUI.

## Applicable Files
- [rewriter_engine.py](file:///d:/softwares/xampp82new/htdocs/pythonmdfiles_gui/rewriter_engine.py)
- [gui_app.py](file:///d:/softwares/xampp82new/htdocs/pythonmdfiles_gui/gui_app.py)

## Instructions

1. **Add Provider Models**:
   - In `gui_app.py`, update `PROVIDER_MODELS` by adding the new provider name as a key and its supported models as a list of strings.
   - Update `ENV_KEY_MAP` with the new provider key and the expected environment variable name (e.g., `COHERE_API_KEY`).

2. **Update Engine Dependencies**:
   - If the provider requires a third-party SDK (e.g. `cohere`), add import statements inside a `try/except` block in `rewriter_engine.py`.
   - Update `requirements.txt` with the library name.

3. **Initialize API Client**:
   - In `MultiProviderLLMClient.__init__`, add initialization logic checking for the provider name. Instantiate the client using the appropriate credentials.

4. **Integrate calling logic**:
   - In `MultiProviderLLMClient._call_llm`, implement provider-specific request structure and token output parsing (getting input/output tokens from response metadata).
   
5. **Set Pricing Rates**:
   - Add default pricing tuples to `MODEL_PRICING` in `rewriter_engine.py` for token cost calculations.
