import pygame
import sys
import brick
import pipe
import coin
import miscellaneous
from goomba import Goomba
from koopa import Koopa
import time


class GameFunctions:
    def __init__(self, finished):
        self.finished = finished
        self.timer = pygame.time.Clock()

        self.dt = 0
        self.block_timer = 1
        self.goomba_timer = 2
        self.koopa_timer = 2
        self.coin_timer = 1
        self.time_timer = 8
        self.mario_timer = 2

        self.death_flag = False
        self.game_over_flag = False
        self.overworld_flag = False
        self.on_warp_pipe = False
        self.warp_underworld = False

    def check_time(self, blocks, goombas, koopas, mario, coins, stats, sound_library):
        self.block_timer -= self.dt
        if self.block_timer < 0:
            self.block_timer = 1
            for block in blocks:
                block.change_index()

        self.mario_timer -= self.dt
        if self.mario_timer < 0:
            self.mario_timer = 2
            mario.change_index()

        self.goomba_timer -= self.dt
        if self.goomba_timer < 0:
            self.goomba_timer = 2
            for goomba in goombas:
                goomba.flip_img()

        self.koopa_timer -= self.dt
        if self.koopa_timer < 0:
            self.koopa_timer = 2
            for koopa in koopas:
                koopa.walk_flip()

        self.coin_timer -= self.dt
        if self.coin_timer < 0:
            self.coin_timer = 1
            for c in coins:
                c.change_index()

        self.time_timer -= self.dt
        if self.time_timer < 0:
            self.time_timer = 1
            stats.time -= 1
            if stats.time == 250:
                pygame.mixer.set_num_channels(0)
                pygame.mixer.set_num_channels(8)
                sound_library[0][1].play(-1)

        self.dt = self.timer.tick(144) / 144

    def check_bottom_collisions(self, begin, blocks, bricks, end, floor, goombas, koopas, mario, sound_library, stats, smallpipes, mediumpipes, largepipes):
        # BLOCKS
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
            stats.score_progression_index = 0
            return
        # FLOOR
        if mario.vector.y_velocity >= 0:
            index = mario.rect.collidelist(floor[begin:end])
            if index == -1:
                mario.jumpFlag = "falling"
            else:
                mario.rect.bottom = floor[index].top
                mario.vector.y_velocity = 0
                mario.jumpFlag = "None"
                stats.score_progression_index = 0
                return
        # BRICKS
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
            stats.score_progression_index = 0
            return
        # GOOMBAS
        index = mario.rect.collidelist(goombas)
        if index == -1:
            pass
        elif goombas[index].dead:
            pass
        elif mario.jumpFlag == "falling":
            stats.score += stats.score_progression[stats.score_progression_index]
            stats.rising_score_value_list.append(stats.score_progression[stats.score_progression_index])
            stats.rising_score_rect_list.append(pygame.Rect(goombas[index].rect.x, goombas[index].rect.y, 30, 30))
            stats.score_progression_index += 1
            stats.rising_score_index += 1
            stats.rising_score_frame_list.append(60)
            if stats.score_progression_index > 9:
                stats.lives += 1
                stats.score_progression_index = 0
            goombas[index].dead = True
            goombas[index].rect.y -= 28
            mario.vector.y_velocity = 0
            mario.jumpFlag = "None"
            mario.jump_small()
        # KOOPAS
        index = mario.rect.collidelist(koopas)
        if index == -1:
            pass
        elif koopas[index].dead:
            pass
        elif mario.jumpFlag == "falling":
            stats.score += stats.score_progression[stats.score_progression_index]
            stats.rising_score_value_list.append(stats.score_progression[stats.score_progression_index])
            stats.rising_score_rect_list.append(pygame.Rect(koopas[index].rect.x, koopas[index].rect.y, 30, 30))
            stats.score_progression_index += 1
            stats.rising_score_index += 1
            stats.rising_score_frame_list.append(60)
            if stats.score_progression_index > 9:
                stats.lives += 1
                stats.score_progression_index = 0
            koopas[index].dead = True
            sound_library[1][10].play()
            goombas[index].rect.y -= 28
            mario.vector.y_velocity = 0
            mario.jumpFlag = "None"
            mario.jump()
        # MARIO X SMALLPIPE
        index = mario.rect.collidelist(smallpipes)
        if index == -1:
            pass
        elif mario.vector.y_velocity < 0:
            mario.rect.top = smallpipes[index].rect.bottom + 7
            mario.vector.y_velocity = 1.5
            mario.jumpFlag = "falling"
            return
        else:
            mario.vector.y_velocity = 0
            mario.rect.bottom = smallpipes[index].rect.top - 1
            mario.jumpFlag = "None"
            stats.score_progression_index = 0
            return
        # MARIO X MEDIUMPIPE
        index = mario.rect.collidelist(mediumpipes)
        if index == -1:
            pass
        elif mario.vector.y_velocity < 0:
            mario.rect.top = mediumpipes[index].rect.bottom + 7
            mario.vector.y_velocity = 1.5
            mario.jumpFlag = "falling"
            return
        else:
            mario.vector.y_velocity = 0
            mario.rect.bottom = mediumpipes[index].rect.top - 1
            mario.jumpFlag = "None"
            stats.score_progression_index = 0
            return
        # MARIO X LARGEPIPE
        index = mario.rect.collidelist(largepipes)
        if index == -1:
            self.on_warp_pipe = False
            pass
        elif mario.vector.y_velocity < 0:
            mario.rect.top = largepipes[index].rect.bottom + 7
            mario.vector.y_velocity = 1.5
            mario.jumpFlag = "falling"
            self.on_warp_pipe = False
            return
        else:
            mario.vector.y_velocity = 0
            mario.rect.bottom = largepipes[index].rect.top - 1
            mario.jumpFlag = "None"
            if index == 1:
                self.on_warp_pipe = True
            stats.score_progression_index = 0
            return


    @staticmethod
    def check_left_collisions(blocks, bricks, smallpipes, mediumpipes, largepipes, mario, goombas, koopas):
        # mario x blocks
        index = mario.rect.collidelist(blocks)
        if index == -1:
            pass
        elif mario.rect.x - blocks[index].rect.x < 0:
            mario.rect.right = blocks[index].rect.left - 1
            mario.vector.x_velocity = 0
        else:
            mario.rect.left = blocks[index].rect.right + 1
            mario.vector.x_velocity = 0
        # mario x bricks
        index = mario.rect.collidelist(bricks)
        if index == -1:
            pass
        elif mario.rect.x - bricks[index].rect.x < 0:
            mario.rect.right = bricks[index].rect.left
            mario.vector.x_velocity = 0
        else:
            mario.rect.left = bricks[index].rect.right
            mario.vector.x_velocity = 0
        # mario x smallpipe
        index = mario.rect.collidelist(smallpipes)
        if index <= -1:
            pass
        elif mario.rect.x - smallpipes[index].rect.x == 0:
            pass
        elif mario.rect.x - smallpipes[index].rect.x < 0:
            mario.rect.right = smallpipes[index].rect.left
            mario.vector.x_velocity = 0
        else:
            mario.rect.left = smallpipes[index].rect.right
            mario.vector.x_velocity = 0
        # mario x mediumpipe
        index = mario.rect.collidelist(mediumpipes)
        if index <= -1:
            pass
        elif mario.rect.x - mediumpipes[index].rect.x == 0:
            pass
        elif mario.rect.x - mediumpipes[index].rect.x < 0:
            mario.rect.right = mediumpipes[index].rect.left
            mario.vector.x_velocity = 0
        else:
            mario.rect.left = mediumpipes[index].rect.right
            mario.vector.x_velocity = 0
        # mario x largepipes
        index = mario.rect.collidelist(largepipes)
        if index <= -1:
            pass
        elif mario.rect.x - largepipes[index].rect.x == 0:
            pass
        elif mario.rect.x - largepipes[index].rect.x < 0:
            mario.rect.right = largepipes[index].rect.left
            mario.vector.x_velocity = 0
        else:
            mario.rect.left = largepipes[index].rect.right
            mario.vector.x_velocity = 0
        # goomba x pipes
        for goomba in goombas:
            if goomba.rect.x > 0:
                #small
                index = goomba.rect.collidelist(smallpipes)
                if index <= -1:
                    pass
                else:
                    goomba.change_direction()
                # medium
                index = goomba.rect.collidelist(mediumpipes)
                if index <= -1:
                    pass
                else:
                    goomba.change_direction()
                # large
                index = goomba.rect.collidelist(largepipes)
                if index <= -1:
                    pass
                else:
                    goomba.change_direction()
        # koopa x pipes
        for koopa in koopas:
            if koopa.rect.x > 0:
                # small
                index = koopa.rect.collidelist(smallpipes)
                if index == -1:
                    pass
                else:
                    koopa.change_direction()
                # medium
                index = koopa.rect.collidelist(mediumpipes)
                if index == -1:
                    pass
                else:
                    koopa.change_direction()
                # large
                index = koopa.rect.collidelist(largepipes)
                if index == -1:
                    pass
                else:
                    koopa.change_direction()


    @staticmethod
    def blit_objects(mario, bricks, blocks, goombas, koopas, solids, smallpipes, mediumpipes, largepipes, flags,
                     castles):
        for obj in bricks:
            obj.blit()
        for obj in blocks:
            obj.blit()
        for obj in goombas:
            if obj.rect.x < -100 or obj.dead_counter > 59:
                goombas.remove(obj)
                print("dead goomba")
            obj.blitme()
        for obj in koopas:
            if obj.rect.x < -100:
                koopas.remove(obj)
                print("dead koopa")
            obj.blitme()
        for obj in solids:
            obj.blit()
        for obj in smallpipes:
            obj.blit()
        for obj in mediumpipes:
            obj.blit()
        for obj in largepipes:
            obj.blit()
        for obj in flags:
            obj.blit()
        for obj in castles:
            obj.blit()

    def update_mario(self, background, blocks, bricks, floor, mario, solids, smallpipes, mediumpipes, largepipes, flags,
                     castles, goombas, koopas, sound_library, stats):
        background = mario.update_x(background, floor, bricks, blocks, solids, smallpipes, mediumpipes, largepipes,
                                    flags, castles)
        self.check_left_collisions(blocks, bricks, smallpipes, mediumpipes, largepipes, mario, goombas, koopas)
        mario.update_y()
        if mario.rect.y > 896:
            self.mario_death(stats, sound_library, mario)
        self.check_bottom_collisions(background.floor_begin, blocks, bricks, background.floor_end, floor,
                                              goombas, koopas, mario, sound_library, stats, smallpipes, mediumpipes,
                                              largepipes)
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

    def check_events(self, mario, sound_lib, stats, overworld_flag):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                stats = stats
                self.check_keydown_events(event, mario, sound_lib, stats, overworld_flag)
            elif event.type == pygame.KEYUP:
                GameFunctions.check_keyup_events(event, mario)

    def check_keydown_events(self, event2, mario, sound_lib, stats, overworld_flag):
        if event2.key == pygame.K_RIGHT and mario.vector.x_velocity < 1:
            mario.change_direction("right")
            mario.flip_back()
        elif event2.key == pygame.K_LEFT and mario.vector.x_velocity > -1:
            mario.change_direction("left")
            mario.flip_direction()
        elif event2.key == pygame.K_DOWN and self.on_warp_pipe:
            self.overworld_flag = True
        elif event2.key == pygame.K_UP or event2.key == pygame.K_SPACE:
            mario.jump()
        elif event2.key == pygame.K_q:
            sys.exit()
        elif event2.key == pygame.K_p:
            pygame.mixer.set_num_channels(0)
            pygame.mixer.set_num_channels(8)
            sound_lib[1][12].play()
            pause_flag = True
            while pause_flag:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            sys.exit()
                        elif event.key == pygame.K_p:
                            pause_flag = False
                            if stats.time > 250 and not overworld_flag:
                                sound_lib[0][0].play(-1)
                            if stats.time <= 250 and not overworld_flag:
                                sound_lib[0][1].play(-1)
                            if stats.time > 250 and overworld_flag:
                                sound_lib[0][2].play(-1)
                            if stats.time <= 250 and overworld_flag:
                                sound_lib[0][3].play(-1)

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
    def load_flag_obj(image_library, rect_list, screen, settings):
        flag_list = []
        for rect in rect_list:
            new_flag = miscellaneous.Flag(image_library, rect, screen, settings)
            flag_list.append(new_flag)
        return flag_list

    @staticmethod
    def load_castle_obj(image_library, rect_list, screen, settings):
        castle_list = []
        for rect in rect_list:
            new_castle = miscellaneous.Castle(image_library, rect, screen, settings)
            castle_list.append(new_castle)
        return castle_list

    @staticmethod
    def load_goomba_objects(image_library, rect_list, screen, settings, sound_lib):
        goomba_list = []
        for rect in rect_list:
            new_goomba = Goomba(screen, settings, rect, image_library, sound_lib)
            goomba_list.append(new_goomba)
        return goomba_list

    @staticmethod
    def load_koopa_objects(image_library, rect_list, screen, settings, sound_lib):
        koopa_list = []
        for rect in rect_list:
            new_koopa = Koopa(screen, settings, rect, image_library, sound_lib)
            koopa_list.append(new_koopa)
        return koopa_list

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

    def game_over(self, stats, sound_library):
        self.finished = True
        self.game_over_flag = True
        sound_library[1][7].play()
        stats.lives = 3
        if stats.score > stats.high_score:
            stats.high_score = stats.score
            file = open('highscore.txt', 'w')
            file.write(str(stats.high_score))
            file.close()

        stats.score = 0
        stats.time = 1000
        stats.coins = 0

    def mario_death(self, stats, sound_library, mario):
        stats.lives -= 1
        stats.time = 1000
        pygame.mixer.set_num_channels(0)
        pygame.mixer.set_num_channels(8)
        sound_library[1][11].play()
        time.sleep(3)

        self.death_flag = True
        if stats.lives == 0:
            self.game_over(stats, sound_library)


    @staticmethod
    def load_sound_library():
        track_lib = [pygame.mixer.Sound('sounds/smb_overworld.wav'),
                     pygame.mixer.Sound('sounds/smb_hurry_overworld.wav'),
                     pygame.mixer.Sound('sounds/smb_underworld.wav'),
                     pygame.mixer.Sound('sounds/smb_hurry_underworld.wav'),
                     pygame.mixer.Sound('sounds/smb_starman.wav')]
        effects_lib = [pygame.mixer.Sound('sounds/smb_1-up.wav'),
                       pygame.mixer.Sound('sounds/smb_breakblock.wav'),
                       pygame.mixer.Sound('sounds/smb_bump.wav'),
                       pygame.mixer.Sound('sounds/smb_coin.wav'),
                       pygame.mixer.Sound('sounds/smb_fireball.wav'), pygame.mixer.Sound('sounds/smb_fireworks.wav'),
                       pygame.mixer.Sound('sounds/smb_flagpole.wav'), pygame.mixer.Sound('sounds/smb_gameover.wav'),
                       pygame.mixer.Sound('sounds/smb_jump-small.wav'),
                       pygame.mixer.Sound('sounds/smb_jump-super.wav'), pygame.mixer.Sound('sounds/smb_kick.wav'),
                       pygame.mixer.Sound('sounds/smb_mariodie.wav'),
                       pygame.mixer.Sound('sounds/smb_pause.wav'), pygame.mixer.Sound('sounds/smb_pipe.wav'),
                       pygame.mixer.Sound('sounds/smb_powerup.wav'),
                       pygame.mixer.Sound('sounds/smb_powerup_appears.wav'),
                       pygame.mixer.Sound('sounds/smb_stage_clear.wav'), pygame.mixer.Sound('sounds/smb_stomp.wav'),
                       pygame.mixer.Sound('sounds/smb_warning.wav')]
        sound_lib = [track_lib, effects_lib]

        return sound_lib

    @staticmethod
    def load_image_library():
        bg_lib = [pygame.image.load('images/bg.png')]

        brick_lib = [pygame.image.load('images/fg/brick.png'), pygame.image.load('images/fg/break.png')]
        brick_lib[0] = pygame.transform.scale(brick_lib[0], (56, 56))

        mystery_lib = [pygame.image.load('images/fg/mystery0.png'), pygame.image.load('images/fg/mystery1.png'),
                       pygame.image.load('images/fg/mystery2.png'), pygame.image.load('images/fg/mystery_hit.png')]
        for index, img in enumerate(mystery_lib):
            mystery_lib[index] = pygame.transform.scale(img, (56, 56))

        flag_lib = [pygame.image.load('images/fg/flag.png'), pygame.image.load('images/bg/pole.png'),
                    pygame.image.load('images/bg/castle.png')]
        flag_lib[1] = pygame.transform.scale(flag_lib[1], (56, 560))
        flag_lib[2] = pygame.transform.scale(flag_lib[2], (280, 280))

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
        for index, img in enumerate(koopa_lib):
            if index == 0 or index == 1:
                koopa_lib[index] = pygame.transform.scale(img, (56, 84))
            else:
                koopa_lib[index] = pygame.transform.scale(img, (56, 56))

        img_lib = [bg_lib, brick_lib, mystery_lib, flag_lib, mushroom_lib, one_up_lib, brick_coin_lib, coin_lib,
                   floor_lib, star_lib, flower_lib, pipes_lib, big_lib, big_invinc_lib, fire_lib, small_lib,
                   small_invinc_lib, goomba_lib, koopa_lib]

        for library in img_lib:
            for index, img in enumerate(library):
                library[index] = img.convert_alpha()

        return img_lib
