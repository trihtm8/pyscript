import pygame

from .screen.screen import create_screen
from .screen.scripts import applyScripts

def main():
    pygame.init()

    screen = create_screen()

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            applyScripts(event)

        screen.print()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
