# ui/windows.py - Settings, Dev Mode, and BDCE Windows

import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from PIL import Image, ImageDraw, ImageOps, ImageTk
import os
from config import THEMES

class SettingsWindow:
    """Settings window manager"""
    
    @staticmethod
    def open(app):
        """Open settings window"""
        sw = tk.Toplevel(app.root)
        sw.title("Settings - WOD Skin Maker")
        sw.geometry(f"{app.root.winfo_width()}x{app.root.winfo_height()}")
        sw.configure(bg=app.BG)
        sw.transient(app.root)
        sw.grab_set()
        
        # Top bar
        tf = tk.Frame(sw, bg=app.PANEL, height=60)
        tf.pack(side="top", fill="x")
        tf.pack_propagate(False)
        
        bb = tk.Button(tf, text="← Back", command=sw.destroy,
                      font=("Consolas", 12, "bold"), bg=app.PANEL, fg=app.ACCENT,
                      activebackground=app.PANEL, relief="flat", bd=0, padx=20)
        bb.pack(side="left", padx=10, pady=10)
        
        title = tk.Label(tf, text="Settings", font=("Consolas", 18, "bold"),
                        fg=app.TEXT, bg=app.PANEL)
        title.pack(side="left", padx=20, pady=10)
        
        # Separator
        sep = tk.Frame(sw, bg="#444444", height=1)
        sep.pack(fill="x")
        
        # Scrollable area
        canvas = tk.Canvas(sw, bg=app.BG, highlightthickness=0)
        sb = tk.Scrollbar(sw, orient="vertical", command=canvas.yview)
        sf = tk.Frame(canvas, bg=app.BG)
        
        sf.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=sf, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        
        # Categories
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
            SettingsWindow._create_cat_header(sf, cat, app)
            for s in settings_list:
                SettingsWindow._create_setting_widget(sf, s, app)
        
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        
        # Bottom buttons
        bf = tk.Frame(sw, bg=app.PANEL)
        bf.pack(side="bottom", fill="x", padx=10, pady=10)
        
        tk.Button(bf, text="Apply Settings", command=lambda: app.apply_all_settings(),
                 font=("Consolas", 12, "bold"), bg=app.ACCENT, fg=app.BTN_TXT,
                 activebackground=app.BTN_HOVER, relief="flat",
                 padx=20, pady=10).pack(side="right", padx=5)
    
    @staticmethod
    def _create_cat_header(parent, cat, app):
        """Create category header"""
        hf = tk.Frame(parent, bg=app.BG)
        hf.pack(fill="x", padx=20, pady=(20, 10))
        
        tk.Label(hf, text=cat, font=("Consolas", 12, "bold"),
                fg=app.ACCENT, bg=app.BG).pack(anchor="w")
        
        sep = tk.Frame(hf, bg="#444444", height=2)
        sep.pack(fill="x", pady=(5, 0))
    
    @staticmethod
    def _create_setting_widget(parent, setting, app):
        """Create individual setting widget"""
        f = tk.Frame(parent, bg=app.BG)
        f.pack(fill="x", padx=40, pady=10)
        
        lf = tk.Frame(f, bg=app.BG)
        lf.pack(fill="x", anchor="w")
        
        lbl = tk.Label(lf, text=setting[0], font=("Consolas", 11),
                      fg=app.TEXT, bg=app.BG)
        lbl.pack(anchor="w")
        
        cf = tk.Frame(f, bg=app.BG)
        cf.pack(fill="x", pady=(5, 0))
        
        if setting[2] == "bool":
            var = tk.BooleanVar(value=app.settings[setting[1]])
            cb = tk.Checkbutton(cf, variable=var, bg=app.BG, fg=app.ACCENT,
                               selectcolor=app.BG, font=("Consolas", 10),
                               command=lambda v=var: app.upd_setting(setting[1], v.get()))
            cb.pack(anchor="w")
        
        elif setting[2] == "dropdown":
            var = tk.StringVar(value=app.settings[setting[1]])
            opts = setting[3]
            dd = tk.OptionMenu(cf, var, *opts,
                              command=lambda v: app.upd_setting(setting[1], v))
            dd.config(bg=app.PANEL, fg=app.TEXT, font=("Consolas", 10), highlightthickness=0)
            dd.pack(anchor="w")
        
        elif setting[2] == "scale":
            var = tk.IntVar(value=app.settings[setting[1]])
            
            vl = tk.Label(cf, text=str(var.get()), font=("Consolas", 10),
                         fg=app.ACCENT, bg=app.BG, width=4)
            vl.pack(side="right", padx=(10, 0))
            
            sc = tk.Scale(cf, from_=setting[3], to=setting[4],
                         orient="horizontal", variable=var,
                         bg=app.PANEL, fg=app.TEXT, troughcolor="#333333",
                         highlightthickness=0, length=200,
                         command=lambda v, vl=vl: (vl.config(text=v),
                                                   app.upd_setting(setting[1], int(v))))
            sc.pack(fill="x", expand=True)


