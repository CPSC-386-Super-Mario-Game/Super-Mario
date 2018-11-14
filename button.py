import pygame

class Text():
    def __init__(self, screen, msg, width, height, x, y, color):
        self.font = pygame.font.SysFont(None, 48)
        self.screen = screen

        self.rect = pygame.Rect(x, y, width, height)
        self.msg_image = self.font.render(msg, True, color, (0, 0, 0))

    def draw_text(self):
        self.screen.blit(self.msg_image, self.rect)


class Picture():
    def __init__(self, screen, x, y, image):
        self.screen = screen
        self.x = x
        self.y = y
        self.image = image


    def draw_picture(self):
        self.screen.blit(self.image, (self.x, self.y))