import pygame

from .app.screen import create_screen
from .app.scripts import event_scripts
from .app.scripts import no_event_scripts


def main():
    pygame.init()

    screen = create_screen()

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            event_scripts(event)
        no_event_scripts()

        screen.print()
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
