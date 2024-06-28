import random
import sys

import pygame
from pygame.locals import *

from .core.widgets import *

from .core.config import config


def event_scripts(event: pygame.event.Event):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    if event.type == KEYDOWN:
        print(Screen.root_location('cont'))
        pass

    if event.type == MOUSEBUTTONDOWN:
        pass

    pass


def no_event_scripts():
    pass
