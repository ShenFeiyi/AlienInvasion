import os
import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join('.','images','alien.bmp'))
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

    def reach_edge(self, game):
        if (self.rect.right > game.settings.screen_width) or (self.rect.left < 0):
            return True
        else:
            return False

    def update(self, game): 
        #self.rect.x += int(game.settings.fleet_direction * game.roundboard.Round * 0.2)
        self.rect.x += game.settings.fleet_direction
