import background as b
from gameFunctions import GameFunctions
import os
import pygame
import settings as s
import map as m
import time


class main:
    def __init__(self):

        #   Provides consistent window positioning.
        os.environ['SDL_VIDEO_WINDOW_POS'] = '60, 35'
        pygame.init()
        #pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()                                         # Used for FPS + time-tracking

        #   Initial set-up
        self.settings = s.Settings()
        pygame.display.set_caption(self.settings.gameTitle)
        self.screen = pygame.display.set_mode((self.settings.screenWidth, self.settings.screenHeight))
        self.screen.fill(self.settings.bgColor)
        self.gF = GameFunctions(finished = False)

        #   Generate game objects
        self.image_library = self.gF.load_image_library()
        self.background = b.Background(self.image_library, self.screen, self.settings)
        self.map = m.Map(self.image_library, self.screen, self.settings)

    #   Game loop
    def play(self):
        while True:
            while not self.gF.finished:
                self.gF.check_events()
                self.background.update()
                self.background.blit()
                self.map.blitme()  # Alternate loading
                pygame.display.flip()

                self.clock.tick(self.settings.FPS)                                        # Locks game at designated FPS


if __name__ == '__main__':
    game = main()
    game.play()
