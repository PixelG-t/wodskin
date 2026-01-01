# steps/end_screen.py - End Screen

class EndScreen:
    def __init__(self, app):
        self.app = app
    
    def show(self):
        """Show end screen"""
        self.app.current_step = 5
        self.app.set_instructions(
            "🎉 Congratulations! You've created your WOD skin! 🎉\n\n"
            "How to add it to the game:\n"
            "1. Join the WOD Discord: https://discord.gg/warofdots\n"
            "2. Go into the #suggest channel and make a suggestion.\n"
            "3. Message Thegypt to ask Python (the creator) about your skin and whether it could be added.\n\n"
            "⚠️ Important: Do NOT harass anyone to add your skin.\n\n"
            "Thank you for using WOD Skin Maker!\n"
            "Made by Wowthatp\n\n"
            "Press ESC to exit."
        )
        self.app.clear_controls()
        self.app.add_button("Create Another Skin", self.restart)
    
    def restart(self):
        """Restart the application"""
        # Reset everything
        self.app.current_step = 0
        self.app.full_health_image = None
        self.app.preview_image = None
        self.app.medium_health_image = None
        self.app.low_health_image = None
        self.app.broken_reference = None
        self.app.low_broken_reference = None
        self.app.broken_effect_image = None
        self.app.full_health_saved = False
        self.app.canvas.delete("all")
        
        from steps.welcome import WelcomeStep
        self.app.current_step_handler = WelcomeStep(self.app)
        self.app.current_step_handler.show()