class DevMode:
    """Developer mode manager"""
    
    @staticmethod
    def open(app):
        """Open dev mode password dialog"""
        correct = "wowthatis!"
        
        dw = tk.Toplevel(app.root)
        dw.title("Dev Mode")
        dw.geometry("400x180")
        dw.configure(bg=app.BG)
        dw.transient(app.root)
        dw.grab_set()
        dw.resizable(False, False)
        
        tk.Label(dw, text="Dev Mode Access", font=("Consolas", 14, "bold"),
                fg=app.ACCENT, bg=app.BG).pack(pady=10)
        
        tk.Label(dw, text="Enter Password:", font=("Consolas", 10),
                fg=app.TEXT, bg=app.BG).pack()
        
        pe = tk.Entry(dw, show="•", font=("Consolas", 10), bg=app.PANEL,
                     fg=app.TEXT, insertbackground=app.TEXT, width=30)
        pe.pack(pady=10)
        pe.focus()
        
        hint = tk.Label(dw, text="", font=("Consolas", 8), fg="#888", bg=app.BG)
        hint.pack()
        
        attempts = [0]
        
        def check():
            entered = pe.get().strip()
            
            if entered == correct:
                dw.destroy()
                DevMode.show_menu(app)
            else:
                attempts[0] += 1
                if attempts[0] >= 2:
                    hint.config(text="Hint: Type carefully, check caps lock")
                messagebox.showerror("Access Denied", f"Incorrect password (Attempt {attempts[0]})")
                pe.delete(0, tk.END)
                pe.focus()
        
        bf = tk.Frame(dw, bg=app.BG)
        bf.pack(pady=10)
        
        tk.Button(bf, text="Enter", command=check, font=("Consolas", 10),
                 bg=app.ACCENT, fg=app.BTN_TXT, activebackground=app.BTN_HOVER,
                 relief="flat", width=15).pack(side="left", padx=5)
        
        tk.Button(bf, text="Cancel", command=dw.destroy, font=("Consolas", 10),
                 bg="#666", fg=app.BTN_TXT, activebackground="#888",
                 relief="flat", width=15).pack(side="left", padx=5)
        
        pe.bind("<Return>", lambda e: check())
    
    @staticmethod
    def show_menu(app):
        """Show dev mode menu"""
        dm = tk.Toplevel(app.root)
        dm.title("Dev Mode Menu")
        dm.geometry("450x550")
        dm.configure(bg=app.BG)
        dm.transient(app.root)
        dm.grab_set()
        
        tk.Label(dm, text="Developer Mode", font=("Consolas", 14, "bold"),
                fg=app.ACCENT, bg=app.BG).pack(pady=15)
        
        c = tk.Canvas(dm, bg=app.BG, highlightthickness=0)
        sb = tk.Scrollbar(dm, orient="vertical", command=c.yview)
        sf = tk.Frame(c, bg=app.BG)
        
        sf.bind("<Configure>", lambda e: c.configure(scrollregion=c.bbox("all")))
        c.create_window((0, 0), window=sf, anchor="nw")
        c.configure(yscrollcommand=sb.set)
        
        c.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        sb.pack(side="right", fill="y")
        
        # Dev functions
        def show_debug():
            info = f"Debug Information:\n\n"
            info += f"Current Step: {app.current_step}\n"
            info += f"Full Health Saved: {app.full_health_saved}\n"
            info += f"Font Size: {app.settings.get('font_size', 'N/A')}\n"
            info += f"Zoom Level: {app.transform.zoom_level}\n"
            messagebox.showinfo("Debug Info", info)
        
        def show_img_stats():
            if not app.full_health_image:
                messagebox.showinfo("Image Stats", "No image loaded")
                return
            
            w, h = app.full_health_image.size
            info = f"Image Statistics:\n\n"
            info += f"Dimensions: {w}x{h} pixels\n"
            info += f"Mode: {app.full_health_image.mode}\n"
            info += f"Has Transparency: Yes (RGBA)\n"
            info += f"Expected Save Size: ~64x64 px\n"
            messagebox.showinfo("Image Stats", info)
        
        def show_paths():
            cwd = os.getcwd()
            info = f"File Paths:\n\n"
            info += f"Working Directory:\n{cwd}\n\n"
            info += f"Skins saved in: {cwd}\n"
            from config import PRESETS_FILE
            info += f"Presets file: {PRESETS_FILE}\n"
            info += f"Preset count: {len(app.presets)}\n"
            messagebox.showinfo("File Paths", info)
        
        def clear_presets():
            if messagebox.askyesno("Clear Presets", "Delete all saved ring presets?"):
                try:
                    app.presets = {}
                    from utils.presets import save_presets
                    from config import PRESETS_FILE
                    save_presets(PRESETS_FILE, app.presets)
                    messagebox.showinfo("Success", "All presets cleared!")
                except Exception as e:
                    messagebox.showerror("Error", f"Could not clear presets:\n{str(e)}")
        
        def reset_settings():
            if messagebox.askyesno("Reset Settings", "Restore all settings to default?"):
                from config import DEFAULT_SETTINGS
                app.settings = DEFAULT_SETTINGS.copy()
                app.apply_all_settings()
                messagebox.showinfo("Success", "Settings reset to default!")
                dm.destroy()
        
        def test_exp():
            if not app.full_health_image:
                messagebox.showinfo("Test Export", "No image loaded")
                return
            
            try:
                img = app.full_health_image.copy()
                img.thumbnail((64, 64), Image.Resampling.LANCZOS)
                app.preview_image = ImageTk.PhotoImage(img)
                app.canvas.delete("all")
                cw = app.canvas.winfo_width() or 800
                ch = app.canvas.winfo_height() or 800
                app.canvas.create_image(cw//2, ch//2, image=app.preview_image)
                messagebox.showinfo("Test Export", "64x64 preview shown on canvas!")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed:\n{str(e)}")
        
        def reset():
            if messagebox.askyesno("Reset", "Reset app to initial state?"):
                try:
                    from steps.end_screen import EndScreen
                    end = EndScreen(app)
                    end.restart()
                    dm.destroy()
                    messagebox.showinfo("Success", "Application reset!")
                except Exception as e:
                    messagebox.showerror("Error", f"Reset failed:\n{str(e)}")
        
        def open_bdce():
            try:
                BDCEEditor.open(app)
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
                     font=("Consolas", 10), bg=app.ACCENT, fg=app.BTN_TXT,
                     activebackground=app.BTN_HOVER, relief="flat",
                     width=30).pack(pady=4)


