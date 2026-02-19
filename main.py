import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image, ImageTk, ImageDraw
import os


BG = "#1e1e1e"
PANEL = "#252526"
TEXT = "#d4d4d4"
ACCENT = "#007acc"
BUTTON_HOVER = "#0a84ff"
BUTTON_TEXT = "#ffffff"


class WODSkinMaker:
    def __init__(self, root):
        self.root = root
        self.root.title("WOD Skin Maker")
        self.root.geometry("1200x800")
        self.root.configure(bg=BG)
        self.root.bind("<Escape>", lambda e: self.root.destroy())

        # Variables
        self.current_step = 0
        self.full_health_image = None
        self.preview_image = None
        self.medium_health_image = None
        self.low_health_image = None
        self.broken_reference = None
        self.low_broken_reference = None

        # Ring Maker variables
        self.ring_color = (0,0,0)
        self.ring_thickness = 20
        self.ring_center = [0,0]
        
        # Track if image has been saved
        self.full_health_saved = False

        # UI Containers
        self.left_frame = tk.Frame(root, bg=BG)
        self.left_frame.pack(side="left", fill="both", expand=True)

        self.right_frame = tk.Frame(root, width=350, bg=PANEL)
        self.right_frame.pack(side="right", fill="y")

        # Preview Canvas
        self.canvas = tk.Canvas(self.left_frame, bg=BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Right Frame Widgets

        # --- Add panel logo ---
        logo_path = r"C:\Users\trey\Downloads\logo.png"
        if os.path.exists(logo_path):
            logo_img = Image.open(logo_path).convert("RGBA")
            logo_img.thumbnail((100, 100), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_img)
            self.logo_label = tk.Label(self.right_frame, image=self.logo_photo, bg=PANEL)
            self.logo_label.pack(pady=(10, 0))
        # --- End panel logo ---

        self.header = tk.Label(self.right_frame, text="WOD Skin Maker",
                               font=("Consolas", 16, "bold"), fg=ACCENT, bg=PANEL)
        self.header.pack(pady=20)

        self.instruction_label = tk.Label(self.right_frame, text="", justify="left",
                                          font=("Consolas", 11), fg=TEXT, bg=PANEL, wraplength=330)
        self.instruction_label.pack(pady=10)

        self.control_frame = tk.Frame(self.right_frame, bg=PANEL)
        self.control_frame.pack(pady=20)

        self.buttons = {}

        # Start Step 0
        self.step_0()

    # welcome screen
    def step_0(self):
        self.current_step = 0
        self.instruction_label.config(
            text="Welcome to WOD Skin Maker!\n\n"
                 "Naming rules for your skin:\n"
                 "- Infantry full health: if_NAMEOFSKIN\n"
                 "- Infantry medium health: if2_NAMEOFSKIN\n"
                 "- Infantry low health: if3_NAMEOFSKIN\n"
                 "- Tank full health: tank1_NAMEOFSKIN\n"
                 "- Tank medium health: tank2_NAMEOFSKIN\n"
                 "- Tank low health: tank3_NAMEOFSKIN\n\n"
                 "Click 'Next' to start creating your full health orb."
                "you have to run this porgram 2 twice once for if unit and other time for tank unit\n"
        )
        self.clear_controls()
        self.add_button("Next", self.step_full_health)

    # Step 1–4: Full Health Orb creation
    def step_full_health(self):
        self.current_step = 1
        self.instruction_label.config(
            text="Step 1: Load your image to create the full health orb.\n\n"
                 "You can crop it to a circle and add a ring if you want.\n"
                 "Then save your image before proceeding."
        )
        self.clear_controls()
        self.add_button("Load Image", self.load_full_health_image)
        self.add_button("Circle Crop", self.circle_cropper)
        self.add_button("Add Ring", self.ring_maker_mode)
        self.add_button("Save Image", self.save_full_health_image)
        if self.full_health_saved:
            self.add_button("Next", self.step_section2)

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
        if self.full_health_image is None:
            messagebox.showerror("Error", "Load or create an image first!")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png"), ("All Files", "*.*")]
        )
        if path:
            self.full_health_image.save(path)
            self.full_health_saved = True
            messagebox.showinfo("Success", f"Image saved: {path}")
            self.step_full_health()

    def update_preview(self, img):
        if img is None:
            return
        canvas_width = self.canvas.winfo_width() or 800
        canvas_height = self.canvas.winfo_height() or 800
        preview = img.copy()
        preview.thumbnail((canvas_width, canvas_height), Image.Resampling.LANCZOS)
        self.preview_image = ImageTk.PhotoImage(preview)
        self.canvas.delete("all")
        self.canvas.create_image(canvas_width//2, canvas_height//2, image=self.preview_image)

    #  Circle Cropper tool
    def circle_cropper(self):
        if self.full_health_image is None:
            messagebox.showerror("Error", "Load an image first!")
            return
        w,h = self.full_health_image.size
        mask = Image.new("L", (w,h), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0,0,w,h), fill=255)
        cropped = Image.new("RGBA", (w,h))
        cropped.paste(self.full_health_image, (0,0), mask)
        self.full_health_image = cropped
        self.update_preview(cropped)

    # Ring Maker Mode 
    def ring_maker_mode(self):
        if self.full_health_image is None:
            messagebox.showerror("Error", "Load an image first!")
            return
        color = colorchooser.askcolor(title="Select ring color")[0]
        if color is None:
            return
        self.ring_color = tuple(map(int,color))
        self.ring_thickness = 20
        w,h = self.full_health_image.size
        self.ring_center = [w//2,h//2]

        self.instruction_label.config(
            text="Ring Maker:\n- Adjust ring thickness with slider\n- Click 'Done' to apply"
        )
        self.clear_controls()

        # Thickness slider
        slider = tk.Scale(self.control_frame, from_=1, to=100, orient="horizontal",
                          label="Ring Thickness", command=self.update_ring_preview,
                          bg=PANEL, fg=TEXT, troughcolor="#333333", highlightthickness=0)
        slider.set(self.ring_thickness)
        slider.pack(pady=10)
        self.ring_slider = slider

        self.add_button("Done", self.apply_ring)

        self.update_ring_preview(slider.get())
    
    def update_ring_preview(self, value=None):
        if value is not None:
            self.ring_thickness = int(value)
        if self.full_health_image is None:
            return
        
        img = self.full_health_image.copy()
        w, h = img.size
        size = min(w, h)
        left = (w - size) // 2
        top = (h - size) // 2
        img = img.crop((left, top, left + size, top + size))
        
        # Make image circular
        mask = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size - 1, size - 1), fill=255)
        circular = Image.new("RGBA", (size, size))
        circular.paste(img, (0, 0), mask)
        
        # Create ring
        ring = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(ring)
        draw.ellipse((0, 0, size - 1, size - 1), outline=self.ring_color, width=self.ring_thickness)
        
        result = Image.alpha_composite(circular, ring)
        self.update_preview(result)

    def drag_ring(self, event):
        # Not used anymore, but keeping for potential future use
        pass

    def apply_ring(self):
        if self.full_health_image is None:
            return
        
        img = self.full_health_image.copy()
        w, h = img.size
        size = min(w, h)
        left = (w - size) // 2
        top = (h - size) // 2
        img = img.crop((left, top, left + size, top + size))
        
        # Make image circular
        mask = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size - 1, size - 1), fill=255)
        circular = Image.new("RGBA", (size, size))
        circular.paste(img, (0, 0), mask)
        
        # Create ring
        ring = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(ring)
        draw.ellipse((0, 0, size - 1, size - 1), outline=self.ring_color, width=self.ring_thickness)
        
        result = Image.alpha_composite(circular, ring)
        self.full_health_image = result
        self.update_preview(result)
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.step_full_health()

    #  Section 2: Medium Health 
    def step_section2(self):
        self.current_step = 2
        self.instruction_label.config(
            text="Section 2: Medium Health Orb\n\n"
                 "Upload your full health orb and a broken dot reference.\n"
                 "Get the reference from WOD folder: assets/skins → open any folder → select a BROKEN dot effect (NOT full health)."
        )
        self.clear_controls()
        self.add_button("Upload Full Health", self.upload_full_health_for_broken)
        self.add_button("Upload Broken Reference", self.upload_broken_reference)
        self.add_button("Save", self.save_medium_health)
        self.add_button("Done", self.step_section2_1)

    def upload_full_health_for_broken(self):
        path = filedialog.askopenfilename(filetypes=[("PNG","*.png")])
        if path:
            self.full_health_image = Image.open(path).convert("RGBA")
            self.update_preview(self.full_health_image)

    def upload_broken_reference(self):
        path = filedialog.askopenfilename(filetypes=[("PNG","*.png")])
        if path:
            self.broken_reference = Image.open(path).convert("RGBA")
            # Show preview of the effect if full health is loaded
            if self.full_health_image is not None:
                preview = self.apply_broken_effect(self.full_health_image, self.broken_reference)
                self.update_preview(preview)
            messagebox.showinfo("Reference loaded", "Broken dot reference loaded. Preview updated!")

    def apply_broken_effect(self, full, broken_ref):
        # Resize broken reference to match full health image size
        broken_ref_resized = broken_ref.resize(full.size, Image.Resampling.LANCZOS)
        mask = broken_ref_resized.split()[3]  # alpha channel
        result = full.copy()
        result.putalpha(mask)
        return result

    def save_medium_health(self):
        if self.full_health_image is None or self.broken_reference is None:
            messagebox.showerror("Error", "Select both full health and broken reference images!")
            return
        result = self.apply_broken_effect(self.full_health_image, self.broken_reference)
        self.update_preview(result)
        path = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=[("PNG","*.png")])
        if path:
            result.save(path)
            self.medium_health_image = result
            messagebox.showinfo("Saved", f"Medium health orb saved: {path}")

    #  Section 2.1: Low Health
    def step_section2_1(self):
        self.current_step = 3
        self.instruction_label.config(
            text="Section 2.1: Low Health Orb\n\n"
                 "Now create the low health unit using a different broken dot effect.\n"
                 "Upload full health orb again and select a new broken dot reference."
        )
        self.clear_controls()
        self.add_button("Upload Full Health", self.upload_full_health_for_broken_low)
        self.add_button("Upload Broken Reference", self.upload_low_broken_reference)
        self.add_button("Save", self.save_low_health)
        self.add_button("Done", self.end_screen)

    def upload_full_health_for_broken_low(self):
        self.upload_full_health_for_broken()

    def upload_low_broken_reference(self):
        path = filedialog.askopenfilename(filetypes=[("PNG","*.png")])
        if path:
            self.low_broken_reference = Image.open(path).convert("RGBA")
            # Show preview of the effect if full health is loaded
            if self.full_health_image is not None:
                preview = self.apply_broken_effect(self.full_health_image, self.low_broken_reference)
                self.update_preview(preview)
            messagebox.showinfo("Reference loaded", "Low health broken dot reference loaded. Preview updated!")

    def save_low_health(self):
        if self.full_health_image is None or self.low_broken_reference is None:
            messagebox.showerror("Error", "Select both full health and low broken reference images!")
            return
        result = self.apply_broken_effect(self.full_health_image, self.low_broken_reference)
        self.update_preview(result)
        path = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=[("PNG","*.png")])
        if path:
            result.save(path)
            self.low_health_image = result
            messagebox.showinfo("Saved", f"Low health orb saved: {path}")

    #  End Screen 
    def end_screen(self):
        self.current_step = 4
        self.instruction_label.config(
            text="🎉 Congratulations! You’ve created your WOD skin! 🎉\n\n"
                 "How to add it to the game:\n"
                 "1. Join the WOD Discord: https://discord.gg/warofdots\n"
                 "2. Go into the #suggest channel and make a suggestion.\n"
                 "3. Message to ask Tea and Python (the creator) about your skin and whether it could be added.\n\n"
                 "⚠️ Important: Do NOT harass anyone to add your skin.\n\n"
                 "IF YOU DO YOU WILL BE BLOCKED FROM THE DISCORD AND POSSIBLY BANNED FROM THE DISCORD SERVER.\n\n"
                 "Thank you for using WOD Skin Maker!\n"
                 "Made by Wowthatp\n\n"
                 "Press ESC to exit."
        )
        self.clear_controls()

    # Helpers
    def clear_controls(self):
