import os
import pygame.font

class Button():    
    def __init__(self, game, msg):        
        self.font = pygame.font.Font(os.path.join('.','others','simsun.ttc'),32)

        # 按钮矩形
        self.rect = pygame.Rect(0, 0, 200, 50)
        self.rect.center = game.screen.get_rect().center
        # 按钮文字
        self.msg = msg
        self.text = self.font.render(msg, True, (255,255,255), (0, 0, 255))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center
    
    def draw(self, game):
        # 画背景
        game.screen.fill((0, 0, 255), self.rect)
        # 画背景之上的图片
        game.screen.blit(self.text, self.text_rect)
