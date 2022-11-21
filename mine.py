import pygame
from pygame import *
import os

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"
ICON_DIR = os.path.dirname(__file__)


class Mine(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = pygame.transform.scale(image.load("%s/blocks/bombus.png" % ICON_DIR), (50, 50))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)