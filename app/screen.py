import pygame

from .core.widgets import *
from .core.config import config


def create_screen():
    screen = Screen(1080, 980)

    windown = Window(500, 500, "My Window", id="w")
    container = Container(300, 300, background_color=pygame.Color('gray'),id='cont')
    image = Container(100, 100, background_color=pygame.Color('green'), id="im")
    image2 = Container(50, 50, background_color=pygame.Color('blue'), id="im2")
    image.add_child((0, 0), image2)
    container.add_child((0, 0), image)
    windown.add_child((0, 0), container)
    windown.add_child((0, 0), image)
    screen.add_child((100, 100), windown)

    return screen
