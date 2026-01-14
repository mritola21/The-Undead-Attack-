class Settings:
    """A class to store all settings for The Undead Attack!."""
 
    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (128, 128, 128)

        # Paladin settings
        self.paladin_limit = 3

        # Bolt settings
        self.bolt_width = 18
        self.bolt_height = 51
        self.bolts_allowed = 3

        # Undead settings
        self.horde_drop_speed = 10

        # Raindrop settings
        self.raindrop_speed = 1

        # How quickly the game speeds up
        self.speedup_scale = 1.2

        # How quickly the undead point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.paladin_speed = 1
        self.bolt_speed = 2.0
        self.undead_speed = 0.6
 
        # horde_direction of 1 represents right; -1 represents left.
        self.horde_direction = 1

        # Scoring
        self.undead_points = 50

    def increase_speed(self):
        """Increase speed settings and undead point values."""
        self.paladin_speed *= self.speedup_scale
        self.bolt_speed *= self.speedup_scale
        self.undead_speed *= self.speedup_scale

        self.undead_points = int(self.undead_points * self.score_scale)
        print(self.undead_points)