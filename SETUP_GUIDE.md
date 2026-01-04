# Setup Guide - WOD Skin Maker


## What Changed?
nothing so far

## File Structure

.
wod_skin_maker/
├── main.py                 #  Start here - run this file
├── app.py                  # Main application class
├── config.py               # All colors, settings, constants
├── requirements.txt        # Dependencies (just Pillow)
├── README.md              # Full documentation
│
├── ui/                     # User Interface
│   ├── controls.py        # Button, label helpers
│   └── windows.py         # Settings, Dev Mode, BDCE
│
├── tools/                  # All the tools
│   ├── circle_crop.py     # Circle cropping
│   ├── ring_maker.py      # Ring creation
│   ├── drawing.py         # Drawing & eraser
│   └── transform.py       # Flip, rotate, zoom
│
├── steps/                  # Each workflow step
│   ├── welcome.py         # Welcome screen
│   ├── full_health.py     # Step 1
│   ├── medium_health.py   # Step 2
│   ├── low_health.py      # Step 2.1
│   ├── final_health.py    # Step 2.2
│   └── end_screen.py      # Completion
│
└── utils/                  # Utilities
    ├── image_ops.py       # Image processing
    └── presets.py         # Preset saving/loading


## How to Run

go on github (https://github.com/PixelG-t/wodskin) and click on code and download zip 

extract the zip and run main.py




## Installation

1. **Install Python** (if not installed)
   - Download from https://python.org
   - Make sure to check "Add to PATH"

2. **Install Pillow**
   
   pip install Pillow
   
   
   Or use requirements.txt:

   cd wod_skin_maker
   pip install -r requirements.txt
   

3. **Run the app**
 
   python main.py
   


## Troubleshooting

### "No module named 'tkinter'"
- **Windows**: tkinter comes with Python
- **Linux**: `sudo apt-get install python3-tk`
- **Mac**: tkinter comes with Python

### "No module named 'PIL'"

pip install Pillow

### "ModuleNotFoundError: No module named 'config'"
Make sure you're running from the `wod_skin_maker` directory:

cd wod_skin_maker
python main.py
```

## Next Steps

1. Test the app: `python main.py`
2. Try all the tools
3. Check Dev Mode (Ctrl+SHift+W, password: wowthatis!)
4. Create a skin!


 Questions?

 ask on the WOD Discord! or dm me on discord username is (wowthatp)

Made with  by Wowthatp

