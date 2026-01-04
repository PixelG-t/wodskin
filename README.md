# WOD Skin Maker v1.2

A tool for creating custom skins for War of the Dots game.

**Created by:** Wowthatp

## Features

- **Full Health Orb Creation**: Load, crop, add rings, draw, and transform images
- **Circle Crop Tool**: Interactive circle cropping with adjustable size
- **Ring Maker**: Add customizable colored rings with thickness control
- **Drawing Tools**: Brush and eraser for fine-tuning
- **Transform Tools**: Flip horizontal/vertical, rotate 90°, zoom in/out
- **Broken Effect Creator**: Apply broken dot patterns for damaged health states
- **BDCE (Broken Dot Creator Editor)**: Create custom broken patterns
- **Settings**: Customizable themes, button sizes, fonts, and more
- **Developer Mode**: Debug tools and advanced features
- **Preset System**: Save and load ring configurations

## Installation

### Requirements
- Python 3.7 or higher
- Pillow (PIL) library
- tkinter (usually comes with Python)

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

```bash
python main.py
```

### Creating a Skin

1. **Welcome Screen**: Read the naming conventions and instructions
2. **Step 1 - Full Health Orb**:
   - Load your 256x256 image 
   - Use Circle Crop to crop to a circle
   - Add Ring to add a colored border
   - Use Draw Tools for fine adjustments
   - Save your image
3. **Step 2 - Medium Health Orb**:
   - Upload your full health orb
   - Upload a broken dot reference pattern
   - Use Eraser Tool to clean up artifacts (optional)
   - Save the 200x200 result
4. **Step 2.1 - Low Health Orb**:
   - Same process as Step 2 with a different broken pattern
5. **Step 2.2 - Final Full Health**:
   - Upload and save final full health at 64x64

### Keyboard Shortcuts

- `Ctrl+D`: Open Developer Mode
- `Ctrl++`/`Ctrl+=`: Zoom In
- `Ctrl+-`: Zoom Out
- `ESC`: Exit Application

### File Naming Convention

**Infantry:**
- Full health: `if_SKINNAME`
- Medium health: `if2_SKINNAME`
- Low health: `if3_SKINNAME`

**Tank:**
- Full health: `tank1_SKINNAME`
- Medium health: `tank2_SKINNAME`
- Low health: `tank3_SKINNAME`

## Project Structure

```
wod_skin_maker/
├── main.py                 # Entry point
├── app.py                  # Main application class
├── config.py               # Configuration and constants
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── ui/
│   ├── __init__.py
│   ├── controls.py        # UI helper methods
│   └── windows.py         # Settings, dev mode, BDCE windows
├── tools/
│   ├── __init__.py
│   ├── circle_crop.py     # Circle cropping tool
│   ├── ring_maker.py      # Ring maker tool
│   ├── drawing.py         # Drawing and eraser tools
│   └── transform.py       # Flip, rotate, zoom tools
├── steps/
│   ├── __init__.py
│   ├── welcome.py         # Welcome screen
│   ├── full_health.py     # Step 1
│   ├── medium_health.py   # Step 2
│   ├── low_health.py      # Step 2.1
│   ├── final_health.py    # Step 2.2
│   └── end_screen.py      # Completion screen
└── utils/
    ├── __init__.py
    ├── image_ops.py       # Image processing utilities
    └── presets.py         # Preset management
```

## Developer Mode

Access with password: `wowthatis!`

Features:
- Show debug information
- View image statistics
- Show file paths
- Clear all presets
- Reset settings
- Test 64x64 export
- Open BDCE (Broken Dot Creator Editor)
- Reset application



**⚠️ Important:** Do NOT harass anyone to add your skin.

## License

Created by Wowthatp for the War of the Dots community.

## Credits

- **Author**: Wowthatp
- **Game**: War of the Dots by Tea and Python


