class Vector:
    def __init__(self, settings):
        self.settings = settings

        self.gravAcc = 0.14066
        self.jumpAcc = -0.09066
        self.jumpIV = -5

        self.rightAcc = 0.07
        self.leftAcc = -0.07
        self.upAcc = 1

        self.x_velocity = 0
        self.y_velocity = 0

        self.min_dx = -3
        self.max_dx = 3
        self.max_dy = 3
        self.min_dy = -3
        self.friction = 0.05

    def update_x_velocity(self, direction):
        if direction == "right":
            if self.x_velocity < self.max_dx:
                self.x_velocity += (self.rightAcc - self.friction)
            return
        if direction == "none":
            if self.x_velocity > 0:
                self.x_velocity -= self.friction
            elif self.x_velocity < 0:
                self.x_velocity += self.friction
            if abs(self.x_velocity) < 0.1:
                self.x_velocity = 0
            return
        if direction == "left":
            if self.x_velocity > self.min_dx:
                self.x_velocity += (self.leftAcc + self.friction)
            return

    def update_y_velocity(self, flag):
        if flag is "jumping":
            self.y_velocity = self.y_velocity + self.gravAcc + self.jumpAcc
        elif flag is "falling":
            self.y_velocity += self.gravAcc
        else:
            return

    def jump(self):
        self.y_velocity = self.jumpIV

    def jump_small(self):
        self.y_velocity = -2

    def change_direction(self, direction):
        if direction == "left":
            self.x_velocity -= 1
        if direction == "right":
            self.x_velocity += 1
