# tools/ring_maker.py - Ring Maker Tool

import tkinter as tk
from tkinter import colorchooser, simpledialog, messagebox
from PIL import Image, ImageDraw
from utils.presets import save_presets

class RingMakerTool:
    def __init__(self, app):
        self.app = app
        self.ring_color = (0, 0, 0)
        self.ring_thickness = 20
        self.ring_slider = None
        self.ring_color_swatch = None
    
    def start(self):
        """Start ring maker mode"""
        if not self.app.full_health_image:
            self.app.show_error("Load an image first!")
            return
        
        self.ring_thickness = 20
        w, h = self.app.full_health_image.size
        
        self.app.set_instructions(
            "Ring Maker:\n- Pick color and adjust thickness\n- Save/Load presets\n- Click 'Done' to apply"
        )
        self.app.clear_controls()
        
        # Color picker
        cf = tk.Frame(self.app.control_frame, bg=self.app.PANEL)
        cf.pack(pady=10)
        tk.Label(cf, text="Ring Color:", font=("Consolas", 10), 
                fg=self.app.TEXT, bg=self.app.PANEL).pack(anchor="w")
        
        cbf = tk.Frame(cf, bg=self.app.PANEL)
        cbf.pack(fill="x", pady=5)
        tk.Button(cbf, text="Pick Color", command=self.pick_color,
                 font=("Consolas", 10), bg=self.app.ACCENT, fg=self.app.BTN_TXT,
                 activebackground=self.app.BTN_HOVER, relief="flat", 
                 width=12).pack(side="left", padx=2)
        
        self.ring_color_swatch = tk.Canvas(cbf, width=40, height=30, bg="#1e1e1e",
                                           highlightthickness=1, highlightbackground="#444")
        self.ring_color_swatch.pack(side="left", padx=5)
        self.update_color_swatch()
        
        # Thickness slider
        slider = tk.Scale(self.app.control_frame, from_=1, to=100, orient="horizontal",
                         label="Ring Thickness", command=self.update_preview,
                         bg=self.app.PANEL, fg=self.app.TEXT, troughcolor="#333333", 
                         highlightthickness=0)
        slider.set(self.ring_thickness)
        slider.pack(pady=10)
        self.ring_slider = slider
        
        # Presets
        pf = tk.Frame(self.app.control_frame, bg=self.app.PANEL)
        pf.pack(pady=10)
        tk.Label(pf, text="Presets:", font=("Consolas", 10), 
                fg=self.app.TEXT, bg=self.app.PANEL).pack(anchor="w")
        
        pbf = tk.Frame(pf, bg=self.app.PANEL)
        pbf.pack(fill="x", pady=5)
        tk.Button(pbf, text="Save Preset", command=self.save_preset,
                 font=("Consolas", 9), bg=self.app.ACCENT, fg=self.app.BTN_TXT,
                 activebackground=self.app.BTN_HOVER, relief="flat", 
                 width=11).pack(side="left", padx=2)
        
        if self.app.presets:
            tk.Button(pbf, text="Load Preset", command=self.load_preset,
                     font=("Consolas", 9), bg=self.app.ACCENT, fg=self.app.BTN_TXT,
                     activebackground=self.app.BTN_HOVER, relief="flat",
                     width=11).pack(side="left", padx=2)
        
        self.app.add_button("Done", self.apply)
        self.update_preview(slider.get())
    
    def pick_color(self):
        """Open color picker dialog"""
        ch = '#{:02x}{:02x}{:02x}'.format(int(self.ring_color[0]), 
                                          int(self.ring_color[1]), 
                                          int(self.ring_color[2]))
        color = colorchooser.askcolor(title="Select ring color", color=ch)[0]
        if color:
            self.ring_color = tuple(map(int, color))
            self.update_color_swatch()
            self.update_preview()
    
    def update_color_swatch(self):
        """Update the color preview swatch"""
        if not self.ring_color_swatch:
            return
        self.ring_color_swatch.delete("all")
        ch = '#{:02x}{:02x}{:02x}'.format(int(self.ring_color[0]),
                                          int(self.ring_color[1]),
                                          int(self.ring_color[2]))
        self.ring_color_swatch.config(bg=ch)
    
    def save_preset(self):
        """Save current ring settings as a preset"""
        name = simpledialog.askstring("Save Preset", "Preset name:")
        if name:
            preset = {
                "color": list(self.ring_color),
                "thickness": self.ring_thickness
            }
            self.app.presets[name] = preset
            from config import PRESETS_FILE
            save_presets(PRESETS_FILE, self.app.presets)
            messagebox.showinfo("Success", f"Preset '{name}' saved!")
    
    def load_preset(self):
        """Load a saved preset"""
        if not self.app.presets:
            messagebox.showinfo("Info", "No presets available")
            return
        
        names = list(self.app.presets.keys())
        dialog = tk.Toplevel(self.app.root)
        dialog.title("Load Preset")
        dialog.geometry("250x200")
        dialog.configure(bg=self.app.BG)
        dialog.transient(self.app.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Select Preset:", font=("Consolas", 11),
                fg=self.app.TEXT, bg=self.app.BG).pack(pady=10)
        
        pvar = tk.StringVar(value=names[0])
        dropdown = tk.OptionMenu(dialog, pvar, *names)
        dropdown.config(bg=self.app.PANEL, fg=self.app.TEXT)
        dropdown.pack(pady=10)
        
        def apply():
            n = pvar.get()
            p = self.app.presets[n]
            self.ring_color = tuple(p["color"])
            self.ring_thickness = p["thickness"]
            self.ring_slider.set(self.ring_thickness)
            self.update_color_swatch()
            self.update_preview()
            dialog.destroy()
        
        tk.Button(dialog, text="Load", command=apply,
                 font=("Consolas", 10), bg=self.app.ACCENT, fg=self.app.BTN_TXT,
                 activebackground=self.app.BTN_HOVER, relief="flat").pack(pady=10)
    
    def update_preview(self, value=None):
        """Update ring preview on canvas"""
        if value is not None:
            self.ring_thickness = int(value)
        
        if not self.app.full_health_image:
            return
        
        img = self.app.full_health_image.copy()
        w, h = img.size
        
        # Use saved circle data if available
        if (self.app.circle_crop.last_radius and 
            self.app.circle_crop.last_center_x is not None):
            sz = int(self.app.circle_crop.last_radius * 2)
            canvas = Image.new("RGBA", (sz, sz), (0, 0, 0, 0))
            
            px = int(self.app.circle_crop.last_radius - self.app.circle_crop.last_center_x)
            py = int(self.app.circle_crop.last_radius - self.app.circle_crop.last_center_y)
            canvas.paste(img, (px, py), img)
            circular = canvas
        else:
            # Fallback
            sz = min(w, h)
            left = (w - sz) // 2
            top = (h - sz) // 2
            cropped = img.crop((left, top, left + sz, top + sz))
            
            mask = Image.new("L", (sz, sz), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, sz - 1, sz - 1), fill=255)
            
            circular = Image.new("RGBA", (sz, sz))
            circular.paste(cropped, (0, 0), mask)
        
        # Add ring
        sz = circular.size[0]
        ring = Image.new("RGBA", (sz, sz), (0, 0, 0, 0))
        draw = ImageDraw.Draw(ring)
        draw.ellipse((0, 0, sz - 1, sz - 1), outline=self.ring_color, width=self.ring_thickness)
        
        result = Image.alpha_composite(circular, ring)
        self.app.update_preview(result)
    
    def apply(self):
        """Apply ring to image permanently"""
        if not self.app.full_health_image:
            return
        
        img = self.app.full_health_image.copy()
        w, h = img.size
        
        # Same logic as preview
        if (self.app.circle_crop.last_radius and 
            self.app.circle_crop.last_center_x is not None):
            sz = int(self.app.circle_crop.last_radius * 2)
            canvas = Image.new("RGBA", (sz, sz), (0, 0, 0, 0))
            
            px = int(self.app.circle_crop.last_radius - self.app.circle_crop.last_center_x)
            py = int(self.app.circle_crop.last_radius - self.app.circle_crop.last_center_y)
            canvas.paste(img, (px, py), img)
            circular = canvas
        else:
            sz = min(w, h)
            left = (w - sz) // 2
            top = (h - sz) // 2
            cropped = img.crop((left, top, left + sz, top + sz))
            
            mask = Image.new("L", (sz, sz), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, sz - 1, sz - 1), fill=255)
            
            circular = Image.new("RGBA", (sz, sz))
            circular.paste(cropped, (0, 0), mask)
        
        sz = circular.size[0]
        ring = Image.new("RGBA", (sz, sz), (0, 0, 0, 0))
        draw = ImageDraw.Draw(ring)
        draw.ellipse((0, 0, sz - 1, sz - 1), outline=self.ring_color, width=self.ring_thickness)
        
        result = Image.alpha_composite(circular, ring)
        self.app.full_health_image = result
        self.app.update_preview(result)
        
        self.app.canvas.unbind("<Motion>")
        self.app.canvas.unbind("<ButtonRelease-1>")
        self.app.current_step_handler.show()
