import pygame
import sys
from element import *
from constants import *

# Initializing pygame
pygame.init()
clock = pygame.time.Clock()

# Global variables
is_in_game = False

# print(dir(pygame))


def toggle_playing():
    global is_in_game
    is_in_game = not is_in_game
    print(is_in_game)


def __main__():
    size = (0, 0)
    flags = pygame.FULLSCREEN | pygame.HWSURFACE
    screen = pygame.display.set_mode(size, flags, vsync=1)

    screen_centre = screen.get_width()/2, screen.get_height()/2

    functions = {
        "sys.exit": sys.exit,
        "toggle_playing": toggle_playing
    }

    title = Label(
        text="Game title!",
        pos=(screen_centre[0], screen_centre[1]-screen.get_height()/4),
        text_color=WHITE,
        text_style="",
        font_size=100,
        font_face=FONT_FACE, 
        tilt=15
    )

    buttons = [
        # Close button
        Button(
            pos=(screen.get_width()-31, 30),
            function="sys.exit",
            size=(40, 40),
            text="X",
            text_style="bold",
            text_color=(245, 208, 201),
            color=(189, 63, 38),
            hovered_color=(217, 92, 67),
            clicked_color=(222, 107, 84),
            curve=10,
        ),

        # Play button
        Button(
            pos=screen_centre,
            function="toggle_playing",
            size=(500, 100),
            text="Play",
            text_offset=(0, -9),
            text_color=WHITE,
            color=(37, 119, 219),
            hovered_color=(52, 136, 237),
            clicked_color=(70, 148, 242),
            curve=25
        )
    ]

    while True:
        t = clock.tick()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in buttons:
                    if i.clicked:
                        functions[i.func]()

        # Resets display
        screen.fill(BG_COLOR)

        # Blits buttons
        for i in buttons:
            i.render(screen)

        title.render(screen)
        pygame.display.update()


if __name__ == "__main__":
    __main__()
