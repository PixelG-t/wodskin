# config.py - Configuration and Constants

# Colors
BG = "#1e1e1e"
PANEL = "#252526"
TEXT = "#d4d4d4"
ACCENT = "#007acc"
BTN_HOVER = "#0a84ff"
BTN_TXT = "#ffffff"

# Themes
THEMES = {
    "dark": {"bg": "#1e1e1e", "panel": "#252526", "text": "#d4d4d4", "accent": "#007acc"},
    "light": {"bg": "#ffffff", "panel": "#f0f0f0", "text": "#333333", "accent": "#0066cc"}
}

# Default settings
DEFAULT_SETTINGS = {
    "show_tips": True,
    "auto_save": False,
    "theme": "dark",
    "button_size": "medium",
    "font_size": 11,
    "canvas_zoom": 100,
    "confirm_before_save": True,
    "ring_thickness_preset": 20,
    "image_quality": "high",
    "show_grid": False,
    "auto_name_files": False,
    "show_coordinates": False,
    "recent_files_limit": 5,
    "preview_size": "large",
    "canvas_bg_color": BG,
    "animation_enabled": True,
    "undo_history_limit": 10,
    "auto_backup": True,
    "advanced_mode": False
}

# File paths
PRESETS_FILE = "ring_presets.json"

# App info
APP_VERSION = "1.2"
APP_TITLE = "WOD Skin Maker"
AUTHOR = "Wowthatp"
