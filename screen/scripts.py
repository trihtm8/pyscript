import random
import sys
import pygame
from pygame.locals import *

from .widgets import *


def apply_scripts(event: pygame.event.Event):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    if event.type == KEYDOWN:
        print(event)
        input = Screen().getElementById('i')
        bg = Screen().getElementById('bg')
        bg.background_color = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        input.value += event.unicode

    pass
