import os
import sys
import pygame
from pygame.sprite import Group
from datetime import datetime as dt
from queue import PriorityQueue as PQ

from setting import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from board import Scoreboard, Roundboard, Topboard

import PCF8591 as ADC
from joystick import js_msg, detect_js

class Game():
    def __init__(self):
        ADC.setup(0x48)

        pygame.init()
        self.settings = Settings()        
        self.game_active = False        
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("外星人入侵")
        self.ship = Ship(self)
        self.ship_left = 1
        self.scoreboard = Scoreboard(self)
        self.roundboard = Roundboard(self)
        self.topboard = Topboard(self)
        self.bullets = Group()
        self.aliens = Group()
        self.button = Button(self,'开始')
        self.reset_level()

        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join('.','sound','ready.ogg'))
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play()
        self.sounds = {}
        self.sounds['bomb'] = pygame.mixer.Sound(os.path.join('.','sound','bomb.wav'))
        self.sounds['shoot'] = pygame.mixer.Sound(os.path.join('.','sound','shoot.wav'))
        self.sounds['bomb'].set_volume(0.7)
        self.sounds['shoot'].set_volume(0.7)

        try:
            with open(os.path.join('.','others','records.txt'), 'r') as file:
                content = file.readlines()
            time, score = content[0].split('\t')
            self.highest = int(score)
        except FileNotFoundError:
            self.highest = 0

    def reset_level(self):        
        self.bullets.empty()
        self.aliens.empty()
        self.create_fleet()
        self.ship.place_center()
        self.ship.movingx = 0
        self.ship.movingy = 0
    
    def next_level(self):
        self.roundboard.Round += 1
        self.roundboard.update(self)
        self.ship.speed += 0.1
        self.reset_level()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.QUIT_GAME()
