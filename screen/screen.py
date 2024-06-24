import pygame
from pygame.locals import *

from .widgets import *

def create_screen():
    screen = Screen()

    # Tạo một widget con và thêm vào màn hình
    container = Container(200, 200, pygame.Color('blue'), "container")
    screen.add_child((50, 50), container)

    return screen