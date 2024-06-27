import random
import sys

import pygame
from pygame.locals import *

from .core.widgets import *


def event_scripts(event: pygame.event.Event):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    pass


def no_event_scripts():
    pass
