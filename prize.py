import pygame
from pygame import *
import os

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"
ICON_DIR = os.path.dirname(__file__)  # Полный путь к каталогу с файлами


class Prize(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = pygame.transform.scale(image.load("%s/blocks/prize.png" % ICON_DIR), (30, 30))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)