"""
Bottom Status Bar Component.
Displays real-time application state, active threads, progress bar, and system metrics.
"""

import customtkinter as ctk
from typing import Dict, Any


class StatusBarComponent(ctk.CTkFrame):
    """Bottom Status Bar Component."""

    def __init__(self, parent, theme_mgr, **kwargs):
        super().__init__(parent, fg_color=theme_mgr.colors["bg_toolbar"], height=32, corner_radius=0, **kwargs)
        
        self.theme_mgr = theme_mgr

        self._build_ui()
        self.theme_mgr.register_listener(self._on_theme_change)

    def _build_ui(self):
        """Constructs progress bar, status text, and metric pills."""
        # Left System Status
        self.status_label = ctk.CTkLabel(
            self,
            text="🟢 Ready",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=self.theme_mgr.colors["success"]
        )
        self.status_label.pack(side="left", padx=12)

        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(
            self,
            width=160,
            height=8,
            progress_color=self.theme_mgr.colors["primary"],
            fg_color=self.theme_mgr.colors["border"]
        )
        self.progress_bar.set(0.0)
        self.progress_bar.pack(side="left", padx=10)

        # Active Task Detail Label
        self.task_label = ctk.CTkLabel(
            self,
            text="Idle",
            font=ctk.CTkFont(size=11),
            text_color=self.theme_mgr.colors["text_muted"]
        )
        self.task_label.pack(side="left", padx=6)

        # Right Metrics Container
        self.right_container = ctk.CTkFrame(self, fg_color="transparent")
        self.right_container.pack(side="right", padx=12)

        # Worker Threads Indicator
        self.threads_label = ctk.CTkLabel(
            self.right_container,
            text="⚡ 3 Worker Threads",
            font=ctk.CTkFont(size=11),
            text_color=self.theme_mgr.colors["text_secondary"]
        )
        self.threads_label.pack(side="right", padx=8)

        # Memory Estimator
        self.memory_label = ctk.CTkLabel(
            self.right_container,
            text="💾 Memory: ~45 MB",
            font=ctk.CTkFont(size=11),
            text_color=self.theme_mgr.colors["text_muted"]
        )
        self.memory_label.pack(side="right", padx=8)

    def set_status(self, text: str, is_running: bool = False):
        """Updates status text and color."""
        if is_running:
            self.status_label.configure(
                text=f"⏳ {text}",
                text_color=self.theme_mgr.colors["warning"]
            )
        else:
            self.status_label.configure(
                text=f"🟢 {text}",
                text_color=self.theme_mgr.colors["success"]
            )

    def set_task(self, task_text: str):
        """Updates detail task label."""
        self.task_label.configure(text=task_text)

    def set_progress(self, val: float):
        """Sets progress bar value (0.0 to 1.0)."""
        self.progress_bar.set(max(0.0, min(1.0, val)))

    def set_threads(self, thread_count: int):
        """Updates thread count display."""
        self.threads_label.configure(text=f"⚡ {thread_count} Worker Threads")

    def _on_theme_change(self, mode: str, colors: Dict[str, str]):
        """Theme refresh callback."""
        self.configure(fg_color=colors["bg_toolbar"])
        self.status_label.configure(text_color=colors["success"])
        self.task_label.configure(text_color=colors["text_muted"])
        self.threads_label.configure(text_color=colors["text_secondary"])
        self.memory_label.configure(text_color=colors["text_muted"])
        self.progress_bar.configure(
            progress_color=colors["primary"],
            fg_color=colors["border"]
        )
