import pygame
from pygame.locals import *

from .widgets import *


def create_screen():
    screen = Screen()

    # Tạo một widget con và thêm vào màn hình
    background = Container(800, 600, id="bg", background_color=pygame.Color(140, 160, 90))
    form = Form(400, 400, "My Form", targeted=False)
    input = Input("My input", 300, font_size=50, targeted=False, id='i')
    form.add_child((10, 10), input)
    screen.add_child((0, 0), background)
    screen.add_child((100, 100), form)

    return screen
