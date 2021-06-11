import pygame
import sys
from element import *
from constants import *
import webbrowser as wb
# print(dir(pygame))

# Initializing pygame
pygame.init()
clock = pygame.time.Clock()


# Layouts:
#  - main_menu
#  - credits
#  - in_game
current_layout = "main_menu"


def set_layout(layout_name):
    global current_layout
    current_layout = layout_name
    print(current_layout)


def main():
    size = (0, 0)
    flags = pygame.FULLSCREEN | pygame.HWSURFACE
    screen = pygame.display.set_mode(size, flags, vsync=1)

    screen_centre = screen.get_width()/2, screen.get_height()/2

    layouts = {
    "main_menu":
        {"buttons":[
            # Close button
            Button(
                pos=(screen.get_width()-31, 30),
                function=sys.exit,
                size=(40, 40),
                text="X",
                text_offset=(0, -2),
                text_style="bold",
                text_color=(245, 208, 201),
                color=(189, 63, 38),
                hovered_color=(217, 92, 67),
                clicked_color=(222, 107, 84),
                curve=8,
                halo=20
            ),

            # Play button
            Button(
                pos=screen_centre,
                function=set_layout,
                args=["in_game"],
                size=(500, 100),
                text="Play",
                text_offset=(0, -9),
                text_color=WHITE,
                color=(37, 119, 219),
                hovered_color=(52, 136, 237),
                clicked_color=(70, 148, 242),
                curve=25,
                halo=20
            ),

            # Credits button
            Button(
                pos=(screen_centre[0], screen_centre[1] + 190),
                function=set_layout,
                args=["credits"],
                size=(400, 90),
                text="Credits",
                text_offset=(0, -9),
                text_color=WHITE,
                color=(37, 119, 219),
                hovered_color=(52, 136, 237),
                clicked_color=(70, 148, 242),
                curve=25,
                halo=20
            )

        ], "statics":[
            # Title
            Label(
                pos=(screen_centre[0], screen_centre[1]-screen.get_height()/4),
                text="Game title!",
                font_size=100,
                text_color=WHITE,
                tilt=15
            )
        ]},
    "credits":
        {"buttons":[
            # Close button
            Button(
                pos=(screen.get_width()-31, 30),
                function=sys.exit,
                size=(40, 40),
                text="X",
                text_offset=(0, -2),
                text_style="bold",
                text_color=(245, 208, 201),
                color=(189, 63, 38),
                hovered_color=(217, 92, 67),
                clicked_color=(222, 107, 84),
                curve=8,
                halo=20
            ),

            # Back button
            Button(
                pos=(60, 30),
                function=set_layout,
                args=["main_menu"],
                size=(100, 40),
                text="Back",
                text_color=WHITE,
                color=(37, 119, 219),
                hovered_color=(52, 136, 237),
                clicked_color=(70, 148, 242),
                curve=8,
                halo=20
            )
        ], "statics": [
            Label(
                pos=screen_centre,
                text="Hello",
                font_size=40,
                text_color=WHITE
            )
        ]},
    "in_game":
        {"buttons":[
            # Back button
            Button(
                pos=(60, 30),
                function=set_layout,
                args=["main_menu"],
                size=(100, 40),
                text="Back",
                text_color=WHITE,
                color=(37, 119, 219),
                hovered_color=(52, 136, 237),
                clicked_color=(70, 148, 242),
                curve=8,
                halo=20
            )
        ], "statics": []}
    }


    while True:
        t = clock.tick()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in layouts[current_layout]["buttons"]:
                    if i.clicked:
                        i.execute()

        # Resets display
        screen.fill(BG_COLOR)

        # Blits buttons
        for i in layouts[current_layout]["buttons"]:
            i.render(screen)

        for i in layouts[current_layout]["statics"]:
            i.render(screen)

        pygame.display.update()


if __name__ == "__main__":
    main()
