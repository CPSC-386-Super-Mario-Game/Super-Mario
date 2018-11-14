import pygame


class Background:
    def __init__(self, image_library, screen, settings):
        self.screen = screen
        self.settings = settings
        self.image_lib = image_library[0]

        self.image = self.image_lib[0]
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = settings.topOfGame                     # Stores where top of game is.

        # Movement Settings
        self.x = self.rect.x
        self.y = self.rect.y
        self.dx = 1

        self.ugimage = pygame.Surface(screen.get_size())
        self.ugimage.fill((0, 0, 0))

        #self.image = pygame.Surface(screen.get_size())
        #self.image.fill((0, 0, 0))

        # Frame of Reference
        self.floor_begin = 0
        self.floor_end = 20



    def blit(self):
        self.screen.blit(self.image, self.rect)

    def ugblit(self):
        self.screen.blit(self.ugimage, self.rect)

    def update(self, x_value):
        self.x = self.rect.x
        self.x -= x_value
        self.rect.x = self.x
