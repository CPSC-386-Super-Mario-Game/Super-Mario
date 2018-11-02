import background as b
import gameFunctions as gF
import os
import pygame
import settings as s
import map as m
import time


def main():
    #   Provides consistent window positioning.
    os.environ['SDL_VIDEO_WINDOW_POS'] = '60, 35'
    pygame.init()
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()                                         # Used for FPS + time-tracking

    #   Initial set-up
    settings = s.Settings()
    pygame.display.set_caption(settings.gameTitle)
    screen = pygame.display.set_mode((settings.screenWidth, settings.screenHeight))
    screen.fill(settings.bgColor)

    #   Generate game objects
    image_library = gF.load_image_library()
    background = b.Background(image_library, screen, settings)
    map = m.Map(image_library, screen, settings)

    #   Game loop
    while True:
        background.update()
        background.blit()
        pygame.display.flip()

        clock.tick(settings.FPS)                                        # Locks game at designated FPS


if __name__ == '__main__':
    main()
