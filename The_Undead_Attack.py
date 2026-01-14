import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from paladin import Paladin  
from bolt import Bolt 
from undead import Undead  
from raindrop import Raindrop
from random import randint

class TheUndeadAttack:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()
        self.stats = GameStats(self)

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("The Undead Attack!")  

        # Create an instance to store game statistics and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.paladin = Paladin(self)  
        self.bolts = pygame.sprite.Group()  
        self.undeads = pygame.sprite.Group()  
        self.raindrops = pygame.sprite.Group()
        
        self._create_horde()

        # Make the Play button.
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            
            if self.stats.game_active:
                self.paladin.update()  
                self._update_bolts()  
                self._update_raindrops()
                self._create_raindrop()
                self._update_undeads()  

            self._update_screen()

    def _update_bolts(self):  
        """Update position of bolts and get rid of old bolts."""  
        # Update bolt positions.
        self.bolts.update() 
        
        # Get rid of bolts that have disappeared.
        for bolt in self.bolts.copy():  
            if bolt.rect.bottom <= 0:
                self.bolts.remove(bolt) 
        
        self._check_bolt_undead_collisions()  

    def _check_bolt_undead_collisions(self):  
        """Respond to bolt-undead collisions."""  
        # Remove any bolts and undeads that have collided.
        collisions = pygame.sprite.groupcollide(
            self.bolts, self.undeads, True, True)  
        
        if collisions:
            for undeads in collisions.values():  
                self.stats.score += self.settings.undead_points * len(undeads)  
            self.sb.prep_score()
            self.sb.check_high_score()
        
        if not self.undeads:  
            # Destroy existing bolts and create new horde.
            self.bolts.empty()  
            self._create_horde()
            self.settings.increase_speed()
        
            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()

    def _update_raindrops(self):
        """Update position of raindrops and get rid of old raindrops."""
        # Update raindrop positions.
        self.raindrops.update()
        
        # Get rid of raindrops that have disappeared.
        for raindrop in self.raindrops.copy():
            if raindrop.rect.top >= self.settings.screen_height:
                self.raindrops.remove(raindrop)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                
    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.paladin.moving_right = True  
        elif event.key == pygame.K_LEFT:
            self.paladin.moving_left = True 
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bolt()  
    
    def _fire_bolt(self):  
        """Create a new bolt and add it to the bolts group.""" 
        if len(self.bolts) < self.settings.bolts_allowed: 
            new_bolt = Bolt(self)  
            self.bolts.add(new_bolt) 
        
    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.paladin.moving_right = False  
        elif event.key == pygame.K_LEFT:
            self.paladin.moving_left = False  

        
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""

        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        self.paladin.blitme()  
        for bolt in self.bolts.sprites():  
            bolt.draw_bolt()  
        self.undeads.draw(self.screen)  

        # Draw the score information.
        self.sb.show_score()

        self.raindrops.draw(self.screen)

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()
        
        # Make the most recently drawn screen visible.
        pygame.display.flip()
    
    def _create_horde(self):
        """Create a horde of undeads."""  
        # Create an undead and find the number of undeads in a row. 
        # Spacing between each undead is equal to one undead width.  
        undead = Undead(self)  
        undead_width, undead_height = undead.rect.size  
        available_space_x = self.settings.screen_width - (2 * undead_width)  
        number_undeads_x = available_space_x // (2 * undead_width)  
 
        # Determine the number of rows of undeads that fit on the screen. 
        paladin_height = self.paladin.rect.height  
        available_space_y = (self.settings.screen_height - (3 * undead_height) - paladin_height)  
        
        number_rows = available_space_y // (undead_height)  
 
        # Create the full horde of undeads.  
        for row_number in range(number_rows):
            for undead_number in range(number_undeads_x): 
                self._create_undead(undead_number, row_number)  
    
    def _create_undead(self, undead_number, row_number):  
        """Create an undead and place it in the row.""" 
        undead = Undead(self)  
        undead_width, undead_height = undead.rect.size  
        undead.x = undead_width + 2 * undead_width * undead_number + randint(-50, 50)  
        
        undead.x = max(undead_width, min(undead.x, self.settings.screen_width - undead_width))  
        undead.rect.x = undead.x  
        undead.rect.y = undead.rect.height + 2 * undead.rect.height * row_number + randint(-50, 50)  
        self.undeads.add(undead)  
    
    def _create_raindrop(self):
        """Create a new raindrop at random intervals."""
        if randint(1, 100) < 5:  # About 5% chance each frame
            new_raindrop = Raindrop(self)
            self.raindrops.add(new_raindrop)
    
    def _update_undeads(self):  
        """
        Check if the horde is at an edge,
        then update the positions of all undeads in the horde.  
        """
        self._check_horde_edges()
        self.undeads.update() 

        # Look for undead-paladin collisions.  
        if pygame.sprite.spritecollideany(self.paladin, self.undeads):  
            self._paladin_hit()  
        
        # Look for undeads hitting the bottom of the screen.  
        self._check_undeads_bottom() 

    def _check_horde_edges(self):
        """Respond appropriately if any undeads have reached an edge."""  
        for undead in self.undeads.sprites(): 
            if undead.check_edges(): 
                self._change_horde_direction()
                break
 
    def _change_horde_direction(self):
        """Drop the entire horde and change the horde's direction."""
        for undead in self.undeads.sprites():  
            undead.rect.y += self.settings.horde_drop_speed  
        self.settings.horde_direction *= -1

    def _paladin_hit(self):  
        """Respond to the paladin being hit by an undead."""  
        if self.stats.paladins_left > 0:  
            # Decrement paladins_left, and update scoreboard.
            self.stats.paladins_left -= 1
            self.sb.prep_paladins()

            # Get rid of any remaining undeads and bolts.  
            self.undeads.empty()  
            self.bolts.empty()  

            # Create a new horde and center the paladin.  
            self._create_horde()
            self.paladin.center_paladin()  

            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)  # Show cursor when game ends

    def _check_undeads_bottom(self):  
        """Check if any undeads have reached the bottom of the screen."""  
        screen_rect = self.screen.get_rect()
        for undead in self.undeads.sprites():  
            if undead.rect.bottom >= screen_rect.bottom:  
                # Treat this the same as if the paladin got hit. 
                self._paladin_hit() 
                break

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()
            
            # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_paladins()
          
            # Get rid of any remaining undeads and bolts. 
            self.undeads.empty()  
            self.bolts.empty()  
 
            # Create a new horde and center the paladin.  
            self._create_horde()
            self.paladin.center_paladin()  # Assuming method renamed in Paladin class

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = TheUndeadAttack()
    ai.run_game()