# steps/low_health.py - Low Health Step (Step 2.1)

from tkinter import filedialog, messagebox
from PIL import Image
from utils.image_ops import apply_broken_effect, resize_to_64

class LowHealthStep:
    def __init__(self, app):
        self.app = app
    
    def show(self):
        """Show low health step"""
        self.app.current_step = 3
        self.app.set_instructions(
            "Section 2.1: Low Health Orb\n\n"
            "1. Upload your full health orb\n"
            "2. Upload a different broken dot reference\n"
            "3. (Optional) Use Eraser Tool to clean artifacts\n"
            "4. Click SAVE to continue to next step"
        )
        self.app.clear_controls()
        self.app.add_button("Upload Full Health", self.upload_full_health)
        self.app.add_button("Upload Broken Reference", self.upload_broken_reference)
        self.app.add_button("Eraser Tool", lambda: self.app.eraser_tool.start(3))
        self.app.add_button("SAVE & Continue", self.save_low)
        self.app.add_button("Skip to Next", self.next_step)
    
    def upload_full_health(self):
        """Upload full health for broken effect"""
        p = filedialog.askopenfilename(filetypes=[("PNG","*.png")])
        if p:
            self.app.full_health_image = Image.open(p).convert("RGBA")
            self.app.update_preview(self.app.full_health_image)
    
    def upload_broken_reference(self):
        """Upload low health broken dot reference"""
        p = filedialog.askopenfilename(filetypes=[("PNG","*.png")])
        if p:
            self.app.low_broken_reference = Image.open(p).convert("RGBA")
            
            if self.app.full_health_image:
                prev = apply_broken_effect(self.app.full_health_image, self.app.low_broken_reference)
                self.app.broken_effect_image = prev.copy()
                self.app.update_preview(prev)
                messagebox.showinfo("Reference loaded", 
                                  "Low health broken dot reference loaded. Preview updated!")
    
    def save_low(self):
        """Save low health image"""
        if not self.app.full_health_image or not self.app.low_broken_reference:
            self.app.show_error("Select both full health and low broken reference images!")
            return
        
        if self.app.broken_effect_image:
            result = self.app.broken_effect_image
        else:
            result = apply_broken_effect(self.app.full_health_image, self.app.low_broken_reference)
        
        self.app.update_preview(result)
        
        if self.app.settings["confirm_before_save"]:
            if not messagebox.askyesno("Confirm", "Save this image?"):
                return
        
        default = "low_health.png"
        p = filedialog.asksaveasfilename(defaultextension=".png", initialfile=default,
                                         filetypes=[("PNG","*.png")])
        if p:
            result_64 = resize_to_64(result)
            result_64.save(p)
            self.app.low_health_image = result
            
            if self.app.settings["auto_backup"]:
                bp = p + ".backup"
                result_64.save(bp)
            
            messagebox.showinfo("Saved", f"Low health orb saved at 64x64: {p}")
            self.next_step()
    
    def next_step(self):
        """Go to final health step"""
        from steps.final_health import FinalHealthStep
        self.app.current_step_handler = FinalHealthStep(self.app)
        self.app.current_step_handler.show()
