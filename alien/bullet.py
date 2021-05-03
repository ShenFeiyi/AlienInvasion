import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, game):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 3, 15)
        self.rect.centerx = game.ship.rect.centerx
        self.rect.top = game.ship.rect.top

    def update(self, game):
        self.rect.y -= 1
    
    def blitme(self, game):
        pygame.draw.rect(game.screen, (60,60,60), self.rect)
