import pygame
import sys
import brick


class GameFunctions:
    def __init__(self, finished):
        self.finished = finished
        self.timer = pygame.time.Clock()

        self.dt = 0
        self.block_timer = 1

    def check_time(self, blocks):
        self.block_timer -= self.dt
        if self.block_timer < 0:
            self.block_timer = 1
            for block in blocks:
                block.change_index()
        self.dt = self.timer.tick(144) / 144

    @staticmethod
    def blit_objects(bricks, blocks):
        for obj in bricks:
            obj.blit()
        for obj in blocks:
            obj.blit()

    @staticmethod
    def check_events(mario):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                GameFunctions.check_keydown_events(event, mario)
            elif event.type == pygame.KEYUP:
                GameFunctions.check_keyup_events(event, mario)

    @staticmethod
    def check_keydown_events(event, mario):
        if event.key == pygame.K_RIGHT and mario.vector.x_velocity < 1:
            mario.change_direction("right")
        elif event.key == pygame.K_LEFT and mario.vector.x_velocity > -1:
            mario.change_direction("left")
        elif event.key == pygame.K_UP or event.key == pygame.K_SPACE:
            mario.jump()
        elif event.key == pygame.K_q:
            sys.exit()

    @staticmethod
    def check_keyup_events(event, mario):
        if event.key == pygame.K_LEFT and mario.x_direction is "left":
            mario.x_direction = "none"
        if event.key == pygame.K_RIGHT and mario.x_direction is "right":
            mario.x_direction = "none"
        elif event.key == pygame.K_UP and mario.jumpFlag is "jumping":
            mario.jumpFlag = "falling"
        elif event.key == pygame.K_SPACE and mario.jumpFlag is "jumping":
            mario.jumpFlag = "falling"

    @staticmethod
    def load_brick_objects(image_library, rect_list, screen, settings):
        brick_list = []
        for rect in rect_list:
            new_brick = brick.Brick(image_library, rect, screen, settings)
            brick_list.append(new_brick)
        return brick_list

    @staticmethod
    def load_block_objects(image_library, rect_list, screen, settings):
        block_list = []
        for rect in rect_list:
            new_block = brick.MysteryBrick(image_library, rect, screen, settings)
            block_list.append(new_block)
        return block_list

    @staticmethod
    def load_image_library():
        bg_lib = [pygame.image.load('images/bg.png')]

        brick_lib = [pygame.image.load('images/fg/brick.png'), pygame.image.load('images/fg/break.png')]
        brick_lib[0] = pygame.transform.scale(brick_lib[0], (56, 56))

        mystery_lib = [pygame.image.load('images/fg/mystery0.png'), pygame.image.load('images/fg/mystery1.png'),
                       pygame.image.load('images/fg/mystery2.png'), pygame.image.load('images/fg/mystery_hit.png')]
        for index, img in enumerate(mystery_lib):
            mystery_lib[index] = pygame.transform.scale(img, (56, 56))

        flag_lib = [pygame.image.load('images/fg/flag.png')]

        mushroom_lib = [pygame.image.load('images/fg/mushroom.png')]

        one_up_lib = [pygame.image.load('images/fg/oneup.png')]

        brick_coin_lib = [pygame.image.load('images/fg/brick_coin0.png'),
                          pygame.image.load('images/fg/brick_coin1.png'),
                          pygame.image.load('images/fg/brick_coin2.png')]

        coin_lib = [pygame.image.load('images/fg/coin0.png'), pygame.image.load('images/fg/coin1.png'),
                    pygame.image.load('images/fg/coin2.png'), pygame.image.load('images/fg/coin3.png')]

        floor_lib = [pygame.image.load('images/fg/ug_brick.png'), pygame.image.load('images/fg/ug_floor.png'),
                     pygame.image.load('images/fg/tile.png'), pygame.image.load('images/fg/floor.png')]

        star_lib = [pygame.image.load('images/fg/star0.png'), pygame.image.load('images/fg/star1.png'),
                    pygame.image.load('images/fg/star2.png'), pygame.image.load('images/fg/star3.png')]

        flower_lib = [pygame.image.load('images/fg/flower0.png'), pygame.image.load('images/fg/flower1.png'),
                      pygame.image.load('images/fg/flower2.png'), pygame.image.load('images/fg/flower3.png')]

        pipes_lib = [pygame.image.load('images/fg/small_pipe_up.png'),
                     pygame.image.load('images/fg/medium_pipe_up.png'),
                     pygame.image.load('images/fg/large_pipe_up.png'),
                     pygame.image.load('images/fg/largest_pipe_up.png')]

        big_lib = [pygame.image.load('images/mario/big_idle.png'), pygame.image.load('images/mario/big_turn.png'),
                   pygame.image.load('images/mario/big_jump.png'), pygame.image.load('images/mario/big_walk0.png'),
                   pygame.image.load('images/mario/big_walk1.png'), pygame.image.load('images/mario/big_walk2.png'),
                   pygame.image.load('images/mario/big_crouch.png')]

        big_invinc_lib = [pygame.image.load('images/mario/invinc0_big_idle.png'),
                          pygame.image.load('images/mario/invinc1_big_idle.png'),
                          pygame.image.load('images/mario/invinc2_big_idle.png'),
                          pygame.image.load('images/mario/invinc0_big_turn.png'),
                          pygame.image.load('images/mario/invinc1_big_turn.png'),
                          pygame.image.load('images/mario/invinc2_big_turn.png'),
                          pygame.image.load('images/mario/invinc0_big_jump.png'),
                          pygame.image.load('images/mario/invinc1_big_jump.png'),
                          pygame.image.load('images/mario/invinc2_big_jump.png'),
                          pygame.image.load('images/mario/invinc0_big_walk0.png'),
                          pygame.image.load('images/mario/invinc1_big_walk0.png'),
                          pygame.image.load('images/mario/invinc2_big_walk0.png'),
                          pygame.image.load('images/mario/invinc0_big_walk1.png'),
                          pygame.image.load('images/mario/invinc1_big_walk1.png'),
                          pygame.image.load('images/mario/invinc2_big_walk1.png'),
                          pygame.image.load('images/mario/invinc0_big_walk2.png'),
                          pygame.image.load('images/mario/invinc1_big_walk2.png'),
                          pygame.image.load('images/mario/invinc2_big_walk2.png'),
                          pygame.image.load('images/mario/invinc0_big_crouch.png'),
                          pygame.image.load('images/mario/invinc1_big_crouch.png'),
                          pygame.image.load('images/mario/invinc2_big_crouch.png')]

        fire_lib = [pygame.image.load('images/mario/fire_idle.png'), pygame.image.load('images/mario/fire_turn.png'),
                    pygame.image.load('images/mario/fire_jump.png'), pygame.image.load('images/mario/fire_walk0.png'),
                    pygame.image.load('images/mario/fire_walk1.png'), pygame.image.load('images/mario/fire_walk2.png'),
                    pygame.image.load('images/mario/fire_crouch.png')]

        small_lib = [pygame.image.load('images/mario/small_idle.png'),
                     pygame.image.load('images/mario/small_turn.png'),
                     pygame.image.load('images/mario/small_jump.png'),
                     pygame.image.load('images/mario/small_walk0.png'),
                     pygame.image.load('images/mario/small_walk1.png'),
                     pygame.image.load('images/mario/small_walk2.png'),
                     pygame.image.load('images/mario/small_die.png'),
                     pygame.image.load('images/mario/small_grow.png')]
        for index, img in enumerate(small_lib):
            small_lib[index] = pygame.transform.scale(img, (56, 56))

        small_invinc_lib = [pygame.image.load('images/mario/invinc0_small_idle.png'),
                            pygame.image.load('images/mario/invinc1_small_idle.png'),
                            pygame.image.load('images/mario/invinc2_small_idle.png'),
                            pygame.image.load('images/mario/invinc0_small_turn.png'),
                            pygame.image.load('images/mario/invinc1_small_turn.png'),
                            pygame.image.load('images/mario/invinc2_small_turn.png'),
                            pygame.image.load('images/mario/invinc0_small_jump.png'),
                            pygame.image.load('images/mario/invinc1_small_jump.png'),
                            pygame.image.load('images/mario/invinc2_small_jump.png'),
                            pygame.image.load('images/mario/invinc0_small_walk0.png'),
                            pygame.image.load('images/mario/invinc1_small_walk0.png'),
                            pygame.image.load('images/mario/invinc2_small_walk0.png'),
                            pygame.image.load('images/mario/invinc0_small_walk1.png'),
                            pygame.image.load('images/mario/invinc1_small_walk1.png'),
                            pygame.image.load('images/mario/invinc2_small_walk1.png'),
                            pygame.image.load('images/mario/invinc0_small_walk2.png'),
                            pygame.image.load('images/mario/invinc1_small_walk2.png'),
                            pygame.image.load('images/mario/invinc2_small_walk2.png')]
        for index, img in enumerate(small_invinc_lib):
            small_invinc_lib[index] = pygame.transform.scale(img, (56, 56))

        goomba_lib = [pygame.image.load('images/enemies/goomba.png'),
                      pygame.image.load('images/enemies/goomba_dead.png')]
        for index, img in enumerate(goomba_lib):
            goomba_lib[index] = pygame.transform.scale(img, (56, 56))

        koopa_lib = [pygame.image.load('images/enemies/koopa0.png'), pygame.image.load('images/enemies/koopa1.png'),
                     pygame.image.load('images/enemies/koopa_stand.png'), pygame.image.load('images/enemies/shell.png')]

        img_lib = [bg_lib, brick_lib, mystery_lib, flag_lib, mushroom_lib, one_up_lib, brick_coin_lib, coin_lib,
                   floor_lib, star_lib, flower_lib, pipes_lib, big_lib, big_invinc_lib, fire_lib, small_lib,
                   small_invinc_lib, goomba_lib, koopa_lib]

        for library in img_lib:
            for index, img in enumerate(library):
                library[index] = img.convert_alpha()

        return img_lib
