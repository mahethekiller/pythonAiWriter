"""
SEO Blog Article Generator, Keyword Density Auditing, Schema Generation, SERP Mining, and Humanization Engine.
"""

import re
import json
import requests
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Tuple, Optional, Callable, Any
import pandas as pd
from bs4 import BeautifulSoup

from core.config import DEFAULT_USER_AGENT
from core.llm_client import MultiProviderLLMClient, calculate_cost_usd
from core.exporters import DocxExporter, generate_slug
from core.humanizer import AIHumanizer
from core.schema_generator import SchemaGenerator
from core.serp_crawler import SERPCrawler
from core.sitemap_miner import SitemapMiner


def count_syllables(word: str) -> int:
    """Estimates the syllable count of an English word."""
    word = word.lower().strip()
    if len(word) <= 3:
        return 1
    word = re.sub(r'(?:[^laeiouy]|ed|es|e)$', '', word)
    word = re.sub(r'^y', '', word)
    syllables = len(re.findall(r'[aeiouy]{1,2}', word))
    return max(1, syllables)


def calculate_flesch_reading_ease(text: str) -> float:
    """Calculates Flesch Reading Ease score for body content."""
    clean_txt = re.sub(r'<[^>]+>', ' ', text).strip()
    words = re.findall(r'\b\w+\b', clean_txt)
    sentences = [s for s in re.split(r'[.!?]+', clean_txt) if s.strip()]
    
    num_words = len(words)
    num_sentences = max(1, len(sentences))
    num_syllables = sum(count_syllables(w) for w in words)
    
    if num_words == 0:
        return 100.0
        
    score = 206.835 - (1.015 * (num_words / num_sentences)) - (84.6 * (num_syllables / num_words))
    return round(max(0.0, min(100.0, score)), 1)


