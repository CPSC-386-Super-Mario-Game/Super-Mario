import pygame
from settings import Settings
import sys
from button import Picture
from button import Text
class MenuLoop:
    def __init__(self, screen, stats, finished, highscore_screen):
        self.settings = Settings()
        self.finished = finished
        self.screen = screen
        self.title_img = Picture(self.screen, 60, 50, pygame.image.load('images/title.png'))
        self.play_button_img_loc = pygame.image.load('images/play_button.png')
        self.play_button_img = Picture(self.screen, 200, 500, self.play_button_img_loc)
        self.play_button_rect = self.play_button_img_loc.get_rect()
        self.play_button_rect.x = 200
        self.play_button_rect.y = 500
        self.highscore_button_img_loc = pygame.image.load('images/highscore_img.png')
        self.highscore_button_img = Picture(self.screen, 200, 550, self.highscore_button_img_loc)
        self.highscore_button_rect = self.highscore_button_img_loc.get_rect()
        self.highscore_button_rect.x = 200
        self.highscore_button_rect.y = 550
        self.highscore_screen = highscore_screen

        self.score_img = Picture(self.screen, 240, 50, pygame.image.load('images/score.png'))
        self.back_img_loc = pygame.image.load('images/go_back.png')
        self.back_img = Picture(self.screen, 220, 550, self.back_img_loc)
        self.back_rect = self.back_img_loc.get_rect()
        self.back_rect.x = 220
        self.back_rect.y = 550

        self.score_number_img = Text(self.screen, str(stats.high_score), 50, 50, 240, 100, (255, 255, 255))

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_xy = pygame.mouse.get_pos()
                if self.play_button_rect.collidepoint(mouse_xy):
                    self.finished = True
                if self.highscore_button_rect.collidepoint(mouse_xy):
                    self.highscore_screen = True
    def check_highscore_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_xy = pygame.mouse.get_pos()
                if self.back_rect.collidepoint(mouse_xy):
                    self.highscore_screen = False
    def update(self):
        self.blitme()
    def update_highscore_screen(self):
        self.blit2()
    def blitme(self):
        self.title_img.draw_picture()
        self.play_button_img.draw_picture()
        self.highscore_button_img.draw_picture()
    def blit2(self):
        self.score_img.draw_picture()
        self.back_img.draw_picture()
        self.score_number_img.draw_text()