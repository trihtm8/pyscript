import pygame

from .app.screen import create_screen
from .app.scripts import apply_scripts


def main():
    pygame.init()

    screen = create_screen()

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            apply_scripts(event)

        screen.print()
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
