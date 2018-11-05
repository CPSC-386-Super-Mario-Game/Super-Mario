import pygame
import sys

class GameFunctions:
    def __init__(self, finished):
        self.finished = finished

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def load_image_library(self):
        image_lib = [pygame.image.load('images/bg.png'), pygame.image.load('images/background/floor.png'), pygame.image.load('images/mario/mario_small_idle.png')]

        return image_lib

