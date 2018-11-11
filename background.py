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

    def blit(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        # self.x -= self.dx                                  # Use dummy variable for decimal Rects to work with Pygame
        self.rect.x = self.x
