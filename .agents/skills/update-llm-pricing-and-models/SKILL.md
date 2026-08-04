---
name: update-llm-pricing-and-models
description: Update AI model lists, endpoint logic, and pricing tables in the Web Content Rewriter application.
---
# Update LLM Pricing and Models Skill

This skill outlines how to update the supported models, pricing tables, and client mapping when AI API providers change their prices, add new models, or deprecate old models.

## Applicable Files
- [rewriter_engine.py](file:///d:/softwares/xampp82new/htdocs/pythonmdfiles_gui/rewriter_engine.py) (contains `MODEL_PRICING` dictionary and provider calls)
- [gui_app.py](file:///d:/softwares/xampp82new/htdocs/pythonmdfiles_gui/gui_app.py) (contains `PROVIDER_MODELS` and `ENV_KEY_MAP` dictionaries)

## Instructions

1. **Update Pricing in Engine**:
   - Locate the `MODEL_PRICING` dictionary in `rewriter_engine.py`.
   - Add/edit pricing tuples in the format: `"model-name-substring": (input_cost_per_1M_tokens, output_cost_per_1M_tokens)`.
   
2. **Update GUI Model Lists**:
   - Locate `PROVIDER_MODELS` in `gui_app.py`.
   - Append the new model identifier to the corresponding provider list so it appears in the dropdown.
   
3. **Verify API Call Mapping**:
   - Check `MultiProviderLLMClient._call_llm` in `rewriter_engine.py` to ensure the provider library can process the new model properly.
   - For example, if adding a new DeepSeek model, check if OpenAI client mapping handles it or if special logic is needed.
