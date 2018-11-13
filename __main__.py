import background as b
from gameFunctions import GameFunctions
import os
import pygame
import settings as s
import map as m
import mario as mario


class Main:
    def __init__(self):
        #   Provides consistent window positioning.
        os.environ['SDL_VIDEO_WINDOW_POS'] = '60, 35'
        pygame.init()
        pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()                                         # Used for FPS + time-tracking

        #   Initial set-up
        self.settings = s.Settings()
        pygame.display.set_caption(self.settings.gameTitle)
        self.screen = pygame.display.set_mode((self.settings.screenWidth, self.settings.screenHeight))
        self.screen.fill(self.settings.bgColor)
        self.gF = GameFunctions(finished=False)

        #   Generate game objects
        self.image_library = self.gF.load_image_library()
        self.sound_library = self.gF.load_sound_library()
        self.background = b.Background(self.image_library, self.screen, self.settings)
        self.map = m.Map(self.image_library, self.screen, self.settings)

        self.mario = mario.SmallMario([self.image_library[15], self.image_library[16]], self.screen, self.settings,
                                      self.map.mario_coor[0][0], self.map.mario_coor[0][1], self.sound_library)
        self.bricks = self.gF.load_brick_objects(self.image_library[1], self.map.brick_rect, self.screen, self.settings)
        self.blocks = self.gF.load_block_objects(self.image_library[2], self.map.mystery_rect, self.screen,
                                                 self.settings)
        self.goombas = self.gF.load_goomba_objects(self.image_library[17], self.map.goomba_rect, self.screen,
                                                   self.settings, self.sound_library)
        self.koopas = self.gF.load_koopa_objects(self.image_library[18], self.map.koopa_coor, self.screen,
                                                 self.settings, self.sound_library)
        self.floor_rects = self.map.floor_rects
        self.solid_rects = self.gF.load_solid_objects(self.image_library[8], self.map.solid_rect, self.screen, self.settings)
        self.smallpipe_rects = self.gF.load_smallpipe_obj(self.image_library[11], self.map.smallpipe_rect, self.screen, self.settings)
        self.mediumpipe_rects = self.gF.load_mediumpipe_obj(self.image_library[11], self.map.mediumpipe_rect, self.screen, self.settings)
        self.largepipe_rects = self.gF.load_largepipe_obj(self.image_library[11], self.map.largepipe_rect, self.screen, self.settings)
        self.flag_rects = self.gF.load_flag_obj(self.image_library[3], self.map.flag_rect, self.screen, self.settings)
        self.castle_rects = self.gF.load_castle_obj(self.image_library[3], self.map.castle_rect, self.screen, self.settings)

        # Underworld
        self.ugmap = m.UnderworldMap(self.image_library, self.screen, self.settings)
        self.ug_bricks = self.gF.load_brick_objects(self.image_library[8], self.ugmap.brick_rect, self.screen,
                                                    self.settings)
        self.ug_blocks = self.gF.load_ugfloor_objects(self.image_library[8], self.ugmap.floor_rect, self.screen,
                                                      self.settings)
        self.ug_leftpipes = self.gF.load_leftpipe_obj(self.image_library[11], self.ugmap.leftpipe_rect, self.screen,
                                                      self.settings)
        self.ug_hugepipes = self.gF.load_hugepipe_obj(self.image_library[11], self.ugmap.hugepipe_rect, self.screen,
                                                      self.settings)
        self.ug_coins = self.gF.load_coin_objs(self.image_library[7], self.ugmap.coin_rect, self.screen, self.settings)

        self.i = 0

        self.sound_library[0][0].play(-1)

    #   Game loop
    def play(self):
        while True:
            # if self.gF.overworld_flag:  # testing purposes, will set mario position differently later
            #     self.mario = mario.SmallMario([self.image_library[15], self.image_library[16]], self.screen,
            #                                   self.settings,
            #                                   self.map.mario_coor[0][0], self.map.mario_coor[0][1])
            # else:
            #     self.mario = mario.SmallMario([self.image_library[15], self.image_library[16]], self.screen,
            #                                   self.settings,
            #                                   self.ugmap.mario_coor[0][0], self.ugmap.mario_coor[0][1])
            while not self.gF.finished:
                self.gF.check_events(self.mario)
                self.background = self.gF.update_mario(self.background, self.blocks, self.bricks, self.floor_rects,
                                                       self.mario, self.solid_rects, self.smallpipe_rects,
                                                       self.mediumpipe_rects, self.largepipe_rects, self.flag_rects,
                                                       self.castle_rects, self.goombas, self.koopas, self.sound_library)
                if not self.gF.overworld_flag:
                    self.background.blit()
                    self.gF.blit_objects(self.mario, self.bricks, self.blocks, self.goombas, self.koopas, self.solid_rects, self.smallpipe_rects,
                                         self.mediumpipe_rects, self.largepipe_rects, self.flag_rects,
                                         self.castle_rects)

                else:
                    self.background.ugblit()
                    self.gF.blit_ugobjects(self.ug_bricks, self.ug_blocks, self.ug_leftpipes, self.ug_hugepipes,
                                           self.ug_coins)

                for floor in self.floor_rects:
                    # if floor.right < 0:
                    #     continue
                    # if floor.left > self.settings.screenWidth:
                    #     break
                    self.screen.blit(self.image_library[8][3], floor)

                self.mario.blit()
                pygame.display.flip()

                self.gF.check_time(self.blocks, self.goombas, self.koopas, self.ug_coins)
                self.clock.tick(self.settings.FPS)                                     # Locks game at designated FPS


if __name__ == '__main__':
    game = Main()
    game.play()
