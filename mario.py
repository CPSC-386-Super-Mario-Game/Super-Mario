import vector


class Mario:
    def __init__(self, image_lib, screen, settings, x, y):
        self.screen = screen
        self.settings = settings
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

    def change_direction(self, direction):
        self.x_direction = direction
        self.vector.change_direction(direction)

    def jump(self):
        if self.jumpFlag == "jumping":
            return
        else:
            self.jumpFlag = "jumping"
            self.vector.jump()

    def blit(self):
        self.screen.blit(self.image, self.rect)


class SmallMario(Mario):
    def __init__(self, image_lib, screen, settings, x, y):
        super().__init__(image_lib, screen, settings, x, y)


class BigMario(Mario):
    def __init__(self, image_lib, screen, settings, x, y):
        super().__init__(image_lib, screen, settings, x, y)


class FireMario(BigMario):
    def __init__(self, image_lib, screen, settings, x, y):
        super().__init__(image_lib, screen, settings, x, y)
