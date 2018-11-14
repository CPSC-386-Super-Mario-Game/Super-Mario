import vector
import pygame


class Mario:
    def __init__(self, image_lib, screen, settings, x, y, sound_library):
        self.screen = screen
        self.settings = settings
        self.sound_library = sound_library
        self.regular_img_lib = image_lib[0]
        self.invul_img_lib = image_lib[1]

        self.walkIndex = 4
        self.walkInc = 1

        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y

        self.vector = vector.Vector(settings)
        self.blitIndex = 0
        self.rect = self.regular_img_lib[0].get_rect()
        self.rect.x = x
        self.rect.y = y

        self.x_direction = "none"
        self.jumpFlag = "none"
        self.flipped = False

    def update_x(self, bg, floor_rects, brick_rects, block_rects, solid_rects, smallpipe_rects,
                 mediumpipe_rects, largepipe_rects, flag_rects, castle_rects):
        self.vector.update_x_velocity(self.x_direction)
        if self.rect.x >= self.settings.screenWidth / 2 and self.vector.x_velocity > 0:
            popme = "none"
            for index, rect in enumerate(floor_rects):
                x = rect.x
                x -= self.vector.x_velocity
                rect.x = x
                if rect.right < 0:
                    popme = index
            if popme != "none":
                floor_rects.pop(popme)

            for index, rect in enumerate(brick_rects):
                brick_rects[index].rect.x -= self.vector.x_velocity
            for index, rect in enumerate(block_rects):
                block_rects[index].rect.x -= self.vector.x_velocity
            for index, rect in enumerate(solid_rects):
                solid_rects[index].rect.x -= self.vector.x_velocity
            for index, rect in enumerate(smallpipe_rects):
                smallpipe_rects[index].rect.x -= self.vector.x_velocity
            for index, rect in enumerate(mediumpipe_rects):
                mediumpipe_rects[index].rect.x -= self.vector.x_velocity
            for index, rect in enumerate(largepipe_rects):
                largepipe_rects[index].rect.x -= self.vector.x_velocity
            for index, rect in enumerate(flag_rects):
                flag_rects[index].rect.x -= self.vector.x_velocity
            for index, rect in enumerate(castle_rects):
                castle_rects[index].rect.x -= self.vector.x_velocity

            bg.update(self.vector.x_velocity)

        else:
            self.x += self.vector.x_velocity
            self.rect.x = self.x
        return bg

    def update_y(self):
        self.vector.update_y_velocity(self.jumpFlag)
        self.y += self.vector.y_velocity
        self.rect.y = self.y

    def change_direction(self, direction):
        self.x_direction = direction
        self.vector.change_direction(direction)

    def jump(self):
        if self.jumpFlag == "jumping" or self.jumpFlag == "falling":
            return
        else:
            self.jumpFlag = "jumping"
            self.sound_library[1][9].play()
            self.vector.jump()

    def jump_small(self):
        self.jumpFlag = "jumping"
        self.sound_library[1][9].play()
        self.vector.jump_small()

    def blit(self):
        if self.jumpFlag == "jumping" or self.jumpFlag == "falling":
            self.blitIndex = 2
        elif self.x_direction == "right" and self.vector.x_velocity < 0 or \
                self.x_direction == "left" and self.vector.x_velocity > 0:
            self.blitIndex = 1
        elif abs(self.vector.x_velocity) > 0:
            self.screen.blit(self.regular_img_lib[self.walkIndex], self.rect)
            return
        else:
            self.blitIndex = 0
        self.screen.blit(self.regular_img_lib[self.blitIndex], self.rect)

    def change_index(self):
        if self.walkIndex == 3 or self.walkIndex == 5:
            self.walkInc *= -1
        self.walkIndex += self.walkInc

    def flip_direction(self):
        if not self.flipped:
            for i in range(0, 6):
                self.regular_img_lib[i] = pygame.transform.flip(self.regular_img_lib[i], True, False)
                self.flipped = True

    def flip_back(self):
        if self.flipped:
            for i in range(0, 6):
                self.regular_img_lib[i] = pygame.transform.flip(self.regular_img_lib[i], True, False)
                self.flipped = False
    '''
        small_lib = [pygame.image.load('images/mario/small_idle.png'),
                     pygame.image.load('images/mario/small_turn.png'),
                     pygame.image.load('images/mario/small_jump.png'),
                     pygame.image.load('images/mario/small_walk0.png'),
                     pygame.image.load('images/mario/small_walk1.png'),
                     pygame.image.load('images/mario/small_walk2.png'),
                     pygame.image.load('images/mario/small_die.png'),
                     pygame.image.load('images/mario/small_grow.png')]
    '''


class SmallMario(Mario):
    def __init__(self, image_lib, screen, settings, x, y,  sound_library):
        super().__init__(image_lib, screen, settings, x, y,  sound_library)


class BigMario(Mario):
    def __init__(self, image_lib, screen, settings, x, y,  sound_library):
        super().__init__(image_lib, screen, settings, x, y,  sound_library)


class FireMario(BigMario):
    def __init__(self, image_lib, screen, settings, x, y, sound_library):
        super().__init__(image_lib, screen, settings, x, y, sound_library)
