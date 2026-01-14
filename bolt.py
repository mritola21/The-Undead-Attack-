import pygame
from pygame.sprite import Sprite

class Bolt(Sprite):
    """A class to manage bolts thrown by the paladin."""

    def __init__(self, ai_game):
        """Create a bolt object at the paladin's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the bolt image and scale it to the bolt size.
        image = pygame.image.load('images/bolt.bmp')
        self.image = pygame.transform.scale(image, (self.settings.bolt_width, self.settings.bolt_height))
        self.rect = self.image.get_rect()
        self.rect.midtop = ai_game.paladin.rect.midtop
        
        # Store the bolt's position as a decimal value.
        self.y = float(self.rect.y)
    
    def update(self):
        """Move the bolt up the screen."""
        # Update the decimal position of the bolt.
        self.y -= self.settings.bolt_speed
        # Update the rect position.
        self.rect.y = self.y

    def draw_bolt(self):
        """Draw the bolt to the screen."""
        self.screen.blit(self.image, self.rect)