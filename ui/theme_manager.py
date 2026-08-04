"""
Centralized Theme Manager for CustomTkinter Desktop Application.
Uses CustomTkinter native ("light_color", "dark_color") tuple pairings for seamless theme switching.
"""

import customtkinter as ctk
from typing import Dict, Any, List, Callable, Tuple


class ThemeManager:
    """Manages color palettes as (light_color, dark_color) tuples for native CustomTkinter appearance switching."""

    # Tuple colors: (Light Mode Color, Dark Mode Color)
    COLOR_TOKENS: Dict[str, Tuple[str, str]] = {
        "bg_app": ("#F8FAFC", "#0E1117"),          # Soft light slate vs deep obsidian
        "bg_sidebar": ("#FFFFFF", "#0E121B"),      # Pure white sidebar vs dark sidebar
        "bg_toolbar": ("#F8FAFC", "#0E1117"),      # Light top bar vs dark top bar
        "bg_card": ("#FFFFFF", "#141923"),         # Pure white card vs dark card
        "bg_card_hover": ("#F1F5F9", "#1E2638"),   # Light hover vs dark hover
        "bg_input": ("#FFFFFF", "#0E121B"),        # White input field vs dark input field
        "border": ("#E5E7EB", "#222A3A"),          # Light border vs dark border
        "border_focus": ("#3B82F6", "#3B82F6"),    # Active focus blue border
        "primary": ("#3B82F6", "#3B82F6"),         # Vibrant primary blue
        "primary_hover": ("#2563EB", "#2563EB"),   # Primary hover blue
        "accent": ("#4F46E5", "#6366F1"),          # Secondary purple accent
        "success": ("#22C55E", "#22C55E"),         # Success gauge green
        "warning": ("#D97706", "#F59E0B"),         # Warning amber
        "danger": ("#EF4444", "#EF4444"),          # Danger red
        "text_primary": ("#111827", "#F9FAFB"),    # Dark text vs white text
        "text_secondary": ("#4B5563", "#9CA3AF"),  # Muted secondary text
        "text_muted": ("#6B7280", "#6B7280"),      # Dimmed helper text
        "text_accent": ("#2563EB", "#60A5FA"),     # Blue cyan highlight text
        "badge_bg": ("#F3F4F6", "#1E2638"),        # Pill badge background
        "step_active_bg": ("#3B82F6", "#2563EB"),  # Active wizard step circle
        "step_inactive_bg": ("#E5E7EB", "#1F2937"),# Inactive wizard step circle
    }

    def __init__(self, initial_mode: str = "Dark"):
        self.mode = initial_mode.capitalize()
        if self.mode not in ["Dark", "Light"]:
            self.mode = "Dark"
        
        self.listeners: List[Callable[[str], None]] = []
        self._apply_mode(self.mode)

    @property
    def colors(self) -> Dict[str, Tuple[str, str]]:
        """Returns theme color tokens as (Light, Dark) tuples."""
        return self.COLOR_TOKENS

    def set_mode(self, mode: str):
        """Changes the theme mode natively across all CustomTkinter widgets."""
        new_mode = mode.capitalize()
        if new_mode in ["Dark", "Light"]:
            self.mode = new_mode
            self._apply_mode(self.mode)
            for callback in self.listeners:
                try:
                    callback(self.mode)
                except Exception as e:
                    print(f"Error notifying theme listener: {e}")

    def toggle_theme(self) -> str:
        """Toggles between Dark and Light mode."""
        new_mode = "Light" if self.mode == "Dark" else "Dark"
        self.set_mode(new_mode)
        return self.mode

    def _apply_mode(self, mode: str):
        """Applies appearance mode to CustomTkinter framework natively."""
        if mode == "Light":
            ctk.set_appearance_mode("Light")
        else:
            ctk.set_appearance_mode("Dark")

    def register_listener(self, callback: Callable[[str], None]):
        """Registers a UI callback for theme changes."""
        if callback not in self.listeners:
            self.listeners.append(callback)

    def unregister_listener(self, callback: Callable[[str], None]):
        """Unregisters a UI callback."""
        if callback in self.listeners:
            self.listeners.remove(callback)
