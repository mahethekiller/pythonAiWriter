---
name: debug-and-enhance-layout-preservation
description: Inspect, debug, and refine layout-preserving HTML rewriting mode and CSS class/ID selectors parser.
---
# Debug and Enhance Layout Preservation Skill

This skill guides the agent in maintaining, debugging, and enhancing the structural layout preservation mechanism in the rewriting engine.

## Applicable Files
- [rewriter_engine.py](file:///d:/softwares/xampp82new/htdocs/pythonmdfiles_gui/rewriter_engine.py) (specifically `MultiProviderLLMClient.rewrite_layout` and `RewriterEngine.process_url`)

## Instructions

1. **Decomposed Tags Check**:
   - Check which elements are stripped out of the DOM in layout mode. Currently, `script`, `svg`, `img`, `picture`, `source`, and `figure` tags are removed.
   - Make sure structural elements (like `div`, `section`, `span`, headers, etc.) are kept intact.

2. **Length Constraints**:
   - The snippet passed to the model has a maximum character limit (currently `40000`). If a webpage is larger, check if it truncates properly without creating invalid HTML.
   
3. **Verify LLM Prompt Integrity**:
   - The prompt instructs the model to preserve all tag attributes, container hierarchy, classes, and IDs, rewriting only the human-readable text contents.
   - If user reports broken layout, inspect if the LLM returned raw text or altered class/ID attributes. Consider adding validation steps post-rewrite to verify HTML tags match the original structure.
