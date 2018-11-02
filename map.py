import pygame
import traceback
import sys
import time


class Map:
    def __init__(self, image_library, screen, settings):
        self.image_library = image_library
        self.brick = self.image_library[1].convert_alpha()
        self.brick = pygame.transform.scale(self.brick, (settings.tileSize, settings.tileSize))
        self.screen = screen
        self.settings = settings

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
                        copy.left = copy.right
                    else:
                        copy.left = copy.right
                        map_row.append(flag)
        except FileNotFoundError:
            print("The file '{}' was not found.".format('textmap.txt'))
            sys.exit(1)
        except Exception as ex:
            print("File error: '{}' when opening the file: '{}'".format(ex, 'textmap.txt'))
            traceback.print_exc()
            sys.exit(1)

    def draw_map(self):
        for row in self.map:
            for obj in row:
                if isinstance(obj, pygame.Rect):
                    self.screen.blit(self.brick, obj)

    def print_map(self):
        for obj in self.map:
            for item in obj:
                if isinstance(item, pygame.Rect):
                    print('x', end="")
                elif isinstance(item, str):
                    print(item, end="")
            print()