##            elif event.type == pygame.KEYDOWN:
##                self.check_keydown(event.key)
            elif event.type == pygame.KEYUP:
                self.check_keyup(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.check_button(self.button)
        if self.game_active:
            self.stick2key()

    def check_button(self,button):
        mouse = pygame.mouse.get_pos()                        
        if button.msg == '开始':
            self.game_active = True
            self.settings = Settings()
            self.ship_left = 1
            self.scoreboard.reset(self)
            self.roundboard.reset(self)
            self.reset_level()
            pygame.mixer.music.load(os.path.join('.','sound','go.ogg'))
            pygame.mixer.music.set_volume(0.7)
            pygame.mixer.music.play()
        elif button.msg == '结束':
            self.game_active = False
            self.settings = Settings()
            self.ship_left = 1
            self.scoreboard.reset(self)
            self.roundboard.reset(self)
            self.reset_level()
            self.button = Button(self,'开始')
            self.button.draw(self)

    def stick2key(self):
        """Convert stick info to key info
        """
        def left():
            self.ship.movingx = -1
        def right():
            self.ship.movingx = 1
        def up():
            self.ship.movingy = -1
        def down():
            self.ship.movingy = 1
        def attack():
            if len(self.bullets) < 4 + self.roundboard.Round:
                self.sounds['shoot'].play()
                bullet = Bullet(self)
                self.bullets.add(bullet)
        state = detect_js()
        #state =      0     1     2      3      4        5
        #js_msg = ['home','up','down','left','right','pressed']
        switch = {
            'home':    None,
            'up':      up,
            'down':    down,
            'left':    left,
            'right':   right,
            'pressed': attack
            }
        action = switch[js_msg[state]]
        if not action is None:
            action()

##    def calm_down(self):
##        self.ship.movingx, self.ship.movingy = 0, 0

##    def check_keydown(self,key):
##        if key == pygame.K_LEFT:
##            self.ship.movingx = -1
##        elif key == pygame.K_RIGHT:
##            self.ship.movingx = 1
##        elif key == pygame.K_UP:
##            self.ship.movingy = -1
##        elif key == pygame.K_DOWN:
##            self.ship.movingy = 1
##        elif key == pygame.K_SPACE:
##            if len(self.bullets) < 4 + self.roundboard.Round:
##                self.sounds['shoot'].play()
##                bullet = Bullet(self)
##                self.bullets.add(bullet)

    def check_keyup(self,key):
        if key == pygame.K_q:
            if self.game_active:
                self.save_records()
                self.__init__()
            else:
                self.QUIT_GAME()
##        elif key == pygame.K_LEFT and self.ship.movingx == -1:
##            self.ship.movingx = 0
##            if pygame.key.get_pressed()[pygame.K_RIGHT]: # more smoothly
##                self.ship.movingx = 1
##        elif key == pygame.K_RIGHT and self.ship.movingx == 1:
##            self.ship.movingx = 0
##            if pygame.key.get_pressed()[pygame.K_LEFT]:
##                self.ship.movingx = -1
##        elif key == pygame.K_UP and self.ship.movingy == -1:
##            self.ship.movingy = 0
##            if pygame.key.get_pressed()[pygame.K_DOWN]:
##                self.ship.movingy = 1
##        elif key == pygame.K_DOWN and self.ship.movingy == 1:
##            self.ship.movingy = 0
##            if pygame.key.get_pressed()[pygame.K_UP]:
##                self.ship.movingx = -1

    def update_screen(self):
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.blitme(self)
        self.ship.blitme()
        if self.game_active:
            self.aliens.draw(self.screen)
            self.scoreboard.show(self.screen)
            self.roundboard.show(self.screen)
        else:
            self.topboard.show(self.screen)
        if self.ship_left < 1 :
            self.game_active = False
        if not self.game_active:
            self.button.draw(self)
        pygame.display.update()

    def update_sprites(self): 
        self.ship.update()        
        self.update_aliens()
        self.update_bullets()
        self.check_alien_bullet_collision()
        self.check_alien_ship_collision()
        self.check_alien_bottom_collision()

    def update_bullets(self):
        self.bullets.update(self)
        for bullet in self.bullets.copy():
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)  

    def check_alien_bullet_collision(self):
        collisions = pygame.sprite.groupcollide(self.aliens,self.bullets,True,True)
        if collisions:
            self.sounds['bomb'].play()
            for alien in collisions.values():
                self.scoreboard.score += 5*len(alien)
                if self.scoreboard.score > self.highest:
                    pygame.mixer.music.load(os.path.join('.','sound','newhighscore.ogg'))
                    pygame.mixer.music.set_volume(0.7)
                    pygame.mixer.music.play()
                    self.highest = 1e18
                self.scoreboard.update(self)
        if len(self.aliens) == 0:
            pygame.mixer.music.load(os.path.join('.','sound','levelup.ogg'))
            pygame.mixer.music.set_volume(0.7)
            pygame.mixer.music.play()
            self.next_level()
    
    def create_alien(self,col_number,row_number):
        alien = Alien()
        alien.rect.x = alien.x = alien.rect.width + alien.rect.width * col_number
        alien.rect.y = alien.rect.height + alien.rect.height * row_number
        self.aliens.add(alien)
        
    def create_fleet(self):
        alien = Alien()
        fleet_cols = self.get_fleet_cols(self.settings.screen_width,alien.rect.width)
        fleet_rows = self.get_fleet_rows(self.settings.screen_height,alien.rect.height)
        
        for row in range(fleet_rows):
            for col in range(fleet_cols):
                self.create_alien(col,row)
                
    def get_fleet_cols(self,screen_width,width):
        space_x = screen_width - 2 * width
        return int(space_x/width)

    def get_fleet_rows(self,screen_height,height):
        space_y = screen_height - 5 * height
        return int(space_y/height)

    def update_aliens(self):
        self.aliens.update(self)
        self.check_fleet_edge()               
        
    def check_fleet_edge(self):
        for alien in self.aliens.copy():
            if alien.reach_edge(self):
                self.settings.fleet_direction *= -1
                for a in self.aliens:                
                    a.rect.y += (5 + 0.8*self.roundboard.Round)
                break
            
    def lose_aship(self):
        self.ship_left -= 1
        if self.ship_left < 1:
            pygame.time.wait(500)           
            self.button = Button(self,'结束')
            pygame.mixer.music.load(os.path.join('.','sound','gameover.ogg'))
            pygame.mixer.music.set_volume(0.7)
            pygame.mixer.music.play()
        else:                
            self.reset_level()
        self.save_records()
            
    def check_alien_ship_collision(self):
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self.sounds['bomb'].play()
            self.lose_aship()
            
    def check_alien_bottom_collision(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens:
            if alien.rect.bottom >= screen_rect.bottom:              
                self.lose_aship()
                break

    def save_records(self):
        records = PQ()
        # `record.txt` format: %Y-%m-%d %H:%M:%S\tScore
        # 如果有旧的文件
        if os.path.exists(os.path.join('.','others','records.txt')):
            with open(os.path.join('.','others','records.txt'), 'r') as file:
                content = file.readlines()
            for c in content:
                time, score = c.split('\t')
                score = int(score)
                records.put((-score, time))
        # 读取新纪录
        newRecord = self.scoreboard.score
        newTime = dt.now().strftime('%Y-%m-%d %H:%M:%S')
        records.put((-newRecord, newTime))
        # 写入新纪录
        with open(os.path.join('.','others','records.txt'), 'w') as file:
            while not records.empty():
                score, time = records.get()
                score = str(-score)
                file.write(time+'\t'+score+'\n')

    def QUIT_GAME(self):
        pygame.quit()
        sys.exit()
