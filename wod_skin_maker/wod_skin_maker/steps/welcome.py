# steps/welcome.py - Welcome Screen (Step 0)

class WelcomeStep:
    def __init__(self, app):
        self.app = app
    
    def show(self):
        """Show welcome screen"""
        self.app.current_step = 0
        self.app.set_instructions(
            "Welcome to WOD Skin Maker! (Version 1.2)\n\n"
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
        self.app.clear_controls()
        self.app.add_button("Next", self.next_step)
        self.app.add_button("Settings", self.app.open_settings)
    
    def next_step(self):
        """Go to full health step"""
        from steps.full_health import FullHealthStep
        self.app.current_step_handler = FullHealthStep(self.app)
        self.app.current_step_handler.show()
