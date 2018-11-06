import pygame
import sys

class GameFunctions:
    def __init__(self, finished):
        self.finished = finished
        self.image_lib = [pygame.image.load('images/bg.png'), pygame.image.load('images/background/floor.png'),
                     pygame.image.load('images/mario/mario_small_idle.png'), pygame.image.load('images/background/tile.png'),
                          pygame.image.load('images/background/brick.png'), pygame.image.load('images/enemies/goomba.png'),
                          pygame.image.load('images/enemies/koopa0.png')]

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

