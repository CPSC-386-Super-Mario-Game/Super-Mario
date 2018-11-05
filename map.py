import pygame
import traceback
import sys
import time


class Map:
    def __init__(self, image_library, screen, settings):
        self.filename = 'textmap.txt'
        with open(self.filename, 'r') as f:
            self.rows = f.readlines()

        self.image_library = image_library
        self.screen = screen
        self.settings = settings

        # self.brick = self.image_library[1].convert_alpha()
        # self.brick = pygame.transform.scale(self.brick, (settings.tileSize, settings.tileSize))
        # self.map = []
        # self.rect = pygame.Rect(0, 0, settings.tileSize, settings.tileSize)
        # self.rect.x = 0
        # self.rect.y = settings.topOfGame
        #
        # self.mario_image = self.image_library[2].convert_alpha()
        # self.mario_image = pygame.transform.scale(self.mario_image, (settings.tileSize, settings.tileSize))
        # self.mario_rect = self.mario_image.get_rect()                               # Mario's x y position is not set
        #
        # self.parse_file()
        # self.print_map()                                                            # For testing + debugging

        self.bricks = []                                                            # Alternate loading
        self.brick_image = self.image_library[1].convert_alpha()
        self.brick_image = pygame.transform.scale(self.brick_image, (settings.tileSize, settings.tileSize))
        self.brick_rect = self.brick_image.get_rect()

        self.mario_image = self.image_library[2].convert_alpha()
        self.mario_image = pygame.transform.scale(self.mario_image, (settings.tileSize, settings.tileSize))
        self.mario_rect = self.mario_image.get_rect()



        self.deltaX = self.deltaY = settings.tileSize
        self.marioXInit = 0
        self.marioYInit = 0
        self.alternate_parse_file()

    def alternate_parse_file(self):
        r = self.brick_rect
        w, h = r.width, r.height
        dx, dy = self.deltaX, self.deltaY

        for nRow in range(len(self.rows)):
            row = self.rows[nRow]
            for nCol in range(len(row)):
                col = row[nCol]
                if col == 'x':
                    self.bricks.append(pygame.Rect(nCol * dx, nRow * dy, w, h))
                if col == 'm':
                    self.mario_rect = pygame.Rect(nCol * dx, nRow * dy, w, h)
                    self.marioXInit = self.mario_rect.x
                    self.marioYInit = self.mario_rect.y


    # def parse_file(self):
    #     try:
    #         with open("textmap.txt", "r") as f:
    #             map_row = []
    #             copy = self.rect.copy()
    #             while True:
    #                 flag = f.read(1)
    #                 if flag == "":
    #                     self.map.append(map_row)
    #                     break
    #                 elif flag == "\n":
    #                     copy.top = copy.bottom
    #                     copy.left = self.rect.left
    #                     self.map.append(map_row)
    #                     map_row = []
    #                 elif flag == "x":
    #                     map_row.append(copy.copy())
    #                     copy.left = copy.right
    #                 elif flag == "m":                                               # WIP, set Mario x y position here
    #                     self.mario_rect.x = 50
    #                     self.mario_rect.y = 50
    #                 else:
    #                     copy.left = copy.right
    #                     map_row.append(flag)
    #     except FileNotFoundError:
    #         print("The file '{}' was not found.".format('textmap.txt'))
    #         sys.exit(1)
    #     except Exception as ex:
    #         print("File error: '{}' when opening the file: '{}'".format(ex, 'textmap.txt'))
    #         traceback.print_exc()
    #         sys.exit(1)
    #
    # def draw_map(self):
    #     for row in self.map:
    #         for obj in row:
    #             if isinstance(obj, pygame.Rect):
    #                 self.screen.blit(self.brick, obj)
    #
    # def print_map(self):
    #     for obj in self.map:
    #         for item in obj:
    #             if isinstance(item, pygame.Rect):
    #                 print('x', end="")
    #             elif isinstance(item, str):
    #                 print(item, end="")
    #         print()

    def blitme(self):
        for rect in self.bricks:
            self.screen.blit(self.brick_image, rect)
        self.screen.blit(self.mario_image, self.mario_rect)
