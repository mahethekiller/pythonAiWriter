"""
Web scraping, layout-preserving rewriting, and semantic HTML rewriting engine.
"""

import os
import re
import json
import time
import requests
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Tuple, Optional, Callable, Any
import pandas as pd
from bs4 import BeautifulSoup, NavigableString, Comment, Doctype

from core.config import DEFAULT_USER_AGENT
from core.llm_client import MultiProviderLLMClient, calculate_cost_usd
from core.exporters import DocxExporter, generate_slug


class WebScraper:
    """Scrapes raw HTML content from target web URLs."""

    @staticmethod
    def scrape_url(url: str, timeout: int = 15) -> str:
        headers = {"User-Agent": DEFAULT_USER_AGENT}
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.text


class LayoutPreservingRewriter:
    """Rewrites text nodes within HTML while preserving exact CSS classes, IDs, DOM structure, and tags."""

    def __init__(self, llm_client: MultiProviderLLMClient):
        self.client = llm_client

    def rewrite_html(self, raw_html: str, custom_instruction: Optional[str] = None, include_header_footer: bool = False) -> Tuple[str, int, int, int, float]:
        soup = BeautifulSoup(raw_html, "html.parser")

        # Strip unneeded scripts and iframes while preserving <style> and <link> tags for CSS layout preservation
        strip_tags = ["script", "noscript", "iframe"]
        if not include_header_footer:
            strip_tags.extend(["header", "footer", "nav"])

        for tag in soup(strip_tags):
            tag.decompose()

        skip_parents = ["script", "style", "noscript", "svg", "iframe", "[document]", "head"]
        if not include_header_footer:
            skip_parents.extend(["header", "footer", "nav"])

        text_nodes: List[NavigableString] = []
        for node in soup.find_all(string=True):
            if type(node) is NavigableString and not isinstance(node, (Comment, Doctype)):
                parent_name = node.parent.name if node.parent else ""
                if parent_name not in skip_parents:
                    txt = str(node).strip()
                    if len(txt) > 2 and re.search(r"[a-zA-Z0-9]", txt):
                        text_nodes.append(node)

        if not text_nodes:
            return str(soup), 0, 0, 0, 0.0

        indexed_texts = {idx: str(node).strip() for idx, node in enumerate(text_nodes)}
        
        system_prompt = (
            "You are an expert web content rewriter. You will receive a JSON dictionary mapping numeric IDs to text snippets extracted from a webpage DOM.\n"
            "CRITICAL CONSTRAINTS:\n"
            "1. Rewrite each text snippet to be unique, engaging, and professional.\n"
            "2. Preserve original tone, meaning, and intent.\n"
            "3. DO NOT alter, add, or remove keys. Your output MUST be valid JSON mapping exact integer string keys to rewritten text strings.\n"
            "4. DO NOT wrap JSON output in markdown formatting like ```json ... ```."
        )

        if custom_instruction and custom_instruction.strip():
            system_prompt += f"\n\nCUSTOM USER INSTRUCTION:\n{custom_instruction.strip()}"

        user_prompt = json.dumps(indexed_texts, indent=2, ensure_ascii=False)

        raw_response, p_tokens, c_tokens, t_tokens = self.client._call_llm(system_prompt, user_prompt)
        cost_usd = calculate_cost_usd(self.client.model, p_tokens, c_tokens)

        clean_str = re.sub(r"^```(json)?\s*", "", raw_response, flags=re.IGNORECASE)
        clean_str = re.sub(r"\s*```$", "", clean_str)

        try:
            rewritten_map = json.loads(clean_str.strip())
            for idx_str, new_txt in rewritten_map.items():
                idx = int(idx_str)
                if 0 <= idx < len(text_nodes):
                    text_nodes[idx].replace_with(new_txt)
        except Exception:
            pass

        return str(soup), p_tokens, c_tokens, t_tokens, cost_usd


class SemanticRewriter:
    """Extracts semantic body content (h1-h6, p, ul, ol, blockquote) and rewrites into clean semantic HTML."""

    def __init__(self, llm_client: MultiProviderLLMClient):
        self.client = llm_client

    def rewrite_html(self, raw_html: str, custom_instruction: Optional[str] = None) -> Tuple[str, int, int, int, float]:
        soup = BeautifulSoup(raw_html, "html.parser")
        
        for tag in soup(["script", "style", "noscript", "svg", "iframe", "nav", "footer", "header"]):
            tag.decompose()

        main_content = soup.find("main") or soup.find("article") or soup.find("body") or soup

        semantic_html = str(main_content)

        system_prompt = (
            "You are an expert web content rewriter. Rewrite the provided semantic HTML webpage content into fresh, original, unique HTML content.\n"
            "CRITICAL CONSTRAINTS:\n"
            "1. Output ONLY valid body HTML tags (<h1>, <h2>, <h3>, <p>, <ul>, <li>, <blockquote>, <strong>).\n"
            "2. Preserve structural depth and heading hierarchy.\n"
            "3. DO NOT wrap output in markdown code blocks like ```html ... ```."
        )

        if custom_instruction and custom_instruction.strip():
            system_prompt += f"\n\nCUSTOM USER INSTRUCTION:\n{custom_instruction.strip()}"

        raw_response, p_tokens, c_tokens, t_tokens = self.client._call_llm(system_prompt, semantic_html[:15000])
        cost_usd = calculate_cost_usd(self.client.model, p_tokens, c_tokens)

        clean_html = re.sub(r"^```(html)?\s*", "", raw_response, flags=re.IGNORECASE)
        clean_html = re.sub(r"\s*```$", "", clean_html)

        return clean_html.strip(), p_tokens, c_tokens, t_tokens, cost_usd