class BDCEEditor:
    """Broken Dot Creator Editor"""
    
    @staticmethod
    def open(app):
        """Open BDCE editor window"""
        bw = tk.Toplevel(app.root)
        bw.title("BDCE - Broken Dot Creator Editor")
        bw.geometry("1000x800")
        bw.configure(bg=app.BG)
        bw.transient(app.root)
        
        # State
        bw.bg_img = None
        bw.mask = Image.new("L", (512, 512), 255)
        bw.display = None
        bw.brush_sz = 20
        
        # Left: canvas
        lf = tk.Frame(bw, bg=app.BG)
        lf.pack(side="left", fill="both", expand=True)
        
        cc = tk.Frame(lf, bg=app.BG)
        cc.pack(expand=True)
        
        cnv = tk.Canvas(cc, bg="white", width=512, height=512,
                       highlightthickness=2, highlightbackground=app.ACCENT)
        cnv.pack(pady=20, padx=20)
        bw.cnv = cnv
        
        # Right: controls
        rf = tk.Frame(bw, bg=app.PANEL, width=300)
        rf.pack(side="right", fill="y")
        rf.pack_propagate(False)
        
        tk.Label(rf, text="BDCE Tools", font=("Consolas", 14, "bold"),
                fg=app.ACCENT, bg=app.PANEL).pack(pady=20)
        
        tk.Label(rf, text="Create broken dot patterns\nfor damaged health orbs",
                font=("Consolas", 9), fg=app.TEXT, bg=app.PANEL,
                justify="center").pack(pady=5)
        
        tk.Frame(rf, bg="#444444", height=2).pack(fill="x", padx=20, pady=10)
        
        # Functions
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
                      bg=app.ACCENT, fg=app.BTN_TXT, font=("Consolas", 10),
                      relief="flat", width=25, height=2)
        ub.pack(pady=5, padx=10)
        
        # Brush size
        brf = tk.Frame(rf, bg=app.PANEL)
        brf.pack(pady=15, padx=10, fill="x")
        
        tk.Label(brf, text="Brush Size:", fg=app.TEXT, bg=app.PANEL,
                font=("Consolas", 10)).pack(anchor="w")
        
        szl = tk.Label(brf, text="20 px", fg=app.ACCENT, bg=app.PANEL,
                      font=("Consolas", 10, "bold"))
        szl.pack(anchor="e")
        
        def upd_sz(v):
            bw.brush_sz = int(v)
            szl.config(text=f"{v} px")
        
        szs = tk.Scale(brf, from_=1, to=100, orient="horizontal",
                      command=upd_sz, bg=app.PANEL, fg=app.TEXT,
                      troughcolor="#333333", highlightthickness=0)
        szs.set(20)
        szs.pack(fill="x", pady=5)
        
        tk.Label(rf, text="Draw Tools:", fg=app.TEXT, bg=app.PANEL,
                font=("Consolas", 10, "bold")).pack(anchor="w", padx=10, pady=(10,5))
        
        tk.Label(rf, text="• Left Click: Solid\n• Right Click: Spray",
                fg=app.TEXT, bg=app.PANEL, font=("Consolas", 9)).pack(anchor="w", padx=20)
        
        # Bind events
        cnv.bind("<Button-1>", paint_solid)
        cnv.bind("<B1-Motion>", paint_solid)
        cnv.bind("<Button-3>", paint_spray)
        cnv.bind("<B3-Motion>", paint_spray)
        
        tk.Frame(rf, bg="#444444", height=2).pack(fill="x", padx=20, pady=15)
        
        # Action buttons
        clb = tk.Button(rf, text="🗑️ Clear Canvas", command=clear,
                       bg="#666", fg=app.BTN_TXT, font=("Consolas", 10),
                       relief="flat", width=25)
        clb.pack(pady=5, padx=10)
        
        invb = tk.Button(rf, text="🔄 Invert Pattern", command=invert,
                        bg="#666", fg=app.BTN_TXT, font=("Consolas", 10),
                        relief="flat", width=25)
        invb.pack(pady=5, padx=10)
        
        svb = tk.Button(rf, text="💾 SAVE Pattern", command=save,
                       bg="#28a745", fg=app.BTN_TXT, font=("Consolas", 10, "bold"),
                       relief="flat", width=25)
        svb.pack(pady=10, padx=10)
        
        tk.Frame(rf, bg="#444444", height=2).pack(fill="x", padx=20, pady=10)
        
        clsb = tk.Button(rf, text="❌ Close Editor", command=close,
                        bg="#dc3545", fg=app.BTN_TXT, font=("Consolas", 10, "bold"),
                        relief="flat", width=25)
        clsb.pack(pady=10, padx=10)
        
        tk.Label(rf, text="\n💡 Black = broken areas",
                font=("Consolas", 8), fg="#888", bg=app.PANEL).pack(side="bottom", pady=10)
        
        upd_cnv()
