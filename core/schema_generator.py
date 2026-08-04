"""
JSON-LD Schema.org Structured Data Generator for PythonAiWriter.
Generates Google Rich Result schemas for BlogPosting, FAQPage, and HowTo.
"""

import json
from typing import List, Dict, Any, Optional


class SchemaGenerator:
    """Generates valid Google JSON-LD Schema.org markup blocks."""

    @staticmethod
    def generate_article_schema(
        title: str,
        meta_description: str,
        url_slug: str,
        site_domain: str = "https://example.com",
        author_name: str = "Editorial Team"
    ) -> Dict[str, Any]:
        """Generates BlogPosting JSON-LD schema."""
        full_url = f"{site_domain.rstrip('/')}/{url_slug.lstrip('/')}"
        return {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": title,
            "description": meta_description,
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": full_url
            },
            "author": {
                "@type": "Organization",
                "name": author_name
            },
            "publisher": {
                "@type": "Organization",
                "name": author_name
            }
        }

    @staticmethod
    def generate_faq_schema(faq_items: List[Dict[str, str]]) -> Optional[Dict[str, Any]]:
        """Generates FAQPage JSON-LD schema from list of {'question': ..., 'answer': ...} items."""
        if not faq_items:
            return None

        entities = []
        for item in faq_items:
            q = item.get("question", "").strip()
            a = item.get("answer", "").strip()
            if q and a:
                entities.append({
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": a
                    }
                })

        if not entities:
            return None

        return {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": entities
        }

    @staticmethod
    def inject_schema_into_html(html_content: str, schemas: List[Dict[str, Any]]) -> str:
        """Injects JSON-LD script blocks into HTML body or head."""
        if not schemas:
            return html_content

        schema_scripts = []
        for schema in schemas:
            if schema:
                json_str = json.dumps(schema, indent=2)
                schema_scripts.append(f'<script type="application/ld+json">\n{json_str}\n</script>')

        if not schema_scripts:
            return html_content

        combined_scripts = "\n".join(schema_scripts)
        if "</head>" in html_content:
            return html_content.replace("</head>", f"{combined_scripts}\n</head>")
        else:
            return f"{combined_scripts}\n{html_content}"
