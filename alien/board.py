import os
import pygame

class Scoreboard():
    def __init__(self, game):       
        self.font = pygame.font.Font(os.path.join('.','others','simsun.ttc'),30)
        self.reset(game)        

    def reset(self, game):
        self.score = 0        
        self.update(game)
    
    def update(self, game):        
        score = "得分:{:,}".format(self.score)
        self.score_ = self.font.render(score, True, (0,0,150), game.settings.bg_color)                                
        self.score_rect = self.score_.get_rect()
        self.score_rect.right = game.screen.get_rect().right - 0.02 * game.settings.screen_height
        self.score_rect.top = game.screen.get_rect().top + 0.02 * game.settings.screen_height
    
    def show(self, screen):
        screen.blit(self.score_, self.score_rect)

class Roundboard():
    def __init__(self, game):       
        self.font = pygame.font.Font(os.path.join('.','others','simsun.ttc'),30)
        self.reset(game)        

    def reset(self, game):
        self.Round = 1
        self.update(game)
    
    def update(self, game):        
        Round = "第{:,}关".format(self.Round)
        self.Round_ = self.font.render(Round, True, (0,0,150), game.settings.bg_color)                                
        self.Round_rect = self.Round_.get_rect()
        self.Round_rect.center = game.screen.get_rect().center
        self.Round_rect.top = game.screen.get_rect().top + 0.02 * game.settings.screen_height
    
    def show(self, screen):
        screen.blit(self.Round_, self.Round_rect)

class Topboard():
    def __init__(self, game):       
        self.font = pygame.font.Font(os.path.join('.','others','simsun.ttc'),20)
        self.reset(game)        

    def reset(self, game):
        self.update(game)
    
    def update(self, game):
        tops = []
        try:
            with open(os.path.join('.','others','records.txt'), 'r') as file:
                content = file.readlines()
            for c in content:
                time, score = c.split('\t')
                tops.append((score, time))
        except FileNotFoundError:
            pass

        self.tops_ = []
        self.tops_rect = []
        for itop, top in enumerate(tops):
            if itop < 7:
                score, time = top
                t = str(itop+1) + '.' + (9-len(str(itop+1))-len(score))*' ' + score + '\t' + time
                top_ = self.font.render(t, True, (0,0,150), game.settings.bg_color)
                top_rect = top_.get_rect()
                top_rect.center = game.screen.get_rect().center
                top_rect.top = game.screen.get_rect().top + 20 * itop + 0.1 * game.settings.screen_height
                self.tops_.append(top_)
                self.tops_rect.append(top_rect)
    
    def show(self, screen):
        for i in range(len(self.tops_)):
            screen.blit(self.tops_[i], self.tops_rect[i])
