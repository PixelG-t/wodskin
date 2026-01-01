#!/usr/bin/env python3
# main.py - WOD Skin Maker Entry Point

"""
WOD Skin Maker v1.2
Created by Wowthatp

A tool for creating custom skins for War of the Dots
"""

import tkinter as tk
from app import WODSkinMaker

if __name__ == "__main__":
    root = tk.Tk()
    app = WODSkinMaker(root)
    root.mainloop()
