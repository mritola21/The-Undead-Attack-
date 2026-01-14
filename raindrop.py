import pygame
from pygame.sprite import Sprite
from random import randint

class Raindrop(Sprite):
    """A class to represent a single raindrop."""

    def __init__(self, ai_game):
        """Initialize the raindrop and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the raindrop image and set its rect attribute.
        self.image = pygame.image.load('images/waterdrop.bmp')
        self.image.set_alpha(150)  # Make it semi-transparent so it appears over other objects
        self.rect = self.image.get_rect()

        # Start each new raindrop at a random position at the top of the screen.
        self.rect.x = randint(0, self.settings.screen_width - self.rect.width)
        self.rect.y = randint(-100, -10)  # Start above the screen

        # Store the raindrop's exact vertical position.
        self.y = float(self.rect.y)

    def update(self):
        """Move the raindrop down the screen."""
        # Update the decimal position of the raindrop.
        self.y += self.settings.raindrop_speed
        # Update the rect position.
        self.rect.y = self.y