def run_batch_process(
    urls: List[str],
    provider: str,
    api_key: str,
    model: str,
    mode: str,
    generate_html: bool,
    generate_docx: bool,
    main_save_folder: Path,
    max_workers: int = 3,
    custom_instruction: Optional[str] = None,
    base_url: Optional[str] = None,
    include_header_footer: bool = False,
    progress_cb: Optional[Callable[[int, int, str], None]] = None,
    log_cb: Optional[Callable[[str], None]] = None
) -> Tuple[pd.DataFrame, Path, Path, Dict[str, Any]]:
    """Runs batch URL scraping & rewriting in background threads, saving outputs and metrics."""
    
    timestamp_folder_name = f"Run_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
    run_output_dir = Path(main_save_folder) / timestamp_folder_name
    run_output_dir.mkdir(parents=True, exist_ok=True)

    llm_client = MultiProviderLLMClient(provider=provider, api_key=api_key, model=model, base_url=base_url)

    if mode == "Layout-Preserving HTML":
        rewriter = LayoutPreservingRewriter(llm_client)
    else:
        rewriter = SemanticRewriter(llm_client)

    results = []
    total_urls = len(urls)
    completed_count = 0

    if log_cb:
        log_cb(f"Starting batch rewrite for {total_urls} URLs (provider={provider}, model={model}, mode={mode})...")

    def _process_url(url: str) -> Dict[str, Any]:
        url = url.strip()
        slug = generate_slug(url)
        res = {
            "URL": url,
            "Slug": slug,
            "Status": "Failed",
            "Error": "",
            "Prompt_Tokens": 0,
            "Completion_Tokens": 0,
            "Total_Tokens": 0,
            "Cost_USD": 0.0,
            "HTML_Path": "",
            "DOCX_Path": ""
        }

        try:
            if log_cb:
                log_cb(f"Fetching: {url}...")
            raw_html = WebScraper.scrape_url(url)

            if log_cb:
                log_cb(f"Rewriting: {url}...")
            if isinstance(rewriter, LayoutPreservingRewriter):
                rewritten_html, p_tok, c_tok, t_tok, cost = rewriter.rewrite_html(raw_html, custom_instruction, include_header_footer=include_header_footer)
            else:
                rewritten_html, p_tok, c_tok, t_tok, cost = rewriter.rewrite_html(raw_html, custom_instruction)

            res["Status"] = "Success"
            res["Prompt_Tokens"] = p_tok
            res["Completion_Tokens"] = c_tok
            res["Total_Tokens"] = t_tok
            res["Cost_USD"] = round(cost, 6)

            if generate_html:
                html_dir = run_output_dir / "html_files"
                html_dir.mkdir(parents=True, exist_ok=True)
                html_file = html_dir / f"{slug}.html"
                with open(html_file, "w", encoding="utf-8") as f:
                    f.write(rewritten_html)
                res["HTML_Path"] = str(html_file.resolve())

            if generate_docx:
                docx_dir = run_output_dir / "docx_files"
                docx_dir.mkdir(parents=True, exist_ok=True)
                docx_file = docx_dir / f"{slug}.docx"
                DocxExporter.html_to_docx(rewritten_html, docx_file)
                res["DOCX_Path"] = str(docx_file.resolve())

            if log_cb:
                log_cb(f"✓ Success: {url} | Tokens: {t_tok:,} | Cost: ${cost:.6f}")

        except Exception as exc:
            res["Error"] = str(exc)
            if log_cb:
                log_cb(f"✗ Failed: {url} | Error: {exc}")

        return res

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_process_url, url): url for url in urls}
        for future in as_completed(futures):
            try:
                result_data = future.result()
                results.append(result_data)
            except Exception as exc:
                pass

            completed_count += 1
            if progress_cb:
                progress_cb(completed_count, total_urls, "Processing batch...")

    df = pd.DataFrame(results)

    total_prompt_tokens = int(df["Prompt_Tokens"].sum()) if "Prompt_Tokens" in df else 0
    total_completion_tokens = int(df["Completion_Tokens"].sum()) if "Completion_Tokens" in df else 0
    total_tokens = int(df["Total_Tokens"].sum()) if "Total_Tokens" in df else 0
    total_cost_usd = float(df["Cost_USD"].sum()) if "Cost_USD" in df else 0.0

    summary_metrics = {
        "execution_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "provider": provider,
        "model": model,
        "mode": mode,
        "total_urls": total_urls,
        "successful": len([r for r in results if r["Status"] == "Success"]),
        "failed": len([r for r in results if r["Status"] == "Failed"]),
        "total_prompt_tokens": total_prompt_tokens,
        "total_completion_tokens": total_completion_tokens,
        "total_tokens": total_tokens,
        "total_cost_usd": round(total_cost_usd, 6)
    }

    excel_path = run_output_dir / "processing_status.xlsx"
    csv_path = run_output_dir / "processing_status.csv"

    try:
        df.to_excel(excel_path, index=False, engine='openpyxl')
        df.to_csv(csv_path, index=False)
    except Exception:
        pass

    return df, excel_path, run_output_dir, summary_metrics
