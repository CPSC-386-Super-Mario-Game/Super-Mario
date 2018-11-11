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
                        coordinates = [copy.x, copy.y]
                        self.mario_coor.append(coordinates)
                        copy.left = copy.right
                    elif flag == "1" or flag == "p":
                        self.mystery_rect.append(copy.copy())
                        copy.left = copy.right
                    elif flag == "b":
                        self.brick_rect.append(copy.copy())
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
