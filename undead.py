import pygame
from pygame.sprite import Sprite

class Undead(Sprite):
    """A class to represent a single undead in the horde."""
    
    def __init__(self, ai_game):
        """Initialize the undead and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        # Load the undead image and set its rect attribute.
        self.image = pygame.image.load('images/small_undead.bmp')
        self.rect = self.image.get_rect()

        # Start each new undead near the top left of the screen.
        self.rect.x = self.rect.width 
        self.rect.y = self.rect.height 

        # Store the undead's exact horizontal position.
        self.x = float(self.rect.x)
    
    def update(self):
        """Move the undead right or left."""
        self.x += (self.settings.undead_speed *
            self.settings.horde_direction)
        self.rect.x = self.x

    def check_edges(self):
        """Return True if undead is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True