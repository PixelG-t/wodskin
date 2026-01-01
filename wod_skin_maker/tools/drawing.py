# tools/drawing.py - Drawing and Eraser Tools

import tkinter as tk
from PIL import ImageDraw

class DrawingTool:
    def __init__(self, app):
        self.app = app
        self.drawing_enabled = False
        self.drawing_tool = "brush"
        self.brush_size = 5
    
    def start(self):
        """Start drawing mode"""
        if not self.app.full_health_image:
            self.app.show_error("Load an image first!")
            return
        
        self.drawing_enabled = True
        self.app.set_instructions(
            "Drawing Mode:\n- Left-click to draw/erase\n- Adjust brush size\n- Select tool and click Done"
        )
        self.app.clear_controls()
        
        tk.Label(self.app.control_frame, text="Tool:", font=("Consolas", 10),
                fg=self.app.TEXT, bg=self.app.PANEL).pack()
        
        tool_var = tk.StringVar(value="brush")
        tk.Radiobutton(self.app.control_frame, text="Brush (Draw)", variable=tool_var,
                      value="brush", command=lambda: setattr(self, 'drawing_tool', 'brush'),
                      bg=self.app.PANEL, fg=self.app.TEXT, selectcolor=self.app.PANEL).pack(anchor="w")
        tk.Radiobutton(self.app.control_frame, text="Eraser", variable=tool_var,
                      value="eraser", command=lambda: setattr(self, 'drawing_tool', 'eraser'),
                      bg=self.app.PANEL, fg=self.app.TEXT, selectcolor=self.app.PANEL).pack(anchor="w")
        
        tk.Label(self.app.control_frame, text="Brush Size:", font=("Consolas", 10),
                fg=self.app.TEXT, bg=self.app.PANEL).pack(pady=(10,5))
        
        ss = tk.Scale(self.app.control_frame, from_=1, to=30, orient="horizontal",
                     command=lambda v: setattr(self, 'brush_size', int(v)),
                     bg=self.app.PANEL, fg=self.app.TEXT, troughcolor="#333333", 
                     highlightthickness=0)
        ss.set(5)
        ss.pack(pady=5)
        
        self.app.canvas.bind("<B1-Motion>", self.draw_on_canvas)
        self.app.canvas.bind("<Button-1>", self.draw_on_canvas)
        
        self.app.add_button("Done", self.finish)
    
    def draw_on_canvas(self, event):
        """Draw or erase on canvas"""
        if not self.app.full_health_image or not self.drawing_enabled:
            return
        
        cw = self.app.canvas.winfo_width() or 800
        ch = self.app.canvas.winfo_height() or 800
        iw, ih = self.app.full_health_image.size
        
        x = int((event.x - cw/2) * iw / cw + iw/2)
        y = int((event.y - ch/2) * ih / ch + ih/2)
        
        if 0 <= x < iw and 0 <= y < ih:
            draw = ImageDraw.Draw(self.app.full_health_image)
            sz = self.brush_size
            
            if self.drawing_tool == "brush":
                draw.ellipse([x-sz, y-sz, x+sz, y+sz], fill=(0,0,0,255))
            else:
                draw.ellipse([x-sz, y-sz, x+sz, y+sz], fill=(0,0,0,0))
            
            self.app.update_preview(self.app.full_health_image)
    
    def finish(self):
        """Finish drawing mode"""
        self.drawing_enabled = False
        self.app.canvas.unbind("<B1-Motion>")
        self.app.canvas.unbind("<Button-1>")
        self.app.current_step_handler.show()


class EraserTool:
    def __init__(self, app):
        self.app = app
        self.eraser_enabled = False
        self.eraser_size = 15
        self.last_eraser_pos = None
    
    def start(self, step_num):
        """Start eraser tool for broken effects"""
        if not self.app.broken_effect_image:
            self.app.show_error("Load a broken reference first!")
            return
        
        self.eraser_enabled = True
        self.step_num = step_num
        
        self.app.set_instructions(
            "Eraser Tool:\n- Draw on canvas to erase\n- Click 'Done Erasing' when finished"
        )
        
        self.app.canvas.bind("<Button-1>", self.on_press)
        self.app.canvas.bind("<B1-Motion>", self.on_drag)
        self.app.canvas.bind("<ButtonRelease-1>", self.on_release)
        
        self.app.clear_controls()
        self.app.add_button("Eraser Size -", lambda: self.adjust_size(-2))
        self.app.add_button("Eraser Size +", lambda: self.adjust_size(2))
        self.size_label = tk.Label(self.app.control_frame, text=f"Size: {self.eraser_size}px",
                fg=self.app.TEXT, bg=self.app.PANEL)
        self.size_label.pack()
        self.app.add_button("Done Erasing", self.stop)
    
    def adjust_size(self, delta):
        """Adjust eraser size"""
        self.eraser_size = max(5, min(50, self.eraser_size + delta))
        self.size_label.config(text=f"Size: {self.eraser_size}px")
    
    def on_press(self, event):
        """Record starting position"""
        self.last_eraser_pos = (event.x, event.y)
    
    def on_drag(self, event):
        """Erase as mouse drags"""
        if not self.app.broken_effect_image or not self.eraser_enabled:
            return
        
        cw = self.app.canvas.winfo_width() or 800
        ch = self.app.canvas.winfo_height() or 800
        iw, ih = self.app.broken_effect_image.size
        
        xr = iw / cw
        yr = ih / ch
        
        x = int((event.x - cw//2) * xr + iw//2)
        y = int((event.y - ch//2) * yr + ih//2)
        
        x = max(0, min(iw - 1, x))
        y = max(0, min(ih - 1, y))
        
        draw = ImageDraw.Draw(self.app.broken_effect_image)
        draw.ellipse((x - self.eraser_size//2, y - self.eraser_size//2,
                     x + self.eraser_size//2, y + self.eraser_size//2),
                    fill=(0, 0, 0, 0))
        
        self.app.update_preview(self.app.broken_effect_image)
    
    def on_release(self, event):
        """Clear last position"""
        self.last_eraser_pos = None
    
    def stop(self):
        """Stop eraser mode"""
        self.app.canvas.unbind("<Button-1>")
        self.app.canvas.unbind("<B1-Motion>")
        self.app.canvas.unbind("<ButtonRelease-1>")
        self.eraser_enabled = False
        
        self.app.show_info("Erasing complete!")
        
        # Return to appropriate step
        if self.step_num == 2:
            from steps.medium_health import MediumHealthStep
            self.app.current_step_handler = MediumHealthStep(self.app)
        elif self.step_num == 3:
            from steps.low_health import LowHealthStep
            self.app.current_step_handler = LowHealthStep(self.app)
        
        self.app.current_step_handler.show()
