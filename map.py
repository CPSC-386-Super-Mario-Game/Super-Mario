import pygame
import traceback
import sys


class Map:
    def __init__(self, image_library, screen, settings):
        self.filename = 'textmap.txt'
        with open(self.filename, 'r') as f:
            self.rows = f.readlines()

        self.image_library = image_library
        self.screen = screen
        self.settings = settings

        self.koopa_coor = []
        self.mario_coor = []

        self.brick_rect = []
        self.floor_rects = []
        self.goomba_rect = []
        self.mystery_rect = []
        self.solid_rect = []
        self.smallpipe_rect = []
        self.mediumpipe_rect = []
        self.largepipe_rect = []

        self.map = []
        self.rect = pygame.Rect(0, 0, settings.tileSize, settings.tileSize)
        self.rect.x = 0
        self.rect.y = settings.topOfGame

        self.parse_file()
        self.print_map()                                                            # For testing + debugging

    def parse_file(self):
        try:
            with open("textmap.txt", "r") as f:
                map_row = []
                copy = self.rect.copy()
                while True:
                    flag = f.read(1)
                    if flag == "":
                        self.map.append(map_row)
                        break
                    elif flag == "\n":
                        copy.top = copy.bottom
                        copy.left = self.rect.left
                        self.map.append(map_row)
                        map_row = []
                    elif flag == "x":
                        map_row.append(copy.copy())
                        self.floor_rects.append(copy.copy())
                        copy.left = copy.right
                    elif flag == "m":
                        map_row.append(flag)
                        coordinates = [copy.x, copy.y]
                        self.mario_coor.append(coordinates)
                        copy.left = copy.right
                    elif flag == "1" or flag == "p":
                        map_row.append(flag)
                        self.mystery_rect.append(copy.copy())
                        copy.left = copy.right
                    elif flag == "b":
                        map_row.append(flag)
                        self.brick_rect.append(copy.copy())
                        copy.left = copy.right
                    elif flag == "g":
                        map_row.append(flag)
                        self.goomba_rect.append(copy.copy())
                        copy.left = copy.right
                    elif flag == "s":
                        map_row.append(flag)
                        self.solid_rect.append(copy.copy())
                        copy.left = copy.right
                    elif flag == "u":
                        map_row.append(flag)
                        self.smallpipe_rect.append(copy.copy())
                        copy.left = copy.right
                    elif flag == "U":
                        map_row.append(flag)
                        self.mediumpipe_rect.append(copy.copy())
                        copy.left = copy.right
                    elif flag == "w":
                        map_row.append(flag)
                        self.largepipe_rect.append(copy.copy())
                        copy.left = copy.right
                    else:
                        copy.left = copy.right
                        map_row.append(flag)
        except FileNotFoundError:
            print("the file '{}' was not found.".format('textmap.txt'))
            sys.exit(1)
        except Exception as ex:
            print("file error: '{}' when opening the file: '{}'".format(ex, 'textmap.txt'))
            traceback.print_exc()
            sys.exit(1)

    def print_map(self):
        for obj in self.map:
            for item in obj:
                if isinstance(item, pygame.Rect):
                    print('x', end="")
                elif isinstance(item, str):
                    print(item, end="")
            print()


class UnderworldMap:
    def __init__(self, image_library, screen, settings):
        self.filename = 'underworld textmap.txt'
        with open(self.filename, 'r') as f:
            self.rows = f.readlines()
        self.image_library = image_library
        self.screen = screen
        self.settings = settings

        self.mario_coor = []

        self.brick_rect = []
        self.floor_rect = []
        self.leftpipe_rect = []
        self.hugepipe_rect = []
        self.coin_rect = []

        self.map = []
        self.rect = pygame.Rect(0, 0, settings.tileSize, settings.tileSize)
        self.rect.x = 0
        self.rect.y = settings.topOfGame

        self.parse_underworld_file()

    def parse_underworld_file(self):
        try:
            with open("underworld textmap.txt", "r") as f:
                map_row = []
                copy = self.rect.copy()
                while True:
                    flag = f.read(1)
                    if flag == "":
                        self.map.append(map_row)
                        break
                    elif flag == "\n":
                        copy.top = copy.bottom
                        copy.left = self.rect.left
                        self.map.append(map_row)
                        map_row = []
                    elif flag == "X":
                        map_row.append(copy.copy())
                        self.floor_rect.append(copy.copy())
                        copy.left = copy.right
                    elif flag == "m":
                        coordinates = [copy.x, copy.y]
                        self.mario_coor.append(coordinates)
                        copy.left = copy.right
                    elif flag == "B":
                        self.brick_rect.append(copy.copy())
                        copy.left = copy.right
                    elif flag == "q":
                        self.leftpipe_rect.append(copy.copy())
                        copy.left = copy.right
                    elif flag == "W":
                        self.hugepipe_rect.append(copy.copy())
                        copy.left = copy.right
                    elif flag == "c":
                        self.coin_rect.append(copy.copy())
                        copy.left = copy.right
                    else:
                        copy.left = copy.right
                        map_row.append(flag)
        except FileNotFoundError:
            print("the file '{}' was not found.".format('textmap.txt'))
            sys.exit(1)
        except Exception as ex:
            print("file error: '{}' when opening the file: '{}'".format(ex, 'textmap.txt'))
            traceback.print_exc()
            sys.exit(1)