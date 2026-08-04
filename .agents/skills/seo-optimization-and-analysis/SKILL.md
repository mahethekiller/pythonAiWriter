---
name: seo-optimization-and-analysis
description: Guide implementation of SEO-related features, metadata rewriting, content grading, and keyword preservation rules.
---
# SEO Optimization and Analysis Skill

This skill guides the agent in developing, debugging, and extending SEO-centric features within the Web Content Rewriter, such as keyword insertion, meta tag auto-generation, readability scores, and structural search-engine friendliness audits.

## Applicable Files
- [rewriter_engine.py](file:///d:/softwares/xampp82new/htdocs/pythonmdfiles_gui/rewriter_engine.py) (specifically system prompts and HTML parsers)
- [gui_app.py](file:///d:/softwares/xampp82new/htdocs/pythonmdfiles_gui/gui_app.py) (for user-facing SEO toggles/parameters)

## Instructions

1. **Keyword Optimization & Preservation**:
   - If extending the application to support target keyword lists:
     - Prompt instructions must guide the LLM to weave keywords naturally without keyword-stuffing.
     - Add post-processing checks to count keyword density (target range: 1-2.5%).

2. **SEO Metadata Generation**:
   - When generating/extracting metadata for rewritten HTML files:
     - **Title Tags**: Ensure titles are concise, descriptive, and under 60 characters.
     - **Meta Descriptions**: Guide the LLM to generate summary descriptions under 160 characters containing core value propositions.
     - **Heading Hierarchy**: Enforce semantic HTML standards (a single `<h1>` tag per page, followed by sequential `<h2>`, `<h3>` tags).

3. **Content Quality & Readability Metrics**:
   - When integrating readability estimators:
     - Use mathematical algorithms (e.g. Flesch Reading Ease) or token-based analysis to output content complexity scores.
     - Compare original versus rewritten text length to prevent significant content thinning (i.e. keep rewritten word count within ±15% of the original).

4. **URL & Link Integrity**:
   - Always ensure relative internal links are converted to absolute links using the source domain's `<base>` tag (already supported). Check that relative anchor paths `href` do not break.
   
5. **SEO Compliance Validator**:
   - If implementing an automated audit checker:
     - Validate that all generated images have descriptive `alt` attributes.
     - Scan for empty tags (e.g. empty paragraphs or headers) and remove them to clean up code bloat.
