#!/usr/bin/env python3
# test_imports.py - Test that all imports work correctly

print("Testing imports...")

try:
    print("  ✓ config")
    import config
    
    print("  ✓ utils.image_ops")
    from utils import image_ops
    
    print("  ✓ utils.presets")
    from utils import presets
    
    print("  ✓ tools.circle_crop")
    from tools import circle_crop
    
    print("  ✓ tools.ring_maker")
    from tools import ring_maker
    
    print("  ✓ tools.drawing")
    from tools import drawing
    
    print("  ✓ tools.transform")
    from tools import transform
    
    print("  ✓ steps.welcome")
    from steps import welcome
    
    print("  ✓ steps.full_health")
    from steps import full_health
    
    print("  ✓ steps.medium_health")
    from steps import medium_health
    
    print("  ✓ steps.low_health")
    from steps import low_health
    
    print("  ✓ steps.final_health")
    from steps import final_health
    
    print("  ✓ steps.end_screen")
    from steps import end_screen
    
    print("  ✓ ui.controls")
    from ui import controls
    
    print("  ✓ ui.windows")
    from ui import windows
    
    print("  ✓ app")
    import app
    
    print("\n✅ All imports successful!")
    print("The multi-file structure is ready to use!")
    
except ImportError as e:
    print(f"\n❌ Import error: {e}")
    exit(1)
