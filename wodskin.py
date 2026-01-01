import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser, simpledialog
from PIL import Image, ImageTk, ImageDraw, ImageOps
import os
import json

# Colors - changed these a few times
BG = "#1e1e1e"
PANEL = "#252526"
TEXT = "#d4d4d4"
ACCENT = "#007acc"
BTN_HOVER = "#0a84ff"
BTN_TXT = "#ffffff"

class WODSkinMaker:
    def __init__(self, root):
        self.root = root
        self.root.title("WOD Skin Maker")
        self.root.geometry("1200x800")
        self.root.configure(bg=BG)
        
        # keyboard shortcuts
        self.root.bind("<Escape>", lambda e: self.confirm_exit())
        self.root.bind("<Control-d>", lambda e: self.open_dev_mode())
        self.root.bind("<Control-plus>", lambda e: self.zoom_in())
        self.root.bind("<Control-equal>", lambda e: self.zoom_in())
        self.root.bind("<Control-minus>", lambda e: self.zoom_out())
        
        # main vars
        self.current_step = 0
        self.full_health_image = None
        self.preview_image = None
        self.medium_health_image = None
        self.low_health_image = None
        self.broken_reference = None
        self.low_broken_reference = None
        
        # ring stuff
        self.ring_color = (0,0,0)
        self.ring_thickness = 20
        self.ring_center = [0,0]
        self.ring_color_preview = None
        self.full_health_saved = False
        
        # load presets
        self.presets_file = "ring_presets.json"
        self.presets = self.load_presets()
        
        # drawing
        self.zoom_level = 1.0
        self.drawing_enabled = False
        self.drawing_tool = "brush"
        self.brush_size = 5
        self.last_draw_pos = None
        
        # circle crop vars
        self.circle_center_x = 0
        self.circle_center_y = 0
        self.circle_radius = 100
        self.cropping_mode = False
        self.last_circle_radius = None
        self.last_circle_center_x = None
        self.last_circle_center_y = None
        
        # eraser
        self.eraser_enabled = False
        self.eraser_size = 15
        self.broken_effect_image = None
        self.last_eraser_pos = None
        
        # UI setup
        self.left_frame = tk.Frame(root, bg=BG)
        self.left_frame.pack(side="left", fill="both", expand=True)
        
        self.right_frame = tk.Frame(root, width=350, bg=PANEL)
        self.right_frame.pack(side="right", fill="y")
        
        # canvas for preview
        self.canvas = tk.Canvas(self.left_frame, bg=BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # right side stuff
        self.header = tk.Label(self.right_frame, text="WOD Skin Maker", 
                               font=("Consolas", 16, "bold"), fg=ACCENT, bg=PANEL)
        self.header.pack(pady=20)
        
        self.instruction_label = tk.Label(self.right_frame, text="", justify="left",
                                          font=("Consolas", 11), fg=TEXT, bg=PANEL, 
                                          wraplength=330)
        self.instruction_label.pack(pady=10)
        
        self.control_frame = tk.Frame(self.right_frame, bg=PANEL)
        self.control_frame.pack(pady=20, fill="both", expand=True)
        
        self.buttons = {}
        
        # Settings dict - TODO: save to file?
        self.settings = {
            "show_tips": True,
            "auto_save": False,
            "theme": "dark",
            "button_size": "medium",
            "font_size": 11,
            "canvas_zoom": 100,
            "confirm_before_save": True,
            "ring_thickness_preset": 20,
            "image_quality": "high",
            "show_grid": False,
            "auto_name_files": False,
            "show_coordinates": False,
            "recent_files_limit": 5,
            "preview_size": "large",
            "canvas_bg_color": BG,
            "animation_enabled": True,
            "undo_history_limit": 10,
            "auto_backup": True,
            "advanced_mode": False
        }
        
        self.themes = {
            "dark": {"bg": "#1e1e1e", "panel": "#252526", "text": "#d4d4d4", "accent": "#007acc"},
            "light": {"bg": "#ffffff", "panel": "#f0f0f0", "text": "#333333", "accent": "#0066cc"}
        }
        
        self.auto_save_count = 0
        
        # start
        self.step_0()
    
    def confirm_exit(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.destroy()
    
    # welcome screen
    def step_0(self):
        self.current_step = 0
        self.instruction_label.config(
            text="Welcome to WOD Skin Maker! (Version 1.2)\n\n"
                 "⚠️ Important: All files must be 256x256 - we size them down later.\n\n"
                 "Naming rules for your skin:\n"
                 "- Infantry full health: if_NAMEOFSKIN\n"
                 "- Infantry medium health: if2_NAMEOFSKIN\n"
                 "- Infantry low health: if3_NAMEOFSKIN\n"
                 "- Tank full health: tank1_NAMEOFSKIN\n"
                 "- Tank medium health: tank2_NAMEOFSKIN\n"
                 "- Tank low health: tank3_NAMEOFSKIN\n\n"
                 "Run this program twice: once for Infantry, once for Tank.\n\n"
                 "Click 'Next' to start creating your full health orb."
        )
        self.clear_controls()
        self.add_button("Next", self.step_full_health)
        self.add_button("Settings", self.open_settings)
    
    # Step 1: Full Health Orb
    def step_full_health(self):
        self.current_step = 1
        self.instruction_label.config(
            text="Step 1: Load your image to create the full health orb.\n\n"
                 "You can crop it to a circle, add a ring, draw, zoom,\n"
                 "or transform (flip/rotate).\n"
                 "Then save your image before proceeding."
        )
        self.clear_controls()
        self.add_button("Load Image", self.load_full_health_image)
        self.add_button("Circle Crop", self.circle_cropper)
        self.add_button("Add Ring", self.ring_maker_mode)
        self.add_button("Draw Tools", self.open_draw_tools)
        self.add_button("Reset Zoom", self.reset_zoom)
        
        # transform buttons in a row
        tf = tk.Frame(self.control_frame, bg=PANEL)
        tf.pack(pady=5)
        tk.Button(tf, text="Flip H", command=self.flip_horizontal, 
                 font=("Consolas", 9), bg=ACCENT, fg=BTN_TXT, 
                 activebackground=BTN_HOVER, relief="flat", width=7).pack(side="left", padx=2)
        tk.Button(tf, text="Flip V", command=self.flip_vertical,
                 font=("Consolas", 9), bg=ACCENT, fg=BTN_TXT,
                 activebackground=BTN_HOVER, relief="flat", width=7).pack(side="left", padx=2)
        tk.Button(tf, text="Rotate 90", command=self.rotate_90,
                 font=("Consolas", 9), bg=ACCENT, fg=BTN_TXT,
                 activebackground=BTN_HOVER, relief="flat", width=8).pack(side="left", padx=2)
        
        self.add_button("Save Image", self.save_full_health_image)
        self.add_button("Next to Step 2", self.step_section2)
    
    def load_full_health_image(self):
        path = filedialog.askopenfilename(
            title="Select full health image",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.webp")]
        )
        if path:
            self.full_health_image = Image.open(path).convert("RGBA")
            self.full_health_saved = False
            self.update_preview(self.full_health_image)
    
    def save_full_health_image(self):
        if not self.full_health_image:
            messagebox.showerror("Error", "Load or create an image first!")
            return
        
        if self.settings["confirm_before_save"]:
            if not messagebox.askyesno("Confirm", "Save this image?"):
                return
        
        default = "full_health.png"
        if self.settings["auto_name_files"]:
            self.auto_save_count += 1
            default = f"full_health_{self.auto_save_count}.png"
        
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            initialfile=default,
            filetypes=[("PNG Image", "*.png"), ("All Files", "*.*")]
        )
        
        if path:
            self.full_health_image.save(path)
            self.full_health_saved = True
            
            if self.settings["auto_backup"]:
                backup = path + ".backup"
                self.full_health_image.save(backup)
            
            messagebox.showinfo("Success", f"Image saved: {path}")
            self.step_full_health()
    
    def update_preview(self, img):
        if not img:
            return
        
        cw = self.canvas.winfo_width() or 800
        ch = self.canvas.winfo_height() or 800
        
        preview = img.copy()
        preview.thumbnail((cw, ch), Image.Resampling.LANCZOS)
        
        self.preview_image = ImageTk.PhotoImage(preview)
        self.canvas.delete("all")
        self.canvas.create_image(cw//2, ch//2, image=self.preview_image)
    
    # Circle Cropper
    def circle_cropper(self):
        if not self.full_health_image:
            messagebox.showerror("Error", "Load an image first!")
            return
        
        self.cropping_mode = True
        w, h = self.full_health_image.size
        self.circle_center_x = w // 2
        self.circle_center_y = h // 2
        self.circle_radius = min(w, h) // 2 - 10
        
        self.instruction_label.config(
            text="Circle Cropper:\n\n- Move circle with mouse\n- Adjust size with slider\n- Click canvas to confirm"
        )
        self.clear_controls()
        
        tk.Label(self.control_frame, text="Circle Size:", 
                font=("Consolas", 10), fg=TEXT, bg=PANEL).pack()
        
        self.size_slider = tk.Scale(self.control_frame, from_=10, to=min(w, h)//2,
                                    orient="horizontal", command=self.update_circle_size,
                                    bg=PANEL, fg=TEXT, troughcolor="#333333", 
                                    highlightthickness=0)
        self.size_slider.set(self.circle_radius)
        self.size_slider.pack(pady=10, fill="x")
        
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<Button-1>", lambda e: self.on_canvas_click(e))
        
        self.show_circle_preview()
        self.add_button("Cancel", self.cancel_cropping)
    
    def on_mouse_move(self, event):
        if not self.cropping_mode or not self.full_health_image:
            return
        
        cw = self.canvas.winfo_width() or 800
        ch = self.canvas.winfo_height() or 800
        w, h = self.full_health_image.size
        
        # convert coords
        self.circle_center_x = int((event.x - cw/2) * w / cw + w/2)
        self.circle_center_y = int((event.y - ch/2) * h / ch + h/2)
        
        # clamp
        self.circle_center_x = max(self.circle_radius, 
                                   min(w - self.circle_radius, self.circle_center_x))
        self.circle_center_y = max(self.circle_radius,
                                   min(h - self.circle_radius, self.circle_center_y))
        
        self.show_circle_preview()
    
    def update_circle_size(self, value):
        self.circle_radius = int(value)
        if self.cropping_mode:
            self.show_circle_preview()
    
    def show_circle_preview(self):
        if not self.full_health_image:
            return
        
        cw = self.canvas.winfo_width() or 800
        ch = self.canvas.winfo_height() or 800
        
        preview = self.full_health_image.copy()
        preview.thumbnail((cw, ch), Image.Resampling.LANCZOS)
        
        w, h = self.full_health_image.size
        pw, ph = preview.size
        sx = pw / w
        sy = ph / h
        
        draw = ImageDraw.Draw(preview)
        cx = int(self.circle_center_x * sx)
        cy = int(self.circle_center_y * sy)
        r = int(self.circle_radius * sx)
        
        draw.ellipse((cx-r, cy-r, cx+r, cy+r), outline=(255, 255, 255), width=3)
        
        self.preview_image = ImageTk.PhotoImage(preview)
        self.canvas.delete("all")
        self.canvas.create_image(cw//2, ch//2, image=self.preview_image)
    
    def on_canvas_click(self, event):
        # ignore clicks on right edge (slider area)
        if event.x > self.canvas.winfo_width() - 50:
            return
        self.apply_circle_crop()
    
    def apply_circle_crop(self):
        if not self.full_health_image:
            return
        
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<Button-1>")
        self.cropping_mode = False
        
        # save circle info for ring maker
        self.last_circle_radius = self.circle_radius
        self.last_circle_center_x = self.circle_center_x
        self.last_circle_center_y = self.circle_center_y
        
        w, h = self.full_health_image.size
        mask = Image.new("L", (w, h), 0)
        draw = ImageDraw.Draw(mask)
        
        x1 = self.circle_center_x - self.circle_radius
        y1 = self.circle_center_y - self.circle_radius
        x2 = self.circle_center_x + self.circle_radius
        y2 = self.circle_center_y + self.circle_radius
        
        draw.ellipse((x1, y1, x2, y2), fill=255)
        
        cropped = Image.new("RGBA", (w, h))
        cropped.paste(self.full_health_image, (0, 0), mask)
        self.full_health_image = cropped
        
        messagebox.showinfo("Done", "Circle crop applied!")
        self.update_preview(cropped)
        self.step_full_health()
    
    def cancel_cropping(self):
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<Button-1>")
        self.cropping_mode = False
        self.step_full_health()
    
    # Ring Maker
    def ring_maker_mode(self):
        if not self.full_health_image:
            messagebox.showerror("Error", "Load an image first!")
            return
        
        self.ring_thickness = 20
        w, h = self.full_health_image.size
        self.ring_center = [w//2, h//2]
        
        self.instruction_label.config(
            text="Ring Maker:\n- Pick color and adjust thickness\n- Save/Load presets\n- Click 'Done' to apply"
        )
        self.clear_controls()
        
        # color picker
        cf = tk.Frame(self.control_frame, bg=PANEL)
        cf.pack(pady=10)
        tk.Label(cf, text="Ring Color:", font=("Consolas", 10), 
                fg=TEXT, bg=PANEL).pack(anchor="w")
        
        cbf = tk.Frame(cf, bg=PANEL)
        cbf.pack(fill="x", pady=5)
        tk.Button(cbf, text="Pick Color", command=self.pick_ring_color,
                 font=("Consolas", 10), bg=ACCENT, fg=BTN_TXT,
                 activebackground=BTN_HOVER, relief="flat", 
                 width=12).pack(side="left", padx=2)
        
        self.ring_color_swatch = tk.Canvas(cbf, width=40, height=30, bg="#1e1e1e",
                                           highlightthickness=1, highlightbackground="#444")
        self.ring_color_swatch.pack(side="left", padx=5)
        self.update_color_swatch()
        
        # thickness slider
        slider = tk.Scale(self.control_frame, from_=1, to=100, orient="horizontal",
                         label="Ring Thickness", command=self.update_ring_preview,
                         bg=PANEL, fg=TEXT, troughcolor="#333333", highlightthickness=0)
        slider.set(self.ring_thickness)
        slider.pack(pady=10)
        self.ring_slider = slider
        
        # presets
        pf = tk.Frame(self.control_frame, bg=PANEL)
        pf.pack(pady=10)
        tk.Label(pf, text="Presets:", font=("Consolas", 10), 
                fg=TEXT, bg=PANEL).pack(anchor="w")
        
        pbf = tk.Frame(pf, bg=PANEL)
        pbf.pack(fill="x", pady=5)
        tk.Button(pbf, text="Save Preset", command=self.save_ring_preset,
                 font=("Consolas", 9), bg=ACCENT, fg=BTN_TXT,
                 activebackground=BTN_HOVER, relief="flat", 
                 width=11).pack(side="left", padx=2)
        
        if self.presets:
            tk.Button(pbf, text="Load Preset", command=self.load_ring_preset,
                     font=("Consolas", 9), bg=ACCENT, fg=BTN_TXT,
                     activebackground=BTN_HOVER, relief="flat",
                     width=11).pack(side="left", padx=2)
        
        self.add_button("Done", self.apply_ring)
        self.update_ring_preview(slider.get())
    
    def pick_ring_color(self):
        ch = '#{:02x}{:02x}{:02x}'.format(int(self.ring_color[0]), 
                                          int(self.ring_color[1]), 
                                          int(self.ring_color[2]))
        color = colorchooser.askcolor(title="Select ring color", color=ch)[0]
        if color:
            self.ring_color = tuple(map(int, color))
            self.update_color_swatch()
            self.update_ring_preview()
    
    def update_color_swatch(self):
        self.ring_color_swatch.delete("all")
        ch = '#{:02x}{:02x}{:02x}'.format(int(self.ring_color[0]),
                                          int(self.ring_color[1]),
                                          int(self.ring_color[2]))
        self.ring_color_swatch.config(bg=ch)
    
    def save_ring_preset(self):
        name = simpledialog.askstring("Save Preset", "Preset name:")
        if name:
            preset = {
                "color": list(self.ring_color),
                "thickness": self.ring_thickness
            }
            self.presets[name] = preset
            self.save_presets_to_file()
            messagebox.showinfo("Success", f"Preset '{name}' saved!")
    
    def load_ring_preset(self):
        if not self.presets:
            messagebox.showinfo("Info", "No presets available")
            return
        
        names = list(self.presets.keys())
        dialog = tk.Toplevel(self.root)
        dialog.title("Load Preset")
        dialog.geometry("250x200")
        dialog.configure(bg=BG)
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Select Preset:", font=("Consolas", 11),
                fg=TEXT, bg=BG).pack(pady=10)
        
        pvar = tk.StringVar(value=names[0])
        dropdown = tk.OptionMenu(dialog, pvar, *names)
        dropdown.config(bg=PANEL, fg=TEXT)
        dropdown.pack(pady=10)
        
        def apply():
            n = pvar.get()
            p = self.presets[n]
            self.ring_color = tuple(p["color"])
            self.ring_thickness = p["thickness"]
            self.ring_slider.set(self.ring_thickness)
            self.update_color_swatch()
            self.update_ring_preview()
            dialog.destroy()
        
        tk.Button(dialog, text="Load", command=apply,
                 font=("Consolas", 10), bg=ACCENT, fg=BTN_TXT,
                 activebackground=BTN_HOVER, relief="flat").pack(pady=10)
    
    def load_presets(self):
        try:
            if os.path.exists(self.presets_file):
                with open(self.presets_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {}
    
    def save_presets_to_file(self):
        try:
            with open(self.presets_file, 'w') as f:
                json.dump(self.presets, f, indent=2)
        except:
            messagebox.showerror("Error", "Could not save presets")
    
    # Drawing Tools
    def open_draw_tools(self):
        if not self.full_health_image:
            messagebox.showerror("Error", "Load an image first!")
            return
        
        self.drawing_enabled = True
        self.instruction_label.config(
            text="Drawing Mode:\n- Left-click to draw/erase\n- Adjust brush size\n- Select tool and click Done"
        )
        self.clear_controls()
        
        tk.Label(self.control_frame, text="Tool:", font=("Consolas", 10),
                fg=TEXT, bg=PANEL).pack()
        
        tool_var = tk.StringVar(value="brush")
        tk.Radiobutton(self.control_frame, text="Brush (Draw)", variable=tool_var,
                      value="brush", command=lambda: setattr(self, 'drawing_tool', 'brush'),
                      bg=PANEL, fg=TEXT, selectcolor=PANEL).pack(anchor="w")
        tk.Radiobutton(self.control_frame, text="Eraser", variable=tool_var,
                      value="eraser", command=lambda: setattr(self, 'drawing_tool', 'eraser'),
                      bg=PANEL, fg=TEXT, selectcolor=PANEL).pack(anchor="w")
        
        tk.Label(self.control_frame, text="Brush Size:", font=("Consolas", 10),
                fg=TEXT, bg=PANEL).pack(pady=(10,5))
        
        ss = tk.Scale(self.control_frame, from_=1, to=30, orient="horizontal",
                     command=lambda v: setattr(self, 'brush_size', int(v)),
                     bg=PANEL, fg=TEXT, troughcolor="#333333", highlightthickness=0)
        ss.set(5)
        ss.pack(pady=5)
        
        self.canvas.bind("<B1-Motion>", self.draw_on_canvas)
        self.canvas.bind("<Button-1>", self.draw_on_canvas)
        
        self.add_button("Done", self.finish_drawing)
    
    def draw_on_canvas(self, event):
        if not self.full_health_image or not self.drawing_enabled:
            return
        
        cw = self.canvas.winfo_width() or 800
        ch = self.canvas.winfo_height() or 800
        iw, ih = self.full_health_image.size
        
        x = int((event.x - cw/2) * iw / cw + iw/2)
        y = int((event.y - ch/2) * ih / ch + ih/2)
        
        if 0 <= x < iw and 0 <= y < ih:
            draw = ImageDraw.Draw(self.full_health_image)
            sz = self.brush_size
            
            if self.drawing_tool == "brush":
                draw.ellipse([x-sz, y-sz, x+sz, y+sz], fill=(0,0,0,255))
            else:
                draw.ellipse([x-sz, y-sz, x+sz, y+sz], fill=(0,0,0,0))
            
            self.update_preview(self.full_health_image)
    
    def finish_drawing(self):
        self.drawing_enabled = False
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<Button-1>")
        self.step_full_health()
    
    # Zoom
    def zoom_in(self):
        if not self.full_health_image:
            return
        self.zoom_level = min(self.zoom_level + 0.2, 3.0)
        self.apply_zoom()
    
    def zoom_out(self):
        if not self.full_health_image:
            return
        self.zoom_level = max(self.zoom_level - 0.2, 0.5)
        self.apply_zoom()
    
    def reset_zoom(self):
        self.zoom_level = 1.0
        self.update_preview(self.full_health_image)
    
    def apply_zoom(self):
        if not self.full_health_image:
            return
        
        img = self.full_health_image.copy()
        cw = self.canvas.winfo_width() or 800
        ch = self.canvas.winfo_height() or 800
        
        new_sz = int(min(cw, ch) * self.zoom_level)
        img.thumbnail((new_sz, new_sz), Image.Resampling.LANCZOS)
        
        self.preview_image = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self.canvas.create_image(cw//2, ch//2, image=self.preview_image)
    
    # Flip & Rotate
    def flip_horizontal(self):
        if not self.full_health_image:
            messagebox.showerror("Error", "Load an image first!")
            return
        
        self.full_health_image = self.full_health_image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        self.zoom_level = 1.0
        self.update_preview(self.full_health_image)
        messagebox.showinfo("Done", "Image flipped horizontally!")
    
    def flip_vertical(self):
        if not self.full_health_image:
            messagebox.showerror("Error", "Load an image first!")
            return
        
        self.full_health_image = self.full_health_image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        self.zoom_level = 1.0
        self.update_preview(self.full_health_image)
        messagebox.showinfo("Done", "Image flipped vertically!")
    
    def rotate_90(self):
        if not self.full_health_image:
            messagebox.showerror("Error", "Load an image first!")
            return
        
        self.full_health_image = self.full_health_image.rotate(90, expand=False)
        self.zoom_level = 1.0
        self.update_preview(self.full_health_image)
        messagebox.showinfo("Done", "Image rotated 90 degrees!")
    
    def update_ring_preview(self, value=None):
        if value is not None:
            self.ring_thickness = int(value)
        
        if not self.full_health_image:
            return
        
        img = self.full_health_image.copy()
        w, h = img.size
        
        # use saved circle data if we have it
        if (self.last_circle_radius and self.last_circle_center_x is not None):
            sz = int(self.last_circle_radius * 2)
            canvas = Image.new("RGBA", (sz, sz), (0, 0, 0, 0))
            
            px = int(self.last_circle_radius - self.last_circle_center_x)
            py = int(self.last_circle_radius - self.last_circle_center_y)
            canvas.paste(img, (px, py), img)
            circular = canvas
        else:
            # fallback
            sz = min(w, h)
            left = (w - sz) // 2
            top = (h - sz) // 2
            cropped = img.crop((left, top, left + sz, top + sz))
            
            mask = Image.new("L", (sz, sz), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, sz - 1, sz - 1), fill=255)
            
            circular = Image.new("RGBA", (sz, sz))
            circular.paste(cropped, (0, 0), mask)
        
        # add ring
        sz = circular.size[0]
        ring = Image.new("RGBA", (sz, sz), (0, 0, 0, 0))
        draw = ImageDraw.Draw(ring)
        draw.ellipse((0, 0, sz - 1, sz - 1), outline=self.ring_color, width=self.ring_thickness)
        
        result = Image.alpha_composite(circular, ring)
        self.update_preview(result)
    
    def drag_ring(self, event):
        pass  # not used anymore
    
    def apply_ring(self):
        if not self.full_health_image:
            return
        
        img = self.full_health_image.copy()
        w, h = img.size
        
        # same logic as preview
        if (self.last_circle_radius and self.last_circle_center_x is not None):
            sz = int(self.last_circle_radius * 2)
            canvas = Image.new("RGBA", (sz, sz), (0, 0, 0, 0))
            
            px = int(self.last_circle_radius - self.last_circle_center_x)
            py = int(self.last_circle_radius - self.last_circle_center_y)
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
        self.full_health_image = result
        self.update_preview(result)
        
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.step_full_health()
    
    # Section 2: Medium Health
    def step_section2(self):
        self.current_step = 2
        self.instruction_label.config(
            text="Section 2: Medium Health Orb\n\n"
                 "1. Upload your full health orb\n"
                 "2. Upload a broken dot reference\n"
                 "3. (Optional) Use Eraser Tool to clean artifacts\n"
                 "4. Click SAVE to continue to next step"
        )
        self.clear_controls()
        self.add_button("Upload Full Health", self.upload_full_health_for_broken)
        self.add_button("Upload Broken Reference", self.upload_broken_reference)
        self.add_button("Eraser Tool", self.start_eraser_medium)
        self.add_button("SAVE & Continue", self.save_medium_health)
        self.add_button("Skip to Next", self.step_section2_1)
    
    def upload_full_health_for_broken(self):
        p = filedialog.askopenfilename(filetypes=[("PNG","*.png")])
        if p:
            self.full_health_image = Image.open(p).convert("RGBA")
            self.update_preview(self.full_health_image)
    
    def upload_broken_reference(self):
        p = filedialog.askopenfilename(filetypes=[("PNG","*.png")])
        if p:
            self.broken_reference = Image.open(p).convert("RGBA")
            
            if self.full_health_image:
                prev = self.apply_broken_effect(self.full_health_image, self.broken_reference)
                self.broken_effect_image = prev.copy()
                self.update_preview(prev)
                messagebox.showinfo("Reference loaded", "Broken dot reference loaded. Preview updated!")
    
    def apply_broken_effect(self, full, broken_ref):
        br_resized = broken_ref.resize(full.size, Image.Resampling.LANCZOS)
        mask = br_resized.split()[3]  # alpha
        result = full.copy()
        result.putalpha(mask)
        return result
    
    def save_medium_health(self):
        if not self.full_health_image or not self.broken_reference:
            messagebox.showerror("Error", "Select both full health and broken reference images!")
            return
        
        if self.broken_effect_image:
            result = self.broken_effect_image
        else:
            result = self.apply_broken_effect(self.full_health_image, self.broken_reference)
        
        self.update_preview(result)
        
        if self.settings["confirm_before_save"]:
            if not messagebox.askyesno("Confirm", "Save this image?"):
                return
        
        default = "medium_health.png"
        p = filedialog.asksaveasfilename(defaultextension=".png", initialfile=default,
                                         filetypes=[("PNG","*.png")])
        if p:
            result_64 = result.resize((64, 64), Image.Resampling.LANCZOS)
            result_64.save(p)
            self.medium_health_image = result
            
            if self.settings["auto_backup"]:
                bp = p + ".backup"
                result_64.save(bp)
            
            messagebox.showinfo("Saved", f"Medium health orb saved at 64x64: {p}")
            self.step_section2_1()
    
    # Section 2.1: Low Health
    def step_section2_1(self):
        self.current_step = 3
        self.instruction_label.config(
            text="Section 2.1: Low Health Orb\n\n"
                 "1. Upload your full health orb\n"
                 "2. Upload a different broken dot reference\n"
                 "3. (Optional) Use Eraser Tool to clean artifacts\n"
                 "4. Click SAVE to continue to next step"
        )
        self.clear_controls()
        self.add_button("Upload Full Health", self.upload_full_health_for_broken_low)
        self.add_button("Upload Broken Reference", self.upload_low_broken_reference)
        self.add_button("Eraser Tool", self.start_eraser_low)
        self.add_button("SAVE & Continue", self.save_low_health)
        self.add_button("Skip to Next", self.step_section2_2)
    
    def upload_full_health_for_broken_low(self):
        self.upload_full_health_for_broken()
    
    def upload_low_broken_reference(self):
        p = filedialog.askopenfilename(filetypes=[("PNG","*.png")])
        if p:
            self.low_broken_reference = Image.open(p).convert("RGBA")
            
            if self.full_health_image:
                prev = self.apply_broken_effect(self.full_health_image, self.low_broken_reference)
                self.broken_effect_image = prev.copy()
                self.update_preview(prev)
                messagebox.showinfo("Reference loaded", 
                                  "Low health broken dot reference loaded. Preview updated!")
    
    def save_low_health(self):
        if not self.full_health_image or not self.low_broken_reference:
            messagebox.showerror("Error", "Select both full health and low broken reference images!")
            return
        
        if self.broken_effect_image:
            result = self.broken_effect_image
        else:
            result = self.apply_broken_effect(self.full_health_image, self.low_broken_reference)
        
        self.update_preview(result)
        
        if self.settings["confirm_before_save"]:
            if not messagebox.askyesno("Confirm", "Save this image?"):
                return
        
        default = "low_health.png"
        p = filedialog.asksaveasfilename(defaultextension=".png", initialfile=default,
                                         filetypes=[("PNG","*.png")])
        if p:
            result_64 = result.resize((64, 64), Image.Resampling.LANCZOS)
            result_64.save(p)
            self.low_health_image = result
            
            if self.settings["auto_backup"]:
                bp = p + ".backup"
                result_64.save(bp)
            
            messagebox.showinfo("Saved", f"Low health orb saved at 64x64: {p}")
            self.step_section2_2()
    
    # Section 2.2: Final Full Health
    def step_section2_2(self):
        self.current_step = 4
        self.instruction_label.config(
            text="Section 2.2: Final Full Health\n\n"
                 "1. Upload your full health dot one more time\n"
                 "2. Click SAVE to finalize and finish\n\n"
                 "We'll save it at the correct 64x64 size for the game."
        )
        self.clear_controls()
        self.add_button("Upload Full Health", self.upload_final_full_health)
        self.add_button("SAVE & Finish", self.save_final_full_health)
        self.add_button("Skip to End", self.end_screen)
    
    def upload_final_full_health(self):
        p = filedialog.askopenfilename(filetypes=[("PNG","*.png")])
        if p:
            self.full_health_image = Image.open(p).convert("RGBA")
            self.update_preview(self.full_health_image)
    
    def save_final_full_health(self):
        if not self.full_health_image:
            messagebox.showerror("Error", "Upload full health image first!")
            return
        
        if self.settings["confirm_before_save"]:
            if not messagebox.askyesno("Confirm", "Save this image?"):
                return
        
        default = "final_full_health.png"
        p = filedialog.asksaveasfilename(defaultextension=".png", initialfile=default,
                                         filetypes=[("PNG","*.png")])
        if p:
            # resize to 64x64
            result_64 = self.full_health_image.resize((64, 64), Image.Resampling.LANCZOS)
            result_64.save(p)
            
            if self.settings["auto_backup"]:
                bp = p + ".backup"
                result_64.save(bp)
            
            messagebox.showinfo("Saved", f"Full health orb saved at 64x64: {p}")
            self.end_screen()
    
    # End Screen
    def end_screen(self):
        self.current_step = 4
        self.instruction_label.config(
            text="🎉 Congratulations! You've created your WOD skin! 🎉\n\n"
                 "How to add it to the game:\n"
                 "1. Join the WOD Discord: https://discord.gg/warofdots\n"
                 "2. Go into the #suggest channel and make a suggestion.\n"
                 "3. Message Thegypt to ask Python (the creator) about your skin and whether it could be added.\n\n"
                 "⚠️ Important: Do NOT harass anyone to add your skin.\n\n"
                 "Thank you for using WOD Skin Maker!\n"
                 "Made by Wowthatp\n\n"
                 "Press ESC to exit."
        )
        self.clear_controls()
        self.add_button("Create Another Skin", self.restart_app)
    
    def restart_app(self):
        # reset everything
        self.current_step = 0
        self.full_health_image = None
        self.preview_image = None
        self.medium_health_image = None
        self.low_health_image = None
        self.broken_reference = None
        self.low_broken_reference = None
        self.full_health_saved = False
        self.ring_color = (0, 0, 0)
        self.ring_thickness = 20
        self.ring_center = [0, 0]
        self.canvas.delete("all")
        self.step_0()
    
    # Eraser Tool
    def start_eraser_medium(self):
        if not self.broken_effect_image:
            messagebox.showerror("Error", "Load a broken reference first!")
            return
        
        self.eraser_enabled = True
        self.instruction_label.config(
            text="Eraser Tool:\n- Draw on canvas to erase\n- Click 'Done Erasing' when finished"
        )
        
        self.canvas.bind("<Button-1>", self.on_eraser_press)
        self.canvas.bind("<B1-Motion>", self.on_eraser_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_eraser_release)
        
        self.clear_controls()
        self.add_button("Eraser Size -", lambda: self.adjust_eraser_size(-2))
        self.add_button("Eraser Size +", lambda: self.adjust_eraser_size(2))
        tk.Label(self.control_frame, text=f"Size: {self.eraser_size}px",
                fg=TEXT, bg=PANEL).pack()
        self.add_button("Done Erasing", lambda: self.stop_eraser(2))
    
    def start_eraser_low(self):
        if not self.broken_effect_image:
            messagebox.showerror("Error", "Load a broken reference first!")
            return
        
        self.eraser_enabled = True
        self.instruction_label.config(
            text="Eraser Tool:\n- Draw on canvas to erase\n- Click 'Done Erasing' when finished"
        )
        
        self.canvas.bind("<Button-1>", self.on_eraser_press)
        self.canvas.bind("<B1-Motion>", self.on_eraser_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_eraser_release)
        
        self.clear_controls()
        self.add_button("Eraser Size -", lambda: self.adjust_eraser_size(-2))
        self.add_button("Eraser Size +", lambda: self.adjust_eraser_size(2))
        tk.Label(self.control_frame, text=f"Size: {self.eraser_size}px",
                fg=TEXT, bg=PANEL).pack()
        self.add_button("Done Erasing", lambda: self.stop_eraser(3))
    
    def adjust_eraser_size(self, delta):
        self.eraser_size = max(5, min(50, self.eraser_size + delta))
        self.update_eraser_ui()
    
    def update_eraser_ui(self):
        for w in self.control_frame.winfo_children():
            if isinstance(w, tk.Label) and "Size:" in w.cget("text"):
                w.config(text=f"Size: {self.eraser_size}px")
                break
    
    def on_eraser_press(self, event):
        self.last_eraser_pos = (event.x, event.y)
    
    def on_eraser_drag(self, event):
        if not self.broken_effect_image or not self.eraser_enabled:
            return
        
        cw = self.canvas.winfo_width() or 800
        ch = self.canvas.winfo_height() or 800
        iw, ih = self.broken_effect_image.size
        
        xr = iw / cw
        yr = ih / ch
        
        x = int((event.x - cw//2) * xr + iw//2)
        y = int((event.y - ch//2) * yr + ih//2)
        
        x = max(0, min(iw - 1, x))
        y = max(0, min(ih - 1, y))
        
        draw = ImageDraw.Draw(self.broken_effect_image)
        draw.ellipse((x - self.eraser_size//2, y - self.eraser_size//2,
                     x + self.eraser_size//2, y + self.eraser_size//2),
                    fill=(0, 0, 0, 0))
        
        self.update_preview(self.broken_effect_image)
    
    def on_eraser_release(self, event):
        self.last_eraser_pos = None
    
    def stop_eraser(self, step):
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.eraser_enabled = False
        
        messagebox.showinfo("Done", "Erasing complete!")
        
        if step == 2:
            self.step_section2()
        elif step == 3:
            self.step_section2_1()
    
    # Helpers
    def clear_controls(self):
        for w in self.control_frame.winfo_children():
            w.destroy()
        self.buttons = {}
        self.control_frame.update_idletasks()
    
    def add_button(self, text, command):
        btn = tk.Button(self.control_frame, text=text, command=command,
                       font=("Consolas", 11), bg=ACCENT, fg=BTN_TXT,
                       activebackground=BTN_HOVER, relief="flat",
                       width=25, height=2)
        btn.pack(pady=5, fill="x", expand=False)
        self.buttons[text] = btn
        self.control_frame.update_idletasks()
    
    # Settings window
    def open_settings(self):
        sw = tk.Toplevel(self.root)
        sw.title("Settings - WOD Skin Maker")
        sw.geometry(f"{self.root.winfo_width()}x{self.root.winfo_height()}")
        sw.configure(bg=BG)
        sw.transient(self.root)
        sw.grab_set()
        
        # top bar
        tf = tk.Frame(sw, bg=PANEL, height=60)
        tf.pack(side="top", fill="x")
        tf.pack_propagate(False)
        
        bb = tk.Button(tf, text="← Back", command=sw.destroy,
                      font=("Consolas", 12, "bold"), bg=PANEL, fg=ACCENT,
                      activebackground=PANEL, relief="flat", bd=0, padx=20)
        bb.pack(side="left", padx=10, pady=10)
        
        title = tk.Label(tf, text="Settings", font=("Consolas", 18, "bold"),
                        fg=TEXT, bg=PANEL)
        title.pack(side="left", padx=20, pady=10)
        
        # separator
        sep = tk.Frame(sw, bg="#444444", height=1)
        sep.pack(fill="x")
        
        # scrollable area
        canvas = tk.Canvas(sw, bg=BG, highlightthickness=0)
        sb = tk.Scrollbar(sw, orient="vertical", command=canvas.yview)
        sf = tk.Frame(canvas, bg=BG)
        
        sf.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=sf, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        
        # categories
        cats = {
            "Display & Appearance": [
                ("Theme", "theme", "dropdown", ["dark", "light"]),
                ("Button Size", "button_size", "dropdown", ["small", "medium", "large"]),
                ("Font Size", "font_size", "scale", 8, 16),
                ("Preview Size", "preview_size", "dropdown", ["small", "medium", "large"]),
                ("Canvas Zoom (%)", "canvas_zoom", "scale", 50, 200),
            ],
            "File Management": [
                ("Confirm Before Save", "confirm_before_save", "bool"),
                ("Auto Backup", "auto_backup", "bool"),
                ("Auto Name Files", "auto_name_files", "bool"),
                ("Recent Files Limit", "recent_files_limit", "scale", 1, 20),
            ],
            "Image Processing": [
                ("Ring Thickness Preset", "ring_thickness_preset", "scale", 1, 100),
                ("Image Quality", "image_quality", "dropdown", ["low", "medium", "high"]),
            ],
            "View Options": [
                ("Show Grid", "show_grid", "bool"),
                ("Show Coordinates", "show_coordinates", "bool"),
                ("Show Tips", "show_tips", "bool"),
            ],
            "Advanced": [
                ("Animation Enabled", "animation_enabled", "bool"),
                ("Undo History Limit", "undo_history_limit", "scale", 1, 50),
                ("Advanced Mode", "advanced_mode", "bool"),
            ],
        }
        
        for cat, settings_list in cats.items():
            self.create_cat_header(sf, cat)
            for s in settings_list:
                self.create_setting_widget(sf, s)
        
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        
        # bottom buttons
        bf = tk.Frame(sw, bg=PANEL)
        bf.pack(side="bottom", fill="x", padx=10, pady=10)
        
        tk.Button(bf, text="Apply Settings", command=self.apply_all_settings,
                 font=("Consolas", 12, "bold"), bg=ACCENT, fg=BTN_TXT,
                 activebackground=BTN_HOVER, relief="flat",
                 padx=20, pady=10).pack(side="right", padx=5)
    
    def create_cat_header(self, parent, cat):
        hf = tk.Frame(parent, bg=BG)
        hf.pack(fill="x", padx=20, pady=(20, 10))
        
        tk.Label(hf, text=cat, font=("Consolas", 12, "bold"),
                fg=ACCENT, bg=BG).pack(anchor="w")
        
        sep = tk.Frame(hf, bg="#444444", height=2)
        sep.pack(fill="x", pady=(5, 0))
    
    def create_setting_widget(self, parent, setting):
        f = tk.Frame(parent, bg=BG)
        f.pack(fill="x", padx=40, pady=10)
        
        lf = tk.Frame(f, bg=BG)
        lf.pack(fill="x", anchor="w")
        
        lbl = tk.Label(lf, text=setting[0], font=("Consolas", 11),
                      fg=TEXT, bg=BG)
        lbl.pack(anchor="w")
        
        cf = tk.Frame(f, bg=BG)
        cf.pack(fill="x", pady=(5, 0))
        
        if setting[2] == "bool":
            var = tk.BooleanVar(value=self.settings[setting[1]])
            cb = tk.Checkbutton(cf, variable=var, bg=BG, fg=ACCENT,
                               selectcolor=BG, font=("Consolas", 10),
                               command=lambda v=var: self.upd_setting(setting[1], v.get()))
            cb.pack(anchor="w")
        
        elif setting[2] == "dropdown":
            var = tk.StringVar(value=self.settings[setting[1]])
            opts = setting[3]
            dd = tk.OptionMenu(cf, var, *opts,
                              command=lambda v: self.upd_setting(setting[1], v))
            dd.config(bg=PANEL, fg=TEXT, font=("Consolas", 10), highlightthickness=0)
            dd.pack(anchor="w")
        
        elif setting[2] == "scale":
            var = tk.IntVar(value=self.settings[setting[1]])
            
            vl = tk.Label(cf, text=str(var.get()), font=("Consolas", 10),
                         fg=ACCENT, bg=BG, width=4)
            vl.pack(side="right", padx=(10, 0))
            
            sc = tk.Scale(cf, from_=setting[3], to=setting[4],
                         orient="horizontal", variable=var,
                         bg=PANEL, fg=TEXT, troughcolor="#333333",
                         highlightthickness=0, length=200,
                         command=lambda v, vl=vl: (vl.config(text=v),
                                                   self.upd_setting(setting[1], int(v))))
            sc.pack(fill="x", expand=True)
    
    def upd_setting(self, key, val):
        self.settings[key] = val
        
        # apply some settings immediately
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
            self.ring_thickness = val
        elif key == "preview_size":
            sizes = {"small": 300, "medium": 600, "large": 800}
            self.canvas.config(height=sizes.get(val, 600))
    
    def apply_font_size(self, sz):
        self.header.config(font=("Consolas", sz + 5, "bold"))
        self.instruction_label.config(font=("Consolas", sz))
        for btn in self.buttons.values():
            btn.config(font=("Consolas", sz))
    
    def apply_all_settings(self):
        fsz = self.settings["font_size"]
        self.apply_font_size(fsz)
        messagebox.showinfo("Settings Applied", "All settings have been applied successfully!")
    
    def apply_theme(self, theme_name):
        if theme_name not in self.themes:
            return
        
        t = self.themes[theme_name]
        self.root.configure(bg=t["bg"])
        self.left_frame.configure(bg=t["bg"])
        self.right_frame.configure(bg=t["panel"])
        self.canvas.configure(bg=t["bg"])
        self.header.configure(bg=t["panel"], fg=t["accent"])
        self.instruction_label.configure(bg=t["panel"], fg=t["text"])
        self.control_frame.configure(bg=t["panel"])
        
        for btn in self.buttons.values():
            btn.configure(bg=t["accent"], fg="#ffffff")
    
    # Dev Mode
    def open_dev_mode(self):
        correct = "wowthatis!"
        
        dw = tk.Toplevel(self.root)
        dw.title("Dev Mode")
        dw.geometry("400x180")
        dw.configure(bg=BG)
        dw.transient(self.root)
        dw.grab_set()
        dw.resizable(False, False)
        
        tk.Label(dw, text="Dev Mode Access", font=("Consolas", 14, "bold"),
                fg=ACCENT, bg=BG).pack(pady=10)
        
        tk.Label(dw, text="Enter Password:", font=("Consolas", 10),
                fg=TEXT, bg=BG).pack()
        
        pe = tk.Entry(dw, show="•", font=("Consolas", 10), bg=PANEL,
                     fg=TEXT, insertbackground=TEXT, width=30)
        pe.pack(pady=10)
        pe.focus()
        
        hint = tk.Label(dw, text="", font=("Consolas", 8), fg="#888", bg=BG)
        hint.pack()
        
        attempts = [0]
        
        def check():
            entered = pe.get().strip()
            
            if entered == correct:
                dw.destroy()
                self.show_dev_menu()
            else:
                attempts[0] += 1
                if attempts[0] >= 2:
                    hint.config(text="Hint: Type carefully, check caps lock")
                messagebox.showerror("Access Denied", f"Incorrect password (Attempt {attempts[0]})")
                pe.delete(0, tk.END)
                pe.focus()
        
        bf = tk.Frame(dw, bg=BG)
        bf.pack(pady=10)
        
        tk.Button(bf, text="Enter", command=check, font=("Consolas", 10),
                 bg=ACCENT, fg=BTN_TXT, activebackground=BTN_HOVER,
                 relief="flat", width=15).pack(side="left", padx=5)
        
        tk.Button(bf, text="Cancel", command=dw.destroy, font=("Consolas", 10),
                 bg="#666", fg=BTN_TXT, activebackground="#888",
                 relief="flat", width=15).pack(side="left", padx=5)
        
        pe.bind("<Return>", lambda e: check())
    
    def show_dev_menu(self):
        dm = tk.Toplevel(self.root)
        dm.title("Dev Mode Menu")
        dm.geometry("450x550")
        dm.configure(bg=BG)
        dm.transient(self.root)
        dm.grab_set()
        
        tk.Label(dm, text="Developer Mode", font=("Consolas", 14, "bold"),
                fg=ACCENT, bg=BG).pack(pady=15)
        
        c = tk.Canvas(dm, bg=BG, highlightthickness=0)
        sb = tk.Scrollbar(dm, orient="vertical", command=c.yview)
        sf = tk.Frame(c, bg=BG)
        
        sf.bind("<Configure>", lambda e: c.configure(scrollregion=c.bbox("all")))
        c.create_window((0, 0), window=sf, anchor="nw")
        c.configure(yscrollcommand=sb.set)
        
        c.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        sb.pack(side="right", fill="y")
        
        # dev functions
        def show_debug():
            info = f"Debug Information:\n\n"
            info += f"Current Step: {self.current_step}\n"
            info += f"Full Health Saved: {self.full_health_saved}\n"
            info += f"Ring Thickness: {self.ring_thickness}\n"
            info += f"Ring Color: {self.ring_color}\n"
            info += f"Font Size: {self.settings.get('font_size', 'N/A')}\n"
            info += f"Zoom Level: {self.zoom_level}\n"
            info += f"Drawing Enabled: {self.drawing_enabled}\n"
            messagebox.showinfo("Debug Info", info)
        
        def show_img_stats():
            if not self.full_health_image:
                messagebox.showinfo("Image Stats", "No image loaded")
                return
            
            w, h = self.full_health_image.size
            info = f"Image Statistics:\n\n"
            info += f"Dimensions: {w}x{h} pixels\n"
            info += f"Mode: {self.full_health_image.mode}\n"
            info += f"Has Transparency: Yes (RGBA)\n"
            info += f"Expected Save Size: ~64x64 px\n"
            messagebox.showinfo("Image Stats", info)
        
        def show_paths():
            cwd = os.getcwd()
            info = f"File Paths:\n\n"
            info += f"Working Directory:\n{cwd}\n\n"
            info += f"Skins saved in: {cwd}\n"
            info += f"Presets file: {self.presets_file}\n"
            info += f"Preset count: {len(self.presets)}\n"
            messagebox.showinfo("File Paths", info)
        
        def clear_presets():
            if messagebox.askyesno("Clear Presets", "Delete all saved ring presets?"):
                try:
                    self.presets = {}
                    self.save_presets_to_file()
                    messagebox.showinfo("Success", "All presets cleared!")
                except Exception as e:
                    messagebox.showerror("Error", f"Could not clear presets:\n{str(e)}")
        
        def reset_settings():
            if messagebox.askyesno("Reset Settings", "Restore all settings to default?"):
                self.settings = {
                    "show_tips": True, "auto_save": False, "theme": "dark",
                    "button_size": "medium", "font_size": 11, "canvas_zoom": 100,
                    "confirm_before_save": True, "ring_thickness_preset": 20,
                    "image_quality": "high", "show_grid": False,
                    "auto_name_files": False, "show_coordinates": False,
                    "recent_files_limit": 5, "preview_size": "large",
                    "canvas_bg_color": BG, "animation_enabled": True,
                    "undo_history_limit": 10, "auto_backup": True,
                    "advanced_mode": False
                }
                self.apply_all_settings()
                messagebox.showinfo("Success", "Settings reset to default!")
                dm.destroy()
        
        def test_exp():
            if not self.full_health_image:
                messagebox.showinfo("Test Export", "No image loaded")
                return
            
            try:
                img = self.full_health_image.copy()
                img.thumbnail((64, 64), Image.Resampling.LANCZOS)
                self.preview_image = ImageTk.PhotoImage(img)
                self.canvas.delete("all")
                cw = self.canvas.winfo_width() or 800
                ch = self.canvas.winfo_height() or 800
                self.canvas.create_image(cw//2, ch//2, image=self.preview_image)
                messagebox.showinfo("Test Export", "64x64 preview shown on canvas!")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed:\n{str(e)}")
        
        def reset():
            if messagebox.askyesno("Reset", "Reset app to initial state?"):
                try:
                    self.restart_app()
                    dm.destroy()
                    messagebox.showinfo("Success", "Application reset!")
                except Exception as e:
                    messagebox.showerror("Error", f"Reset failed:\n{str(e)}")
        
        def open_bdce():
            try:
                self.open_bdce_editor()
            except Exception as e:
                messagebox.showerror("Error", f"Could not open BDCE:\n{str(e)}")
        
        btns = [
            ("Show Debug Info", show_debug),
            ("Show Image Stats", show_img_stats),
            ("Show File Paths", show_paths),
            ("Clear All Presets", clear_presets),
            ("Reset Settings", reset_settings),
            ("Test Export (64x64)", test_exp),
            ("Broken Dot Creator (BDCE)", open_bdce),
            ("Reset Application", reset),
            ("Close Dev Menu", dm.destroy),
        ]
        
        for txt, cmd in btns:
            tk.Button(sf, text=txt, command=lambda c=cmd: c(),
                     font=("Consolas", 10), bg=ACCENT, fg=BTN_TXT,
                     activebackground=BTN_HOVER, relief="flat",
                     width=30).pack(pady=4)
    
    # BDCE Editor
    def open_bdce_editor(self):
        bw = tk.Toplevel(self.root)
        bw.title("BDCE - Broken Dot Creator Editor")
        bw.geometry("1000x800")
        bw.configure(bg=BG)
        bw.transient(self.root)
        
        # state
        bw.bg_img = None
        bw.mask = Image.new("L", (512, 512), 255)
        bw.display = None
        bw.brush_sz = 20
        
        # left: canvas
        lf = tk.Frame(bw, bg=BG)
        lf.pack(side="left", fill="both", expand=True)
        
        cc = tk.Frame(lf, bg=BG)
        cc.pack(expand=True)
        
        cnv = tk.Canvas(cc, bg="white", width=512, height=512,
                       highlightthickness=2, highlightbackground=ACCENT)
        cnv.pack(pady=20, padx=20)
        bw.cnv = cnv
        
        # right: controls
        rf = tk.Frame(bw, bg=PANEL, width=300)
        rf.pack(side="right", fill="y")
        rf.pack_propagate(False)
        
        tk.Label(rf, text="BDCE Tools", font=("Consolas", 14, "bold"),
                fg=ACCENT, bg=PANEL).pack(pady=20)
        
        tk.Label(rf, text="Create broken dot patterns\nfor damaged health orbs",
                font=("Consolas", 9), fg=TEXT, bg=PANEL,
                justify="center").pack(pady=5)
        
        tk.Frame(rf, bg="#444444", height=2).pack(fill="x", padx=20, pady=10)
        
        # functions
        def upd_cnv():
            try:
                if bw.bg_img:
                    img = bw.bg_img.copy()
                else:
                    img = Image.new("RGBA", (512, 512), (255, 255, 255, 255))
                
                inv = ImageOps.invert(bw.mask)
                blk = Image.new("RGBA", (512, 512), (0, 0, 0, 255))
                img.paste(blk, (0, 0), inv)
                
                bw.display = ImageTk.PhotoImage(img)
                bw.cnv.delete("all")
                bw.cnv.create_image(0, 0, image=bw.display, anchor="nw")
            except Exception as e:
                print(f"Update error: {e}")
        
        def load_ref():
            try:
                p = filedialog.askopenfilename(
                    title="Select Reference Image",
                    filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")])
                
                if p:
                    img = Image.open(p).convert("RGBA")
                    img = img.resize((512, 512), Image.Resampling.LANCZOS)
                    bw.bg_img = img
                    upd_cnv()
                    messagebox.showinfo("Loaded", "Reference image loaded!")
            except Exception as e:
                messagebox.showerror("Error", f"Load failed:\n{str(e)}")
        
        def clear():
            try:
                if messagebox.askyesno("Clear", "Clear all drawing?"):
                    bw.mask = Image.new("L", (512, 512), 255)
                    upd_cnv()
            except Exception as e:
                messagebox.showerror("Error", f"Clear failed:\n{str(e)}")
        
        def invert():
            try:
                bw.mask = ImageOps.invert(bw.mask)
                upd_cnv()
                messagebox.showinfo("Done", "Pattern inverted!")
            except Exception as e:
                messagebox.showerror("Error", f"Invert failed:\n{str(e)}")
        
        def save():
            try:
                p = filedialog.asksaveasfilename(
                    defaultextension=".png",
                    initialfile="broken_pattern.png",
                    filetypes=[("PNG", "*.png")])
                
                if p:
                    out = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
                    blk = Image.new("RGBA", (512, 512), (0, 0, 0, 255))
                    inv = ImageOps.invert(bw.mask)
                    out.paste(blk, (0, 0), inv)
                    out.save(p)
                    messagebox.showinfo("Saved", f"Pattern saved to:\n{p}")
            except Exception as e:
                messagebox.showerror("Error", f"Save failed:\n{str(e)}")
        
        def close():
            bw.destroy()
        
        def paint_solid(event):
            x, y = event.x, event.y
            if 0 <= x < 512 and 0 <= y < 512:
                r = bw.brush_sz
                draw = ImageDraw.Draw(bw.mask)
                draw.ellipse([x-r, y-r, x+r, y+r], fill=0)
                upd_cnv()
        
        def paint_spray(event):
            import random
            x, y = event.x, event.y
            if 0 <= x < 512 and 0 <= y < 512:
                r = bw.brush_sz
                draw = ImageDraw.Draw(bw.mask)
                for _ in range(max(10, r)):
                    dx = random.randint(-r, r)
                    dy = random.randint(-r, r)
                    if dx*dx + dy*dy <= r*r:
                        px, py = x + dx, y + dy
                        if 0 <= px < 512 and 0 <= py < 512:
                            sz = random.randint(1, 3)
                            draw.ellipse([px-sz, py-sz, px+sz, py+sz], fill=0)
                upd_cnv()
        
        # UI
        ub = tk.Button(rf, text="📁 Load Reference Image", command=load_ref,
                      bg=ACCENT, fg=BTN_TXT, font=("Consolas", 10),
                      relief="flat", width=25, height=2)
        ub.pack(pady=5, padx=10)
        
        # brush size
        brf = tk.Frame(rf, bg=PANEL)
        brf.pack(pady=15, padx=10, fill="x")
        
        tk.Label(brf, text="Brush Size:", fg=TEXT, bg=PANEL,
                font=("Consolas", 10)).pack(anchor="w")
        
        szl = tk.Label(brf, text="20 px", fg=ACCENT, bg=PANEL,
                      font=("Consolas", 10, "bold"))
        szl.pack(anchor="e")
        
        def upd_sz(v):
            bw.brush_sz = int(v)
            szl.config(text=f"{v} px")
        
        szs = tk.Scale(brf, from_=1, to=100, orient="horizontal",
                      command=upd_sz, bg=PANEL, fg=TEXT,
                      troughcolor="#333333", highlightthickness=0)
        szs.set(20)
        szs.pack(fill="x", pady=5)
        
        tk.Label(rf, text="Draw Tools:", fg=TEXT, bg=PANEL,
                font=("Consolas", 10, "bold")).pack(anchor="w", padx=10, pady=(10,5))
        
        tk.Label(rf, text="• Left Click: Solid\n• Right Click: Spray",
                fg=TEXT, bg=PANEL, font=("Consolas", 9)).pack(anchor="w", padx=20)
        
        # bind events
        cnv.bind("<Button-1>", paint_solid)
        cnv.bind("<B1-Motion>", paint_solid)
        cnv.bind("<Button-3>", paint_spray)
        cnv.bind("<B3-Motion>", paint_spray)
        
        tk.Frame(rf, bg="#444444", height=2).pack(fill="x", padx=20, pady=15)
        
        # action buttons
        clb = tk.Button(rf, text="🗑️ Clear Canvas", command=clear,
                       bg="#666", fg=BTN_TXT, font=("Consolas", 10),
                       relief="flat", width=25)
        clb.pack(pady=5, padx=10)
        
        invb = tk.Button(rf, text="🔄 Invert Pattern", command=invert,
                        bg="#666", fg=BTN_TXT, font=("Consolas", 10),
                        relief="flat", width=25)
        invb.pack(pady=5, padx=10)
        
        svb = tk.Button(rf, text="💾 SAVE Pattern", command=save,
                       bg="#28a745", fg=BTN_TXT, font=("Consolas", 10, "bold"),
                       relief="flat", width=25)
        svb.pack(pady=10, padx=10)
        
        tk.Frame(rf, bg="#444444", height=2).pack(fill="x", padx=20, pady=10)
        
        clsb = tk.Button(rf, text="❌ Close Editor", command=close,
                        bg="#dc3545", fg=BTN_TXT, font=("Consolas", 10, "bold"),
                        relief="flat", width=25)
        clsb.pack(pady=10, padx=10)
        
        tk.Label(rf, text="\n💡 Black = broken areas",
                font=("Consolas", 8), fg="#888", bg=PANEL).pack(side="bottom", pady=10)
        
        upd_cnv()

if __name__ == "__main__":
    root = tk.Tk()
    app = WODSkinMaker(root)
    root.mainloop()
