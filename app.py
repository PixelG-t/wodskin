# app.py - Main Application Class

import tkinter as tk
from config import *
from ui.controls import UIControls
from ui.windows import SettingsWindow, DevMode
from tools.circle_crop import CircleCropTool
from tools.ring_maker import RingMakerTool
from tools.drawing import DrawingTool, EraserTool
from tools.transform import TransformTool
from steps.welcome import WelcomeStep
from utils.presets import load_presets
from PIL import Image

class WODSkinMaker(UIControls):
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("1200x800")
        self.root.configure(bg=BG)
        
        # Setup keyboard shortcuts
        self.setup_shortcuts()
        
        # Initialize variables
        self.init_variables()
        
        # Create UI
        self.create_ui()
        
        # Initialize tools
        self.circle_crop = CircleCropTool(self)
        self.ring_maker = RingMakerTool(self)
        self.drawing_tool = DrawingTool(self)
        self.eraser_tool = EraserTool(self)
        self.transform = TransformTool(self)
        
        # Start with welcome screen
        self.current_step_handler = WelcomeStep(self)
        self.current_step_handler.show()
    
    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        self.root.bind("<Escape>", lambda e: self.confirm_exit())
        self.root.bind("<Control-d>", lambda e: DevMode.open(self))
        self.root.bind("<Control-plus>", lambda e: self.transform.zoom_in())
        self.root.bind("<Control-equal>", lambda e: self.transform.zoom_in())
        self.root.bind("<Control-minus>", lambda e: self.transform.zoom_out())
    
    def init_variables(self):
        """Initialize all app variables"""
        self.current_step = 0
        self.current_step_handler = None
        
        # Images
        self.full_health_image = None
        self.preview_image = None
        self.medium_health_image = None
        self.low_health_image = None
        self.broken_reference = None
        self.low_broken_reference = None
        self.broken_effect_image = None
        self.full_health_saved = False
        
        # Settings
        self.settings = DEFAULT_SETTINGS.copy()
        self.presets = load_presets(PRESETS_FILE)
        self.auto_save_count = 0
        
        # Import config constants
        self.BG = BG
        self.PANEL = PANEL
        self.TEXT = TEXT
        self.ACCENT = ACCENT
        self.BTN_HOVER = BTN_HOVER
        self.BTN_TXT = BTN_TXT
    
    def create_ui(self):
        """Create main UI layout"""
        # Left frame (canvas)
        self.left_frame = tk.Frame(self.root, bg=BG)
        self.left_frame.pack(side="left", fill="both", expand=True)
        
        # Right frame (controls)
        self.right_frame = tk.Frame(self.root, width=350, bg=PANEL)
        self.right_frame.pack(side="right", fill="y")
        
        # Canvas
        self.canvas = tk.Canvas(self.left_frame, bg=BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Header
        self.header = tk.Label(self.right_frame, text=APP_TITLE, 
                               font=("Consolas", 16, "bold"), fg=ACCENT, bg=PANEL)
        self.header.pack(pady=20)
        
        # Instructions
        self.instruction_label = tk.Label(self.right_frame, text="", justify="left",
                                          font=("Consolas", 11), fg=TEXT, bg=PANEL, 
                                          wraplength=330)
        self.instruction_label.pack(pady=10)
        
        # Control frame
        self.control_frame = tk.Frame(self.right_frame, bg=PANEL)
        self.control_frame.pack(pady=20, fill="both", expand=True)
        
        self.buttons = {}
    
    def confirm_exit(self):
        """Confirm before exiting"""
        from tkinter import messagebox
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.destroy()
    
    def open_settings(self):
        """Open settings window"""
        SettingsWindow.open(self)
    
    def upd_setting(self, key, val):
        """Update a setting and apply if needed"""
        self.settings[key] = val
        
        # Apply some settings immediately
        if key == "theme":
            self.apply_theme(val)
        elif key == "button_size":
            widths = {"small": 15, "medium": 25, "large": 35}
            for btn in self.buttons.values():
                btn.config(width=widths.get(val, 25))
        elif key == "font_size":
            self.apply_font_size(val)
        elif key == "canvas_zoom":
            if self.full_health_image:
                self.update_preview(self.full_health_image)
        elif key == "ring_thickness_preset":
            self.ring_maker.ring_thickness = val
        elif key == "preview_size":
            sizes = {"small": 300, "medium": 600, "large": 800}
            self.canvas.config(height=sizes.get(val, 600))
    
    def apply_font_size(self, sz):
        """Apply font size to all UI elements"""
        self.header.config(font=("Consolas", sz + 5, "bold"))
        self.instruction_label.config(font=("Consolas", sz))
        for btn in self.buttons.values():
            btn.config(font=("Consolas", sz))
    
    def apply_all_settings(self):
        """Apply all settings"""
        from tkinter import messagebox
        fsz = self.settings["font_size"]
        self.apply_font_size(fsz)
        messagebox.showinfo("Settings Applied", "All settings have been applied successfully!")
    
    def apply_theme(self, theme_name):
        """Apply color theme"""
        if theme_name not in THEMES:
            return
        
        t = THEMES[theme_name]
        self.root.configure(bg=t["bg"])
        self.left_frame.configure(bg=t["bg"])
        self.right_frame.configure(bg=t["panel"])
        self.canvas.configure(bg=t["bg"])
        self.header.configure(bg=t["panel"], fg=t["accent"])
        self.instruction_label.configure(bg=t["panel"], fg=t["text"])
        self.control_frame.configure(bg=t["panel"])
        
        for btn in self.buttons.values():
            btn.configure(bg=t["accent"], fg="#ffffff")
        
        # Update config values
        self.BG = t["bg"]
        self.PANEL = t["panel"]
        self.TEXT = t["text"]
        self.ACCENT = t["accent"]
