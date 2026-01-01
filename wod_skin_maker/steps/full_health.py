# steps/full_health.py - Full Health Step (Step 1)

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

class FullHealthStep:
    def __init__(self, app):
        self.app = app
    
    def show(self):
        """Show full health step"""
        self.app.current_step = 1
        self.app.set_instructions(
            "Step 1: Load your image to create the full health orb.\n\n"
            "You can crop it to a circle, add a ring, draw, zoom,\n"
            "or transform (flip/rotate).\n"
            "Then save your image before proceeding."
        )
        self.app.clear_controls()
        self.app.add_button("Load Image", self.load_image)
        self.app.add_button("Circle Crop", self.app.circle_crop.start)
        self.app.add_button("Add Ring", self.app.ring_maker.start)
        self.app.add_button("Draw Tools", self.app.drawing_tool.start)
        self.app.add_button("Reset Zoom", self.app.transform.reset_zoom)
        
        # Transform buttons in a row
        tf = tk.Frame(self.app.control_frame, bg=self.app.PANEL)
        tf.pack(pady=5)
        tk.Button(tf, text="Flip H", command=self.app.transform.flip_horizontal, 
                 font=("Consolas", 9), bg=self.app.ACCENT, fg=self.app.BTN_TXT, 
                 activebackground=self.app.BTN_HOVER, relief="flat", width=7).pack(side="left", padx=2)
        tk.Button(tf, text="Flip V", command=self.app.transform.flip_vertical,
                 font=("Consolas", 9), bg=self.app.ACCENT, fg=self.app.BTN_TXT,
                 activebackground=self.app.BTN_HOVER, relief="flat", width=7).pack(side="left", padx=2)
        tk.Button(tf, text="Rotate 90", command=self.app.transform.rotate_90,
                 font=("Consolas", 9), bg=self.app.ACCENT, fg=self.app.BTN_TXT,
                 activebackground=self.app.BTN_HOVER, relief="flat", width=8).pack(side="left", padx=2)
        
        self.app.add_button("Save Image", self.save_image)
        self.app.add_button("Next to Step 2", self.next_step)
    
    def load_image(self):
        """Load full health image"""
        path = filedialog.askopenfilename(
            title="Select full health image",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.webp")]
        )
        if path:
            self.app.full_health_image = Image.open(path).convert("RGBA")
            self.app.full_health_saved = False
            self.app.update_preview(self.app.full_health_image)
    
    def save_image(self):
        """Save full health image"""
        if not self.app.full_health_image:
            self.app.show_error("Load or create an image first!")
            return
        
        if self.app.settings["confirm_before_save"]:
            if not messagebox.askyesno("Confirm", "Save this image?"):
                return
        
        default = "full_health.png"
        if self.app.settings["auto_name_files"]:
            self.app.auto_save_count += 1
            default = f"full_health_{self.app.auto_save_count}.png"
        
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            initialfile=default,
            filetypes=[("PNG Image", "*.png"), ("All Files", "*.*")]
        )
        
        if path:
            self.app.full_health_image.save(path)
            self.app.full_health_saved = True
            
            if self.app.settings["auto_backup"]:
                backup = path + ".backup"
                self.app.full_health_image.save(backup)
            
            messagebox.showinfo("Success", f"Image saved: {path}")
            self.show()
    
    def next_step(self):
        """Go to medium health step"""
        from steps.medium_health import MediumHealthStep
        self.app.current_step_handler = MediumHealthStep(self.app)
        self.app.current_step_handler.show()
