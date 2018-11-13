import pygame
import sys
import brick
import pipe
import coin
from goomba import Goomba


class GameFunctions:
    def __init__(self, finished):
        self.finished = finished
        self.timer = pygame.time.Clock()

        self.dt = 0
        self.block_timer = 1
        self.goomba_timer = 2
        self.coin_timer = 1

        self.overworld_flag = False

    def check_time(self, blocks, goombas, coins):
        self.block_timer -= self.dt
        if self.block_timer < 0:
            self.block_timer = 1
            for block in blocks:
                block.change_index()

        self.goomba_timer -= self.dt
        if self.goomba_timer < 0:
            self.goomba_timer = 2
            for goomba in goombas:
                goomba.flip_img()

        self.coin_timer -= self.dt
        if self.coin_timer < 0:
            self.coin_timer = 1
            for coin in coins:
                coin.change_index()

        self.dt = self.timer.tick(144) / 144

    @staticmethod
    def check_bottom_collisions(begin, blocks, bricks, end, floor, mario):
        index = mario.rect.collidelist(blocks)
        if index == -1:
            pass
        elif mario.rect.y - blocks[index].rect.y > 0:
            if mario.rect.right - blocks[index].rect.left < 20:
                mario.rect.right = blocks[index].rect.left
                mario.rect.top = blocks[index].rect.bottom
                return
            elif mario.rect.left - blocks[index].rect.right > -20:
                mario.rect.left = blocks[index].rect.right
                return
            mario.rect.top = blocks[index].rect.bottom
            mario.vector.y_velocity = 1.5
            mario.jumpFlag = "falling"
            return
        elif mario.vector.y_velocity >= 0:
            mario.vector.y_velocity = 0
            mario.rect.bottom = blocks[index].rect.top
            mario.jumpFlag = "None"
            return

        if mario.vector.y_velocity >= 0:
            index = mario.rect.collidelist(floor[begin:end])
            if index == -1:
                mario.jumpFlag = "falling"
            else:
                mario.rect.bottom = floor[index].top
                mario.vector.y_velocity = 0
                mario.jumpFlag = "None"
                return

        index = mario.rect.collidelist(bricks)
        if index == -1:
            pass
        elif mario.vector.y_velocity < 0:
            mario.rect.top = bricks[index].rect.bottom + 7
            mario.vector.y_velocity = 1.5
            mario.jumpFlag = "falling"
            return
        else:
            mario.vector.y_velocity = 0
            mario.rect.bottom = bricks[index].rect.top - 1
            mario.jumpFlag = "None"
            return

    @staticmethod
    def check_left_collisions(blocks, bricks, mario):
        index = mario.rect.collidelist(blocks)
        if index == -1:
            pass
        elif mario.rect.x - blocks[index].rect.x < 0:
            mario.rect.right = blocks[index].rect.left - 1
            mario.vector.x_velocity = 0
        else:
            mario.rect.left = blocks[index].rect.right + 1
            mario.vector.x_velocity = 0

        index = mario.rect.collidelist(bricks)
        if index == -1:
            pass
        elif mario.rect.x - bricks[index].rect.x < 0:
            mario.rect.right = bricks[index].rect.left
            mario.vector.x_velocity = 0
        else:
            mario.rect.left = bricks[index].rect.right
            mario.vector.x_velocity = 0

    @staticmethod
    def blit_objects(bricks, blocks, goombas, solids, smallpipes, mediumpipes, largepipes):
        for obj in bricks:
            obj.blit()
        for obj in blocks:
            obj.blit()
        for obj in goombas:
            if obj.update():
                goombas.remove(obj)
                print("dead goomba")
        for obj in solids:
            obj.blit()
        for obj in smallpipes:
            obj.blit()
        for obj in mediumpipes:
            obj.blit()
        for obj in largepipes:
            obj.blit()
    @staticmethod
    def update_mario(background, blocks, bricks, floor, mario, solids, smallpipes, mediumpipes, largepipes):
        background = mario.update_x(background, floor, bricks, blocks, solids, smallpipes, mediumpipes, largepipes)
        GameFunctions.check_left_collisions(blocks, bricks, mario)
        mario.update_y()
        GameFunctions.check_bottom_collisions(background.floor_begin, blocks, bricks, background.floor_end, floor, mario)
        return background

    @staticmethod
    def blit_ugobjects(bricks, blocks, leftpipes, hugepipes, coins):
        for obj in bricks:
            obj.blit()
        for obj in blocks:
            obj.blit()
        for obj in hugepipes:
            obj.blit()
        for obj in leftpipes:
            obj.blit()
        for obj in coins:
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
    def load_solid_objects(image_library, rect_list, screen, settings):
        solid_list = []
        for rect in rect_list:
            new_solid = brick.Solid(image_library, rect, screen, settings)
            solid_list.append(new_solid)
        return solid_list

    @staticmethod
    def load_ugfloor_objects(image_library, rect_list, screen, settings):
        floor_list = []
        for rect in rect_list:
            new_floor = brick.Floor(image_library, rect, screen, settings)
            floor_list.append(new_floor)
        return floor_list

    @staticmethod
    def load_block_objects(image_library, rect_list, screen, settings):
        block_list = []
        for rect in rect_list:
            new_block = brick.MysteryBrick(image_library, rect, screen, settings)
            block_list.append(new_block)
        return block_list

    @staticmethod
    def load_smallpipe_obj(image_library, rect_list, screen, settings):
        smallpipe_list = []
        for rect in rect_list:
            new_smallpipe = pipe.SmallPipe(image_library, rect, screen, settings)
            smallpipe_list.append(new_smallpipe)
        return smallpipe_list

    @staticmethod
    def load_mediumpipe_obj(image_library, rect_list, screen, settings):
        mediumpipe_list = []
        for rect in rect_list:
            new_mediumpipe = pipe.MediumPipe(image_library, rect, screen, settings)
            mediumpipe_list.append(new_mediumpipe)
        return mediumpipe_list

    @staticmethod
    def load_largepipe_obj(image_library, rect_list, screen, settings):
        largepipe_list = []
        for rect in rect_list:
            new_largepipe = pipe.LargePipe(image_library, rect, screen, settings)
            largepipe_list.append(new_largepipe)
        return largepipe_list

    @staticmethod
    def load_goomba_objects(image_library, rect_list, screen, settings):
        goomba_list = []
        for rect in rect_list:
            new_goomba = Goomba(screen, settings, rect, image_library)
            goomba_list.append(new_goomba)
        return goomba_list

    @staticmethod
    def load_leftpipe_obj(image_library, rect_list, screen, settings):
        leftpipe_list = []
        for rect in rect_list:
            new_leftpipe = pipe.LeftPipe(image_library, rect, screen, settings)
            leftpipe_list.append(new_leftpipe)
        return leftpipe_list

    @staticmethod
    def load_hugepipe_obj(image_library, rect_list, screen, settings):
        hugepipe_list = []
        for rect in rect_list:
            new_hugepipe = pipe.HugePipe(image_library, rect, screen, settings)
            hugepipe_list.append(new_hugepipe)
        return hugepipe_list

    @staticmethod
    def load_coin_objs(image_library, rect_list, screen, settings):
        coin_list = []
        for rect in rect_list:
            new_coin = coin.Coin(image_library, rect, screen, settings)
            coin_list.append(new_coin)
        return coin_list

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
        for index, img in enumerate(coin_lib):
            coin_lib[index] = pygame.transform.scale(img, (28, 56))

        floor_lib = [pygame.image.load('images/fg/ug_brick.png'), pygame.image.load('images/fg/ug_floor.png'),
                     pygame.image.load('images/fg/tile.png'), pygame.image.load('images/fg/floor.png')]
        for index, img in enumerate(floor_lib):
            floor_lib[index] = pygame.transform.scale(img, (56, 56))

        star_lib = [pygame.image.load('images/fg/star0.png'), pygame.image.load('images/fg/star1.png'),
                    pygame.image.load('images/fg/star2.png'), pygame.image.load('images/fg/star3.png')]

        flower_lib = [pygame.image.load('images/fg/flower0.png'), pygame.image.load('images/fg/flower1.png'),
                      pygame.image.load('images/fg/flower2.png'), pygame.image.load('images/fg/flower3.png')]

        pipes_lib = [pygame.image.load('images/fg/small_pipe_up.png'),
                     pygame.image.load('images/fg/medium_pipe_up.png'),
                     pygame.image.load('images/fg/large_pipe_up.png'),
                     pygame.image.load('images/fg/largest_pipe_up.png'),
                     pygame.image.load('images/fg/pipe_left.png')]
        pipes_lib[4] = pygame.transform.scale(pipes_lib[4], (162, 112))
        pipes_lib[3] = pygame.transform.scale(pipes_lib[3], (112, 616))
        pipes_lib[0] = pygame.transform.scale(pipes_lib[0], (112, 112))
        pipes_lib[1] = pygame.transform.scale(pipes_lib[1], (112, 168))
        pipes_lib[2] = pygame.transform.scale(pipes_lib[2], (112, 224))

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
