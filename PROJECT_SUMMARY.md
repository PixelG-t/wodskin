# WOD Skin Maker



### Key Improvements

#### 1. **Organization** 
- Each feature in its own file
- Logical grouping by functionality
- Clear separation of concerns

#### 2. **Maintainability** 
- Easy to find and modify code
- No more scrolling through 1,240 lines
- Each file has single responsibility

#### 3. **Collaboration** 
- Multiple developers can work simultaneously
- Clear module boundaries
- Version control friendly (git diff works better)

#### 4. **Reusability** 
- Tools can be imported into other projects
- Utility functions are standalone
- No code duplication

#### 5. **Testing** 
- Each module can be tested independently
- Clear interfaces between components
- Easier to write unit tests



### How to Use

1. **Extract** the wod_skin_maker folder
2. **Install** dependencies: `pip install -r requirements.txt`
3. **Run**: `python main.py`

That's it! Everything works exactly the same, but the code is now much cleaner.



### File Organization Map

```

─────────────────────────────────────────────────────────
Colors/Constants    → config.py
Settings System     → config.py + app.py
UI Helpers          → ui/controls.py
Settings Window     → ui/windows.py
Dev Mode            → ui/windows.py
BDCE Editor         → ui/windows.py
Circle Crop         → tools/circle_crop.py
Ring Maker          → tools/ring_maker.py
Drawing Tools       → tools/drawing.py
Eraser Tool         → tools/drawing.py
Transform Tools     → tools/transform.py
Welcome Screen      → steps/welcome.py
Full Health Step    → steps/full_health.py
Medium Health Step  → steps/medium_health.py
Low Health Step     → steps/low_health.py
Final Health Step   → steps/final_health.py
End Screen          → steps/end_screen.py
Image Processing    → utils/image_ops.py
Preset Management   → utils/presets.py
Main Application    → app.py
Entry Point         → main.py
```





 Support
Join WOD Discord: https://discord.gg/warofdots
GitHub: https://github.com/PixelG-t/wodskin
discord username: wowthatp 


Made by: Wowthat

Approve by: Tea and Python 
