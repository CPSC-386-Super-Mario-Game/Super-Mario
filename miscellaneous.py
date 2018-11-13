class Flag:
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

class Castle:
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