class Brick:
    def __init__(self, image_library, rect, screen, settings):
        self.screen = screen
        self.settings = settings
        self.img_lib = image_library

        self.img = self.img_lib[0]
        self.rect = rect

        self.incFlag = False
        self.incVar = -1
        self.counter = 0
        self.counter2 = 0

    def blit(self):
        if self.rect.right < 0 or self.rect.left > self.settings.screenWidth:
            return
        self.screen.blit(self.img, self.rect)

    def change_rect(self):
        if self.incFlag:
            self.rect.y += self.incVar
            self.counter += self.incVar
        if self.counter == -15:
            self.counter = 0
            self.incVar *= -1
        if self.counter == 15:
            self.incVar = -1
            self.counter = 0
            self.incFlag = False

    def update_x_coor(self, speed):
        self.rect.x += speed

    def create_powerup(self):
        self.incFlag = True


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
        self.power_up = None


class MysteryBrick(Brick):
    def __init__(self, image_library, rect, screen, settings):
        super().__init__(image_library, rect, screen, settings)
        self.power_up = None
        self.index = 0
        self.indexInc = 1

        self.consumed = False
        self.gen_coin = False

    def blit(self):
        if self.rect.right < 0 or self.rect.left > self.settings.screenWidth:
            return
        self.screen.blit(self.img_lib[self.index], self.rect)

    def change_index(self):
        if not self.consumed:
            self.index += self.indexInc
            if self.index == 0 or self.index == 2:
                self.indexInc *= -1
        else:
            self.index = 3

    def set_powerup(self, powerup):
        self.power_up = powerup

    def create_powerup(self):
        if self.power_up == "coin":
            self.gen_coin = True
