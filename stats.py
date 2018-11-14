import pygame

class Score:
    def __init__(self, screen):
        self.screen = screen
        # Stats
        self.score_progression = [100, 200, 400, 500, 800, 1000, 2000, 4000, 5000, 8000]
        self.score_progression_index = 0
        self.score = 0
        self.coins = 0
        self.world = "1-1"
        self.time = 400
        self.lives = 3

        self.font = pygame.font.SysFont(None, 40)
        self.score_text_rect = pygame.Rect(100, 0, 30, 30)
        self.score_text = self.font.render("SCORE", True, (255, 255, 255))
        self.score_rect = pygame.Rect(120, 30, 30, 30)
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

    def blit_score(self):
        self.score_to_text = self.font.render(str(self.score), True, (255, 255, 255))
        self.coins_to_text = self.font.render(str(self.coins), True, (255, 255, 255))
        self.time_to_text = self.font.render(str(self.time), True, (255, 255, 255))
        self.lives_to_text = self.font.render(str(self.lives), True, (255, 255, 255))
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