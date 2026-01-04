# tools/circle_crop.py - Circle Cropping Tool

import tkinter as tk
from PIL import Image, ImageDraw
from utils.image_ops import apply_circle_crop

class CircleCropTool:
    def __init__(self, app):
        self.app = app
        self.cropping_mode = False
        self.center_x = 0
        self.center_y = 0
        self.radius = 100
        self.last_radius = None
        self.last_center_x = None
        self.last_center_y = None
        self.size_slider = None
    
    def start(self):
        """Start circle cropping mode"""
        if not self.app.full_health_image:
            self.app.show_error("Load an image first!")
            return
        
        self.cropping_mode = True
        w, h = self.app.full_health_image.size
        self.center_x = w // 2
        self.center_y = h // 2
        self.radius = min(w, h) // 2 - 10
        
        self.app.set_instructions(
            "Circle Cropper:\n\n- Move circle with mouse\n- Adjust size with slider\n- Click canvas to confirm"
        )
        self.app.clear_controls()
        
        # Add slider
        tk.Label(self.app.control_frame, text="Circle Size:", 
                font=("Consolas", 10), fg=self.app.TEXT, bg=self.app.PANEL).pack()
        
        self.size_slider = tk.Scale(self.app.control_frame, from_=10, to=min(w, h)//2,
                                    orient="horizontal", command=self.update_size,
                                    bg=self.app.PANEL, fg=self.app.TEXT, 
                                    troughcolor="#333333", highlightthickness=0)
        self.size_slider.set(self.radius)
        self.size_slider.pack(pady=10, fill="x")
        
        # Bind events
        self.app.canvas.bind("<Motion>", self.on_mouse_move)
        self.app.canvas.bind("<Button-1>", self.on_canvas_click)
        
        self.show_preview()
        self.app.add_button("Cancel", self.cancel)
    
    def update_size(self, value):
        """Update circle radius from slider"""
        self.radius = int(value)
        if self.cropping_mode:
            self.show_preview()
    
    def on_mouse_move(self, event):
        """Update circle position as mouse moves"""
        if not self.cropping_mode or not self.app.full_health_image:
            return
        
        cw = self.app.canvas.winfo_width() or 800
        ch = self.app.canvas.winfo_height() or 800
        w, h = self.app.full_health_image.size
        
        # Convert canvas coords to image coords
        self.center_x = int((event.x - cw/2) * w / cw + w/2)
        self.center_y = int((event.y - ch/2) * h / ch + h/2)
        
        # Clamp to image bounds
        self.center_x = max(self.radius, min(w - self.radius, self.center_x))
        self.center_y = max(self.radius, min(h - self.radius, self.center_y))
        
        self.show_preview()
    
    def show_preview(self):
        """Show circle outline on preview"""
        if not self.app.full_health_image:
            return
        
        cw = self.app.canvas.winfo_width() or 800
        ch = self.app.canvas.winfo_height() or 800
        
        preview = self.app.full_health_image.copy()
        preview.thumbnail((cw, ch), Image.Resampling.LANCZOS)
        
        w, h = self.app.full_health_image.size
        pw, ph = preview.size
        sx = pw / w
        sy = ph / h
        
        draw = ImageDraw.Draw(preview)
        cx = int(self.center_x * sx)
        cy = int(self.center_y * sy)
        r = int(self.radius * sx)
        
        draw.ellipse((cx-r, cy-r, cx+r, cy+r), outline=(255, 255, 255), width=3)
        
        self.app.update_canvas_preview(preview)
    
    def on_canvas_click(self, event):
        """Apply circle crop when canvas is clicked"""
        if event.x > self.app.canvas.winfo_width() - 50:
            return  # Ignore clicks on slider
        self.apply()
    
    def apply(self):
        """Apply circle crop to image"""
        if not self.app.full_health_image:
            return
        
        self.cleanup()
        
        # Save circle info for ring maker
        self.last_radius = self.radius
        self.last_center_x = self.center_x
        self.last_center_y = self.center_y
        
        # Apply crop
        self.app.full_health_image = apply_circle_crop(
            self.app.full_health_image, 
            self.center_x, 
            self.center_y, 
            self.radius
        )
        
        self.app.show_info("Circle crop applied!")
        self.app.update_preview(self.app.full_health_image)
        self.app.current_step_handler.show()
    
    def cancel(self):
        """Cancel cropping"""
        self.cleanup()
        self.app.current_step_handler.show()
    
    def cleanup(self):
        """Unbind events and exit crop mode"""
        self.app.canvas.unbind("<Motion>")
        self.app.canvas.unbind("<Button-1>")
        self.cropping_mode = False
