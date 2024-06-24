import sys
import pygame
from pygame.locals import *

from .widgets import *

def applyScripts(event: pygame.event.Event):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    if event.type == KEYDOWN:
        screen = Screen()
        print(screen.id)

    pass
