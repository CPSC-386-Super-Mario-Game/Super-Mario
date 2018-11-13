import vector


class Mario:
    def __init__(self, image_lib, screen, settings, x, y, sound_library):
        self.screen = screen
        self.settings = settings
        self.sound_library = sound_library
        self.original_x = x
        self.original_y = y
        self.vector = vector.Vector(settings)
        self.regular_img_lib = image_lib[0]
        self.invul_img_lib = image_lib[1]

        self.x = x
        self.y = y
        self.image = self.regular_img_lib[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.x_direction = "none"
        self.jumpFlag = "none"

    def update(self):
        self.vector.update_x_velocity(self.x_direction)
        self.vector.update_y_velocity(self.jumpFlag)
        self.x += self.vector.x_velocity
        self.y += self.vector.y_velocity
        if self.y >= 800:
            self.jumpFlag = "none"
            self.vector.y_velocity = 0
        self.rect.x = self.x
        self.rect.y = self.y

    def update_x(self, background, floor_rects, brick_rects, block_rects, solid_rects, smallpipe_rects,
                 mediumpipe_rects, largepipe_rects, flag_rects, castle_rects, goomba_rects, koopa_rects):
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

            dx = background.x
            background.update(self.vector.x_velocity)
            dy = background.x

        else:
            self.x += self.vector.x_velocity
            self.rect.x = self.x
        return background

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

    def blit(self):
        self.screen.blit(self.image, self.rect)


class SmallMario(Mario):
    def __init__(self, image_lib, screen, settings, x, y,  sound_library):
        super().__init__(image_lib, screen, settings, x, y,  sound_library)


class BigMario(Mario):
    def __init__(self, image_lib, screen, settings, x, y,  sound_library):
        super().__init__(image_lib, screen, settings, x, y,  sound_library)


class FireMario(BigMario):
    def __init__(self, image_lib, screen, settings, x, y, sound_library):
        super().__init__(image_lib, screen, settings, x, y, sound_library)