class SEOArticleGenerator:
    """Generates SEO-optimized long-form articles, link insertions, AI image prompts, and metrics."""

    def __init__(self, llm: MultiProviderLLMClient):
        self.llm = llm
        self.humanizer = AIHumanizer()
        self.serp_crawler = SERPCrawler()

    def generate_article(
        self,
        topic: str,
        primary_keyword: str,
        secondary_keywords: List[str],
        search_intent: str,
        tone: str,
        format_type: str,
        target_audience: str,
        word_count_target: str,
        internal_links: List[str],
        include_external_links: bool = True,
        include_image_prompts: bool = True,
        custom_outline: Optional[str] = None,
        include_tldr: bool = True,
        include_faq: bool = True,
        cta_text: Optional[str] = None,
        competitor_urls: List[str] = [],
        enable_serp_mining: bool = False,
        enable_humanizer: bool = True,
        sitemap_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generates full SEO article content through multi-stage production pipeline."""

        # 0. Mine Sitemap Internal Links if URL provided
        if sitemap_url and not internal_links:
            miner = SitemapMiner()
            fetched_urls = miner.fetch_internal_urls(sitemap_url, max_urls=6)
            if fetched_urls:
                internal_links = fetched_urls
        
        # 1. Live SERP & Competitor Research Pass
        serp_context = ""
        if enable_serp_mining:
            try:
                intel = self.serp_crawler.fetch_serp_intel(primary_keyword)
                if intel.get("competitor_headings") or intel.get("paa_questions"):
                    headings_str = "\n  - ".join(intel.get("competitor_headings", []))
                    paa_str = "\n  - ".join(intel.get("paa_questions", []))
                    serp_context = (
                        f"\n\nLIVE COMPETITOR SERP INTEL:\n"
                        f"• Competitor Avg Word Count: ~{intel.get('avg_word_count', 1800)} words\n"
                        f"• Key Competitor Headings Covered in Top Rankings:\n  - {headings_str}\n"
                        f"• Frequently Asked Questions (People Also Ask):\n  - {paa_str}\n"
                    )
            except Exception:
                pass

        # 2. Competitor URLs Context
        competitor_context = ""
        if competitor_urls:
            ref_texts = []
            for comp_url in competitor_urls[:2]:
                try:
                    res = requests.get(comp_url, headers={"User-Agent": DEFAULT_USER_AGENT}, timeout=8)
                    if res.ok:
                        s = BeautifulSoup(res.content, "html.parser")
                        main_b = s.find("main") or s.find("body") or s
                        ref_texts.append(f"Source ({comp_url}):\n" + main_b.get_text(separator=" ", strip=True)[:2000])
                except Exception:
                    pass
            if ref_texts:
                competitor_context = "\n\nCompetitor Reference Content:\n" + "\n---\n".join(ref_texts)

        # 3. Step A: Meta Title, Meta Description & Slug Generation
        meta_system_prompt = (
            "You are an expert SEO strategist. Generate a high-CTR Meta Title, a compelling Meta Description, and a clean URL Slug.\n"
            "CRITICAL CONSTRAINTS:\n"
            "1. Meta Title MUST be <= 60 characters and contain the primary keyword.\n"
            "2. Meta Description MUST be <= 160 characters.\n"
            "3. Output format MUST be valid JSON with keys: 'meta_title', 'meta_description', 'url_slug'."
        )
        meta_user_prompt = f"Topic: {topic}\nPrimary Keyword: {primary_keyword}\nSearch Intent: {search_intent}"
        
        raw_meta, p_tok1, c_tok1, t_tok1 = self.llm.generate_text(meta_system_prompt, meta_user_prompt)
        
        try:
            clean_json_str = re.sub(r"^```(json)?\s*", "", raw_meta, flags=re.IGNORECASE)
            clean_json_str = re.sub(r"\s*```$", "", clean_json_str)
            meta_data = json.loads(clean_json_str.strip())
        except Exception:
            meta_data = {
                "meta_title": topic[:60],
                "meta_description": f"Comprehensive guide about {topic} targeting {primary_keyword}.",
                "url_slug": generate_slug(topic)
            }

        # 4. Step B: Article Writing Prompt Assembly
        links_instruction = ""
        if internal_links:
            formatted_links = ", ".join([f"<{url}>" for url in internal_links])
            links_instruction += f"\n- Contextually embed hyperlinked anchors pointing to these internal URLs where relevant: {formatted_links}."
        if include_external_links:
            links_instruction += "\n- Include 1 or 2 outbound links to authoritative external web sources (e.g. Wikipedia, research stats, official docs) using standard HTML <a> tags."

        media_instruction = ""
        if include_image_prompts:
            media_instruction = (
                "\n- Insert 2 to 3 AI Image Callout Prompts at key section breaks using this EXACT HTML structure:\n"
                '<div style="background-color: #1e293b; color: #e2e8f0; border-left: 4px solid #3b82f6; padding: 12px; margin: 16px 0; border-radius: 4px;">\n'
                '  📸 <strong>AI Image Prompt:</strong> <em>[Detailed prompt description for Midjourney/DALL-E]</em><br>\n'
                '  <small>🏷️ <strong>Alt Text:</strong> [Keyword-rich image alt text]</small>\n'
                '</div>'
            )

        tldr_instruction = ""
        if include_tldr:
            tldr_instruction = (
                "\n- Include a 'Key Takeaways' / TL;DR callout box right after the <h1> title formatted cleanly in HTML using:\n"
                '<div style="background-color: #0f172a; color: #f8fafc; border: 1px solid #334155; padding: 14px; border-radius: 6px; margin-bottom: 20px;">\n'
                '  <strong>💡 Key Takeaways:</strong>\n'
                '  <ul><li>Point 1</li><li>Point 2</li><li>Point 3</li></ul>\n'
                '</div>'
            )

        faq_instruction = ""
        if include_faq:
            faq_instruction = (
                "\n- Conclude the article with a 'Frequently Asked Questions (FAQ)' section featuring 3 high-volume People Also Ask Q&As, using <h2>Frequently Asked Questions</h2> and <h3> question headers."
            )

        cta_instruction = ""
        if cta_text and cta_text.strip():
            cta_instruction = f"\n- End the article with a clear Call to Action (CTA) callout box featuring this instruction: {cta_text.strip()}."

        custom_outline_instruction = ""
        if custom_outline and custom_outline.strip():
            custom_outline_instruction = f"\n- Strictly follow this user-specified outline / heading structure:\n{custom_outline.strip()}"

        sec_keywords_str = ", ".join(secondary_keywords) if secondary_keywords else "None"

        article_system_prompt = (
            f"You are an elite SEO content writer and subject matter expert. Write a comprehensive, highly engaging, and search-optimized blog article.\n\n"
            f"STRATEGY SPECIFICATIONS:\n"
            f"• Target Audience: {target_audience}\n"
            f"• Tone of Voice: {tone}\n"
            f"• Article Format: {format_type}\n"
            f"• Target Word Count Length: {word_count_target}\n"
            f"• Search Intent: {search_intent}\n"
            f"• Primary Keyword: '{primary_keyword}' (Use naturally across headers, intro, body, and conclusion; target density ~1.5%)\n"
            f"• Secondary / LSI Keywords: {sec_keywords_str}\n\n"
            f"FORMATTING & COMPLIANCE RULES:\n"
            f"1. Output ONLY valid semantic HTML body content (starting with <h1>, then <h2>, <h3>, <p>, <ul>, <li>, <strong>, <a>).\n"
            f"2. DO NOT wrap output in markdown code blocks like ```html ... ```.\n"
            f"3. Ensure smooth transitions, short punchy paragraphs, and actionable insights."
            f"{tldr_instruction}"
            f"{links_instruction}"
            f"{media_instruction}"
            f"{faq_instruction}"
            f"{cta_instruction}"
            f"{custom_outline_instruction}"
            f"{serp_context}"
        )

        article_user_prompt = f"Topic: {topic}\nPrimary Keyword: {primary_keyword}\n{competitor_context}"

        content_html, p_tok2, c_tok2, t_tok2 = self.llm.generate_text(article_system_prompt, article_user_prompt)

        # 5. AI Humanizer Polish Pass
        if enable_humanizer:
            content_html = self.humanizer.humanize_text(content_html)

        total_prompt_tokens = p_tok1 + p_tok2
        total_completion_tokens = c_tok1 + c_tok2
        total_tokens = total_prompt_tokens + total_completion_tokens
        cost_usd = calculate_cost_usd(self.llm.model, total_prompt_tokens, total_completion_tokens)

        # 6. Step C: SEO Audit & Metrics Calculation
        clean_text_content = re.sub(r'<[^>]+>', ' ', content_html)
        words_list = re.findall(r'\b\w+\b', clean_text_content.lower())
        word_count = len(words_list)

        # Primary Keyword Density
        pk_clean = primary_keyword.lower().strip()
        pk_count = clean_text_content.lower().count(pk_clean) if pk_clean else 0
        pk_words_len = len(pk_clean.split())
        pk_density = round((pk_count * pk_words_len / max(1, word_count)) * 100, 2)

        # Readability Score
        readability_score = calculate_flesch_reading_ease(content_html)
        if readability_score >= 80:
            readability_label = f"{readability_score} (Easy / 6th Grade)"
        elif readability_score >= 60:
            readability_label = f"{readability_score} (Standard / 8th-9th Grade)"
        elif readability_score >= 40:
            readability_label = f"{readability_score} (Fairly Difficult / High School)"
        else:
            readability_label = f"{readability_score} (Advanced / University)"

        # Check Meta Length Pass/Fail
        meta_title_pass = len(meta_data.get("meta_title", "")) <= 60
        meta_desc_pass = len(meta_data.get("meta_description", "")) <= 160

        # Count Headings
        soup = BeautifulSoup(content_html, "html.parser")
        h2_count = len(soup.find_all("h2"))
        h3_count = len(soup.find_all("h3"))
        img_prompt_count = content_html.count("AI Image Prompt:")

        # Dynamic Composite SEO Health Score (0 - 100)
        score_density = 25 if (1.0 <= pk_density <= 2.5) else (18 if (0.5 <= pk_density <= 3.5) else 10)
        score_readability = 25 if (60 <= readability_score <= 85) else (18 if (40 <= readability_score <= 95) else 10)
        score_headings = 25 if (h2_count >= 2 and h3_count >= 1) else (18 if h2_count >= 1 else 10)
        score_meta = 25 if (meta_title_pass and meta_desc_pass) else 15
        
        seo_score = score_density + score_readability + score_headings + score_meta
        reading_time_min = max(1, round(word_count / 200))

        # 7. Generate JSON-LD Schema.org Markup
        article_schema = SchemaGenerator.generate_article_schema(
            title=meta_data.get("meta_title", topic),
            meta_description=meta_data.get("meta_description", ""),
            url_slug=meta_data.get("url_slug", generate_slug(topic))
        )

        faq_items = []
        if include_faq:
            for h3 in soup.find_all("h3"):
                q_text = h3.get_text(strip=True)
                p_sibling = h3.find_next_sibling("p")
                if p_sibling:
                    faq_items.append({"question": q_text, "answer": p_sibling.get_text(strip=True)})
        
        faq_schema = SchemaGenerator.generate_faq_schema(faq_items)
        schemas_to_inject = [article_schema]
        if faq_schema:
            schemas_to_inject.append(faq_schema)

        # Generate Markdown and HTML with embedded Schema
        content_md = f"# {meta_data.get('meta_title', topic)}\n\n" + re.sub(r'<p>(.*?)</p>', r'\1\n\n', content_html)
        content_md = re.sub(r'<h[23]>(.*?)</h[23]>', r'\n## \1\n', content_md)
        content_md = re.sub(r'<[^>]+>', '', content_md)

        full_html = (
            "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n"
            "  <meta charset=\"UTF-8\">\n"
            f"  <title>{meta_data.get('meta_title', topic)}</title>\n"
            f"  <meta name=\"description\" content=\"{meta_data.get('meta_description', '')}\">\n"
            "  <style>body { font-family: system-ui, sans-serif; line-height: 1.6; max-width: 850px; margin: 40px auto; padding: 0 20px; color: #1e293b; } h1 { color: #0f172a; } h2 { color: #1e3a8a; border-bottom: 1px solid #e2e8f0; padding-bottom: 6px; } h3 { color: #2563eb; } a { color: #2563eb; text-decoration: underline; } ul { padding-left: 20px; }</style>\n"
            "</head>\n<body>\n"
            f"{content_html}\n"
            "</body>\n</html>"
        )
        full_html = SchemaGenerator.inject_schema_into_html(full_html, schemas_to_inject)

        metrics = {
            "topic": topic,
            "meta_title": meta_data.get("meta_title", topic),
            "meta_description": meta_data.get("meta_description", ""),
            "url_slug": meta_data.get("url_slug", generate_slug(topic)),
            "word_count": word_count,
            "reading_time_min": reading_time_min,
            "seo_score": seo_score,
            "primary_keyword": primary_keyword,
            "pk_count": pk_count,
            "pk_density": pk_density,
            "readability_score": readability_score,
            "readability_label": readability_label,
            "meta_title_pass": meta_title_pass,
            "meta_desc_pass": meta_desc_pass,
            "h2_count": h2_count,
            "h3_count": h3_count,
            "img_prompt_count": img_prompt_count,
            "prompt_tokens": total_prompt_tokens,
            "completion_tokens": total_completion_tokens,
            "total_tokens": total_tokens,
            "cost_usd": cost_usd,
            "content_html_body": content_html,
            "full_html": full_html,
            "content_md": content_md,
            "schemas": schemas_to_inject
        }

        return metrics


def run_blog_batch_process(
    topics_data: List[Dict[str, Any]],
    provider: str,
    api_key: str,
    model: str,
    generate_html: bool,
    generate_docx: bool,
    generate_md: bool,
    generate_json: bool,
    main_save_folder: Path,
    max_workers: int = 3,
    base_url: Optional[str] = None,
    progress_cb: Optional[Callable[[int, int, str], None]] = None,
    log_cb: Optional[Callable[[str], None]] = None
) -> Tuple[pd.DataFrame, Path, Path, Dict[str, Any]]:
    """Runs batch blog article generation, exports output files, and logs metrics."""
    timestamp_folder_name = f"Blog_Run_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
    run_output_dir = Path(main_save_folder) / timestamp_folder_name
    run_output_dir.mkdir(parents=True, exist_ok=True)

    llm = MultiProviderLLMClient(provider=provider, api_key=api_key, model=model, base_url=base_url)
    generator = SEOArticleGenerator(llm)

    results = []
    total = len(topics_data)
    completed = 0

    if log_cb:
        log_cb(f"Starting SEO Blog Generation for {total} topics (provider={provider}, model={model})...")

    def _process_item(item_data):
        topic = item_data.get("topic", "Untitled Topic")
        slug = item_data.get("url_slug") or generate_slug(topic)
        if log_cb:
            log_cb(f"Writing SEO Article: '{topic}'...")

        res_metrics = generator.generate_article(
            topic=topic,
            primary_keyword=item_data.get("primary_keyword", topic),
            secondary_keywords=item_data.get("secondary_keywords", []),
            search_intent=item_data.get("search_intent", "Informational"),
            tone=item_data.get("tone", "Conversational & Engaging"),
            format_type=item_data.get("format_type", "Ultimate Guide"),
            target_audience=item_data.get("target_audience", "General Audience"),
            word_count_target=item_data.get("word_count_target", "Standard (~1,500 words)"),
            internal_links=item_data.get("internal_links", []),
            include_external_links=item_data.get("include_external_links", True),
            include_image_prompts=item_data.get("include_image_prompts", True),
            custom_outline=item_data.get("custom_outline"),
            include_tldr=item_data.get("include_tldr", True),
            include_faq=item_data.get("include_faq", True),
            cta_text=item_data.get("cta_text"),
            competitor_urls=item_data.get("competitor_urls", []),
            enable_serp_mining=item_data.get("enable_serp_mining", False),
            enable_humanizer=item_data.get("enable_humanizer", True),
            sitemap_url=item_data.get("sitemap_url")
        )

        html_file, docx_file, md_file, json_file = "", "", "", ""

        if generate_html:
            html_dir = run_output_dir / "html_articles"
            html_dir.mkdir(parents=True, exist_ok=True)
            html_path = html_dir / f"{slug}.html"
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(res_metrics["full_html"])
            html_file = str(html_path.resolve())

        if generate_docx:
            docx_dir = run_output_dir / "docx_articles"
            docx_dir.mkdir(parents=True, exist_ok=True)
            docx_path = docx_dir / f"{slug}.docx"
            DocxExporter.html_to_docx(res_metrics["content_html_body"], docx_path)
            docx_file = str(docx_path.resolve())

        if generate_md:
            md_dir = run_output_dir / "md_articles"
            md_dir.mkdir(parents=True, exist_ok=True)
            md_path = md_dir / f"{slug}.md"
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(res_metrics["content_md"])
            md_file = str(md_path.resolve())

        if generate_json:
            json_dir = run_output_dir / "json_cms_payloads"
            json_dir.mkdir(parents=True, exist_ok=True)
            json_path = json_dir / f"{slug}.json"
            json_payload = {
                "title": res_metrics["topic"],
                "slug": res_metrics["url_slug"],
                "meta_title": res_metrics["meta_title"],
                "meta_description": res_metrics["meta_description"],
                "content_html": res_metrics["content_html_body"],
                "content_markdown": res_metrics["content_md"],
                "json_ld_schemas": res_metrics.get("schemas", []),
                "seo_audit": {
                    "word_count": res_metrics["word_count"],
                    "primary_keyword": res_metrics["primary_keyword"],
                    "keyword_density_percent": res_metrics["pk_density"],
                    "readability_score": res_metrics["readability_score"],
                    "readability_label": res_metrics["readability_label"]
                }
            }
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(json_payload, f, indent=2)
            json_file = str(json_path.resolve())

        res_metrics["HTML_Path"] = html_file
        res_metrics["DOCX_Path"] = docx_file
        res_metrics["MD_Path"] = md_file
        res_metrics["JSON_Path"] = json_file

        if log_cb:
            log_cb(f"✓ Completed: '{topic}' | Words: {res_metrics['word_count']} | Density: {res_metrics['pk_density']}% | Cost: ${res_metrics['cost_usd']:.6f}")

        return res_metrics

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_process_item, item): item for item in topics_data}
        for future in as_completed(futures):
            try:
                rec = future.result()
                results.append(rec)
            except Exception as exc:
                if log_cb:
                    log_cb(f"✗ Article generation error: {exc}")

            completed += 1
            if progress_cb:
                progress_cb(completed, total, "Processing article...")

    df = pd.DataFrame(results)

    total_prompt_tokens = int(df["prompt_tokens"].sum()) if "prompt_tokens" in df else 0
    total_completion_tokens = int(df["completion_tokens"].sum()) if "completion_tokens" in df else 0
    total_tokens = int(df["total_tokens"].sum()) if "total_tokens" in df else 0
    total_cost_usd = float(df["cost_usd"].sum()) if "cost_usd" in df else 0.0

    summary_metrics = {
        "execution_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "provider": provider,
        "model": model,
        "total_articles": total,
        "total_prompt_tokens": total_prompt_tokens,
        "total_completion_tokens": total_completion_tokens,
        "total_tokens": total_tokens,
        "total_cost_usd": round(total_cost_usd, 6),
        "last_article_metrics": results[0] if results else {}
    }

    excel_path = run_output_dir / "blog_generation_report.xlsx"
    csv_path = run_output_dir / "blog_generation_report.csv"

    try:
        df.to_excel(excel_path, index=False, engine='openpyxl')
        df.to_csv(csv_path, index=False)
    except Exception:
        pass

    return df, excel_path, run_output_dir, summary_metrics
