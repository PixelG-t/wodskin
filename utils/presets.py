# utils/presets.py - Preset management utilities

import json
import os
from tkinter import messagebox

def load_presets(filename):
    """Load ring presets from JSON file"""
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading presets: {e}")
    return {}

def save_presets(filename, presets):
    """Save ring presets to JSON file"""
    try:
        with open(filename, 'w') as f:
            json.dump(presets, f, indent=2)
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Could not save presets: {e}")
        return False
