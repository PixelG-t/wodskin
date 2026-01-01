# ui/controls.py - UI Helper Methods

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class UIControls:
    """Base class with UI helper methods"""
    
    def clear_controls(self):
        """Clear all buttons from control frame"""
        for w in self.control_frame.winfo_children():
            w.destroy()
        self.buttons = {}
        self.control_frame.update_idletasks()
    
    def add_button(self, text, command):
        """Add a button to the control frame"""
        btn = tk.Button(self.control_frame, text=text, command=command,
                       font=("Consolas", 11), bg=self.ACCENT, fg=self.BTN_TXT,
                       activebackground=self.BTN_HOVER, relief="flat",
                       width=25, height=2)
        btn.pack(pady=5, fill="x", expand=False)
        self.buttons[text] = btn
        self.control_frame.update_idletasks()
    
    def set_instructions(self, text):
        """Set instruction label text"""
        self.instruction_label.config(text=text)
    
    def show_error(self, message):
        """Show error message box"""
        messagebox.showerror("Error", message)
    
    def show_info(self, message):
        """Show info message box"""
        messagebox.showinfo("Info", message)
    
    def update_preview(self, img):
        """Update preview canvas with image"""
        if not img:
            return
        
        cw = self.canvas.winfo_width() or 800
        ch = self.canvas.winfo_height() or 800
        
        preview = img.copy()
        preview.thumbnail((cw, ch), Image.Resampling.LANCZOS)
        
        self.preview_image = ImageTk.PhotoImage(preview)
        self.canvas.delete("all")
        self.canvas.create_image(cw//2, ch//2, image=self.preview_image)
    
    def update_canvas_preview(self, img):
        """Update canvas with already-sized image"""
        if not img:
            return
        
        cw = self.canvas.winfo_width() or 800
        ch = self.canvas.winfo_height() or 800
        
        self.preview_image = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self.canvas.create_image(cw//2, ch//2, image=self.preview_image)
