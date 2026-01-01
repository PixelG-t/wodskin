# steps/final_health.py - Final Health Step (Step 2.2)

from tkinter import filedialog, messagebox
from PIL import Image
from utils.image_ops import resize_to_64

class FinalHealthStep:
    def __init__(self, app):
        self.app = app
    
    def show(self):
        """Show final health step"""
        self.app.current_step = 4
        self.app.set_instructions(
            "Section 2.2: Final Full Health\n\n"
            "1. Upload your full health dot one more time\n"
            "2. Click SAVE to finalize and finish\n\n"
            "We'll save it at the correct 64x64 size for the game."
        )
        self.app.clear_controls()
        self.app.add_button("Upload Full Health", self.upload_final)
        self.app.add_button("SAVE & Finish", self.save_final)
        self.app.add_button("Skip to End", self.next_step)
    
    def upload_final(self):
        """Upload final full health image"""
        p = filedialog.askopenfilename(filetypes=[("PNG","*.png")])
        if p:
            self.app.full_health_image = Image.open(p).convert("RGBA")
            self.app.update_preview(self.app.full_health_image)
    
    def save_final(self):
        """Save final full health image"""
        if not self.app.full_health_image:
            self.app.show_error("Upload full health image first!")
            return
        
        if self.app.settings["confirm_before_save"]:
            if not messagebox.askyesno("Confirm", "Save this image?"):
                return
        
        default = "final_full_health.png"
        p = filedialog.asksaveasfilename(defaultextension=".png", initialfile=default,
                                         filetypes=[("PNG","*.png")])
        if p:
            result_64 = resize_to_64(self.app.full_health_image)
            result_64.save(p)
            
            if self.app.settings["auto_backup"]:
                bp = p + ".backup"
                result_64.save(bp)
            
            messagebox.showinfo("Saved", f"Full health orb saved at 64x64: {p}")
            self.next_step()
    
    def next_step(self):
        """Go to end screen"""
        from steps.end_screen import EndScreen
        self.app.current_step_handler = EndScreen(self.app)
        self.app.current_step_handler.show()
