class Brick:
    def __init__(self, image_library, rect, screen, settings):
        self.screen = screen
        self.settings = settings
        self.img_lib = image_library

        self.img = self.img_lib[0]
        self.rect = rect

    def blit(self):
        if self.rect.right < 0 or self.rect.left > self.settings.screenWidth:
            return
        self.screen.blit(self.img, self.rect)

    def update_x_coor(self, speed):
        self.rect.x += speed


class Floor:
    def __init__(self, image_library, rect, screen, settings):
        self.screen = screen
        self.settings = settings
        self.img_lib = image_library

        self.img = self.img_lib[1]
        self.rect = rect

    def blit(self):
        if self.rect.right < 0 or self.rect.left > self.settings.screenWidth:
            return
        self.screen.blit(self.img, self.rect)

    def update_x_coor(self, speed):
        self.rect.x += speed

class Solid:
    def __init__(self, image_library, rect, screen, settings):
        self.screen = screen
        self.settings = settings
        self.img_lib = image_library

        self.img = self.img_lib[2]
        self.rect = rect

    def blit(self):
        if self.rect.right < 0 or self.rect.left > self.settings.screenWidth:
            return
        self.screen.blit(self.img, self.rect)

    def update_x_coor(self, speed):
        self.rect.x += speed


class CoinBrick(Brick):
    def __init__(self, image_library, rect, screen, settings):
        super().__init__(image_library, rect, screen, settings)


class MysteryBrick(Brick):
    def __init__(self, image_library, rect, screen, settings):
        super().__init__(image_library, rect, screen, settings)
        self.index = 0
        self.indexInc = 1

    def blit(self):
        if self.rect.right < 0 or self.rect.left > self.settings.screenWidth:
            return
        self.screen.blit(self.img_lib[self.index], self.rect)

    def change_index(self):
        self.index += self.indexInc
        if self.index == 0 or self.index == 2:
            self.indexInc *= -1
