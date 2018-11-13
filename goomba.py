from mario import Mario
import pygame
from pygame.sprite import Sprite
from map import Map


class Goomba(Sprite):
    def __init__(self,  screen, settings, rect, imglib, soundlib):
        super(Goomba, self).__init__()
        self.map = map
        self.screen = screen
        self.speed_factor = 1  # -1 left +1 right
        self.settings = settings
        self.soundlib = soundlib
        # self.y_mod = 200
        self.dead = False
        self.dead_counter = 0
        self.direction_left = True

        self.images = []
        self.images.append(imglib[0])
        self.images.append(pygame.transform.flip(imglib[0], True, False))
        self.images.append(imglib[1])
        self.image = self.images[0]
        self.rect = rect
        self.screen_rect = screen.get_rect()

        self.rect.x = rect.x
        self.rect.y = rect.y

        # Store a decimal value for the ship's center
        self.center_x = float(self.rect.x)
        self.center_y = float(self.rect.y)

        # Movement flag
        self.moving_right = False
        self.moving_left = True
        # self.moving_up = False
        # self.moving_down = False

    def update(self, mario):
        if mario.rect.x >= self.settings.screenWidth / 2 and mario.vector.x_velocity > 0:
            self.center_x -= mario.vector.x_velocity
        if self.dead:
            if self.dead_counter == 0:
                self.soundlib[1][10].play()
            self.image = self.images[2]
            if self.dead_counter == 60:
                return True
            else:
                self.dead_counter += 1
        elif self.moving_right and self.rect.right < self.screen_rect.right:
            self.center_x += self.speed_factor
        elif self.moving_left:
            self.center_x -= self.speed_factor
            if self.rect.left < -150:
                return True

        # Update rect object from self.center
        self.rect.x = self.center_x
        self.rect.y = self.center_y
        return False

    def flip_img(self):
        if self.dead:
            pass
        elif self.direction_left:
            self.image = self.images[1]
        else:
            self.image = self.images[0]
        self.direction_left = not self.direction_left

    def blitme(self):
        #self.screen.blit(self.image, self.rect)
        if self.rect.right < 0 or self.rect.left > self.settings.screenWidth:
            return
        self.screen.blit(self.image, self.rect)

    def change_direction(self):
        self.moving_left = not self.moving_left
        self.moving_right = not self.moving_right
