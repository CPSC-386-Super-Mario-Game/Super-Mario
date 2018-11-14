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

        # Stats
        self.score = 0
        self.coins = 0
        self.world = "1-1"
        self.time = 400
        self.lives = 3

        self.font = pygame.font.SysFont(None, 40)
        self.score_text_rect = pygame.Rect(100, 0, 30, 30)
        self.score_text = self.font.render("SCORE", True, (255, 255, 255))
        self.score_rect = pygame.Rect(135, 30, 30, 30)
        self.score_to_text = self.font.render(str(self.score), True, (255, 255, 255))
        self.coins_text_rect = pygame.Rect(400, 0, 30, 30)
        self.coins_text = self.font.render("COINS", True, (255, 255, 255))
        self.coins_rect = pygame.Rect(435, 30, 30, 30)
        self.coins_to_text = self.font.render(str(self.coins), True, (255, 255, 255))
        self.world_text_rect = pygame.Rect(700, 0, 30, 30)
        self.world_text = self.font.render("WORLD", True, (255, 255, 255))
        self.world_rect = pygame.Rect(730, 30, 30, 30)
        self.world_to_text = self.font.render(self.world, True, (255, 255, 255))
        self.time_text_rect = pygame.Rect(1000, 0, 30, 30)
        self.time_text = self.font.render("TIME", True, (255, 255, 255))
        self.time_rect = pygame.Rect(1010, 30, 30, 30)
        self.time_to_text = self.font.render(str(self.time), True, (255, 255, 255))
        self.lives_text_rect = pygame.Rect(1300, 0, 30, 30)
        self.lives_text = self.font.render("LIVES", True, (255, 255, 255))
        self.lives_rect = pygame.Rect(1330, 30, 30, 30)
        self.lives_to_text = self.font.render(str(self.lives), True, (255, 255, 255))



    def blit(self):
        self.screen.blit(self.image, self.rect)

    def blit_score(self):
        self.screen.blit(self.score_text, self.score_text_rect)
        self.screen.blit(self.score_to_text, self.score_rect)
        self.screen.blit(self.coins_text, self.coins_text_rect)
        self.screen.blit(self.coins_to_text, self.coins_rect)
        self.screen.blit(self.world_text, self.world_text_rect)
        self.screen.blit(self.world_to_text, self.world_rect)
        self.screen.blit(self.time_text, self.time_text_rect)
        self.screen.blit(self.time_to_text, self.time_rect)
        self.screen.blit(self.lives_text, self.lives_text_rect)
        self.screen.blit(self.lives_to_text, self.lives_rect)
    def ugblit(self):
        self.screen.blit(self.ugimage, self.rect)

    def update(self, x_value):
        self.x = self.rect.x
        self.x -= x_value
        self.rect.x = self.x
