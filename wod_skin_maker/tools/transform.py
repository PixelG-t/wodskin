# tools/transform.py - Transform Tools (Flip, Rotate, Zoom)

from PIL import Image
from utils.image_ops import flip_image, rotate_image

class TransformTool:
    def __init__(self, app):
        self.app = app
        self.zoom_level = 1.0
    
    def flip_horizontal(self):
        """Flip image horizontally"""
        if not self.app.full_health_image:
            self.app.show_error("Load an image first!")
            return
        
        self.app.full_health_image = flip_image(self.app.full_health_image, "horizontal")
        self.zoom_level = 1.0
        self.app.update_preview(self.app.full_health_image)
        self.app.show_info("Image flipped horizontally!")
    
    def flip_vertical(self):
        """Flip image vertically"""
        if not self.app.full_health_image:
            self.app.show_error("Load an image first!")
            return
        
        self.app.full_health_image = flip_image(self.app.full_health_image, "vertical")
        self.zoom_level = 1.0
        self.app.update_preview(self.app.full_health_image)
        self.app.show_info("Image flipped vertically!")
    
    def rotate_90(self):
        """Rotate image 90 degrees"""
        if not self.app.full_health_image:
            self.app.show_error("Load an image first!")
            return
        
        self.app.full_health_image = rotate_image(self.app.full_health_image, 90)
        self.zoom_level = 1.0
        self.app.update_preview(self.app.full_health_image)
        self.app.show_info("Image rotated 90 degrees!")
    
    def zoom_in(self):
        """Zoom in on canvas"""
        if not self.app.full_health_image:
            return
        self.zoom_level = min(self.zoom_level + 0.2, 3.0)
        self.apply_zoom()
    
    def zoom_out(self):
        """Zoom out on canvas"""
        if not self.app.full_health_image:
            return
        self.zoom_level = max(self.zoom_level - 0.2, 0.5)
        self.apply_zoom()
    
    def reset_zoom(self):
        """Reset zoom to 1.0"""
        self.zoom_level = 1.0
        self.app.update_preview(self.app.full_health_image)
    
    def apply_zoom(self):
        """Apply current zoom level to preview"""
        if not self.app.full_health_image:
            return
        
        img = self.app.full_health_image.copy()
        cw = self.app.canvas.winfo_width() or 800
        ch = self.app.canvas.winfo_height() or 800
        
        new_sz = int(min(cw, ch) * self.zoom_level)
        img.thumbnail((new_sz, new_sz), Image.Resampling.LANCZOS)
        
        self.app.update_canvas_preview(img)
