import pygame
import sys
from time import sleep
import webbrowser as wb
from element import *
from level import *
from player import *
from global_variables import *
# print(dir(pygame))

# Initializing pygame
pygame.init()
clock = pygame.time.Clock()

current_layout = "main_menu"


def set_layout(layout_name):
    global current_layout
    current_layout = layout_name


def reset_level():
    player1.x = 550
    player1.y = 974
    player2.x = 1350
    player2.y = 780

    if player1._grav < 0:
        switch_grav()


def BACK_BUTTON(layout_name):
    return Button(
        pos=(85, 30),
        function=set_layout,
        args=[layout_name],
        size=(150, 40),
        text="◄ Back",
        text_offset=(-5, -2),
        color=(37, 119, 219),
        hovered_color=(52, 136, 237),
        clicked_color=(70, 148, 242),
        curve=8,
        halo=30
    )


def GITHUB_BUTTON(link, pos):
    return Button(
        pos=pos,
        function=wb.open,
        args=[link],
        size=(380, 80),
        text="See GitHub",
        text_offset=(0, -3),
        color=(27, 191, 71),
        hovered_color=(35, 217, 84),
        clicked_color=(39, 227, 89),
        curve=25,
        halo=30
    )


def main():
    size = (1920, 1080)
    flags = pygame.FULLSCREEN | pygame.HWSURFACE
    screen = pygame.display.set_mode(size, flags, vsync=1)

    screen_centre = screen.get_width()/2, screen.get_height()/2
    centre_x = screen.get_width()/2
    centre_y = screen.get_height()/2

    CLOSE_BUTTON = Button(
        pos=(screen.get_width()-31, 30),
        function=sys.exit,
        size=(40, 40),
        text="X",
        text_offset=(0, -2),
        text_style="bold",
        text_color=WHITE,
        color=(240, 0, 0),
        hovered_color=(255, 69, 69),
        clicked_color=(245, 115, 115),
        curve=8,
        halo=30
    )

    layouts = {
    "main_menu":
        {"buttons":[
            CLOSE_BUTTON,

            # Play button
            Button(
                pos=screen_centre,
                function=set_layout,
                args=["in_game"],
                size=(500, 100),
                text="Play",
                text_offset=(0, -9),
                color=(37, 119, 219),
                hovered_color=(52, 136, 237),
                clicked_color=(70, 148, 242),
                curve=30,
                halo=30
            ),

            # Credits button
            Button(
                pos=(centre_x, centre_y + 190),
                function=set_layout,
                args=["credits"],
                size=(400, 90),
                text="Credits",
                text_offset=(0, -9),
                color=(27, 191, 71),
                hovered_color=(35, 217, 84),
                clicked_color=(39, 227, 89),
                curve=25,
                halo=30
            )

        ], "statics":[
            # Background
            Image(
                pos=screen_centre,
                path="images/bg.png"
            ),
            # Title
            Label(
                pos=(centre_x, centre_y-screen.get_height()/4),
                text="Game title!",
                font_size=100,
                tilt=15
            )
        ]},
    "credits":
        {"buttons":[
            CLOSE_BUTTON,
            BACK_BUTTON("main_menu"),
            GITHUB_BUTTON(
                link="https://github.com/TheSilvered",
                pos=(centre_x + 200, centre_y - 50)
            ),
            GITHUB_BUTTON(
                link="https://github.com/eli033",
                pos=(centre_x + 200, centre_y + 250)
            )

        ], "statics": [
            # Background
            Image(
                pos=screen_centre,
                path="images/bg.png"
            ),
            Label(
                pos=(centre_x, centre_y - screen.get_height()//2.7),
                text="This game was made by:",
                font_size=100
            ),

            Label(
                pos=(centre_x, centre_y - 180),
                font_size=60,
                text="Coding:"
            ),

            Label(
                pos=(centre_x - 200, centre_y - 50),
                font_size=60,
                text="TheSilvered"
            ),

            Label(
                pos=(centre_x, centre_y + 130),
                font_size=60,
                text="Graphics:"
            ),

            Label(
                pos=(centre_x - 135, centre_y + 250),
                font_size=60,
                text="eli033"
            )
        ]},
    "in_game":
        {"buttons":[
            CLOSE_BUTTON,
            BACK_BUTTON("main_menu"),

            # Switch for gravity
            Button(
                pos=(centre_x, 35),
                function=switch_grav,
                size=(300, 50),
                text="Switch gravity",
                text_offset=(0, -4),
                color=(59, 73, 227),
                hovered_color=(90, 102, 232),
                clicked_color=(125, 135, 245),
                curve=9,
                halo=30
            ),

            # Reset button
            Button(
                pos=(centre_x+500, 35),
                function=reset_level,
                size=(200, 50),
                text="Reset",
                text_offset=(0, -4),
                color=(59, 73, 227),
                hovered_color=(90, 102, 232),
                clicked_color=(125, 135, 245),
                curve=9,
                halo=30
            )

        ], "statics": [
            # Background
            Image(
                pos=screen_centre,
                path="images/bg.png"
            )
        ]}
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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    print(player1.pos)

        # Resets display
        screen.fill(BG_COLOR)

        for i in layouts[current_layout]["statics"]:
            i.render(screen)

        for i in layouts[current_layout]["buttons"]:
        
            i.render(screen)
        if current_layout == "in_game":
            levels[current_level][0].render(screen)
            levels[current_level][1].render(screen)
            player1.render(screen)
            player2.render(screen)

        pygame.display.update()


if __name__ == "__main__":
    main()
