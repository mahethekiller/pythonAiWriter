"""
Output File History & Log Viewer.
Displays generated articles, WordPress HTML, Word docx, Markdown, and JSON payloads.
"""

import os
from pathlib import Path
import customtkinter as ctk


def build_history_view(app, parent_container):
    """Builds the History & Output Files view."""
    
    # Header Card
    header_card = ctk.CTkFrame(
        parent_container,
        fg_color="#1E293B",
        border_width=1,
        border_color="#2B3648",
        corner_radius=10
    )
    header_card.pack(fill="x", padx=12, pady=(10, 6))

    ctk.CTkLabel(
        header_card,
        text="📚 Execution History & Output Archives",
        font=ctk.CTkFont(size=16, weight="bold"),
        text_color="#38BDF8"
    ).pack(anchor="w", padx=14, pady=(10, 2))

    ctk.CTkLabel(
        header_card,
        text="Quickly access generated WordPress HTML files, Word (.docx) documents, Markdown (.md), and JSON CMS payloads.",
        font=ctk.CTkFont(size=11),
        text_color="#94A3B8"
    ).pack(anchor="w", padx=14, pady=(0, 10))

    # Folders Grid Container
    folders = [
        {"title": "📁 Dated Output Folders", "path": "output_results", "desc": "Rewriter runs organized by date & timestamp."},
        {"title": "🌐 WordPress HTML Articles", "path": "blog_articles", "desc": "Generated blog posts in semantic HTML format."},
        {"title": "📄 Word (.docx) Documents", "path": "docx_articles", "desc": "Formatted Microsoft Word document exports."},
        {"title": "📝 Markdown (.md) Articles", "path": "md_articles", "desc": "Plain Markdown articles with metadata header."},
        {"title": "⚙️ Headless CMS JSON", "path": "json_cms_payloads", "desc": "Structured API payloads ready for CMS import."}
    ]

    for f in folders:
        card = ctk.CTkFrame(
            parent_container,
            fg_color="#1E293B",
            border_width=1,
            border_color="#2B3648",
            corner_radius=10
        )
        card.pack(fill="x", padx=12, pady=5)

        sub_frame = ctk.CTkFrame(card, fg_color="transparent")
        sub_frame.pack(fill="x", padx=14, pady=10)

        left_info = ctk.CTkFrame(sub_frame, fg_color="transparent")
        left_info.pack(side="left", fill="both", expand=True)

        ctk.CTkLabel(
            left_info,
            text=f["title"],
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#FFFFFF"
        ).pack(anchor="w")

        folder_path = Path(os.getcwd()) / f["path"]
        exists_str = f"Location: ./{f['path']} ({'Exists' if folder_path.exists() else 'Not created yet'})"

        ctk.CTkLabel(
            left_info,
            text=f"{f['desc']} • {exists_str}",
            font=ctk.CTkFont(size=11),
            text_color="#94A3B8"
        ).pack(anchor="w", pady=(2, 0))

        btn = ctk.CTkButton(
            sub_frame,
            text="Open Folder",
            width=110,
            height=30,
            fg_color="#4F7CFF",
            hover_color="#3B62E6",
            command=lambda p=folder_path: _open_directory(p)
        )
        btn.pack(side="right", padx=(8, 0))


def _open_directory(target_path: Path):
    """Opens target directory in system file explorer."""
    if not target_path.exists():
        target_path.mkdir(parents=True, exist_ok=True)
    os.startfile(str(target_path))
