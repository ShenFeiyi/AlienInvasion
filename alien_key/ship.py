import os
import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.image = pygame.image.load(os.path.join('.','images','ship.bmp'))
        self.rect = self.image.get_rect()
        self.place_center()
        self.movingx = 0
        self.movingy = 0
        self.speed = 2
    
    def blitme(self):
        self.screen.blit(self.image, self.rect)
    
    def update(self):        
        if (not self.movingx==0) and (0 < self.rect.centerx+self.movingx*(self.rect.width/2+self.speed) < self.screen.get_rect().right):
            self.rect.centerx += self.movingx*self.speed
        if (not self.movingy==0) and (0 < self.rect.centery+self.movingy*(self.rect.height/2+self.speed) < self.screen.get_rect().bottom):
            self.rect.centery += self.movingy*self.speed
    
    def place_center(self):
        self.rect.centerx = self.screen.get_rect().centerx
        self.rect.bottom = self.screen.get_rect().bottom            
