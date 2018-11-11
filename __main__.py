import background as b
from gameFunctions import GameFunctions
import os
import pygame
import settings as s
import map as m
import mario as mario


class Main:
    def __init__(self):
        #   Provides consistent window positioning.
        os.environ['SDL_VIDEO_WINDOW_POS'] = '60, 35'
        pygame.init()
        pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()                                         # Used for FPS + time-tracking

        #   Initial set-up
        self.settings = s.Settings()
        pygame.display.set_caption(self.settings.gameTitle)
        self.screen = pygame.display.set_mode((self.settings.screenWidth, self.settings.screenHeight))
        self.screen.fill(self.settings.bgColor)
        self.gF = GameFunctions(finished=False)

        #   Generate game objects
        self.image_library = self.gF.load_image_library()
        self.background = b.Background(self.image_library, self.screen, self.settings)
        self.map = m.Map(self.image_library, self.screen, self.settings)

        self.mario = mario.SmallMario([self.image_library[15], self.image_library[16]], self.screen, self.settings,
                                      self.map.mario_coor[0][0], self.map.mario_coor[0][1])
        self.bricks = self.gF.load_brick_objects(self.image_library[1], self.map.brick_rect, self.screen, self.settings)
        self.blocks = self.gF.load_block_objects(self.image_library[2], self.map.mystery_rect, self.screen,
                                                 self.settings)

    #   Game loop
    def play(self):
        while True:
            while not self.gF.finished:
                self.gF.check_events(self.mario)

                self.background.update()
                self.mario.update()

                self.background.blit()
                self.gF.blit_objects(self.bricks, self.blocks)
                self.mario.blit()
                pygame.display.flip()

                self.gF.check_time(self.blocks)
                self.clock.tick(self.settings.FPS)                                     # Locks game at designated FPS


if __name__ == '__main__':
    game = Main()
    game.play()
