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
    player1.set_pos(levels[current_level][0].player_pos)
    player2.set_pos(levels[current_level][1].player_pos)
    player1.x_speed = 0
    player1.y_speed = 0
    player2.x_speed = 0
    player2.y_speed = 0    

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
        color=(59, 73, 227),
        hovered_color=(90, 102, 232),
        clicked_color=(125, 135, 245),
        curve=8,
        halo=30
    )


def LINK_BUTTON(link, pos, txt):
    return Button(
        pos=pos,
        function=wb.open,
        args=[link],
        size=(380, 80),
        text=txt,
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

    level_win = False

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
                color=(59, 73, 227),
                hovered_color=(90, 102, 232),
                clicked_color=(125, 135, 245),
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
                text="Astronauts!",
                font_size=100,
                tilt=15
            )
        ]},
    "credits":
        {"buttons":[
            CLOSE_BUTTON,
            BACK_BUTTON("main_menu"),

            Button(
                pos=(centre_x + 220, centre_y + 100),
                function=wb.open,
                args=["https://github.com/TheSilvered"],
                size=(380, 80),
                text="GitHub",
                text_offset=(0, -3),
                color=(27, 191, 71),
                hovered_color=(35, 217, 84),
                clicked_color=(39, 227, 89),
                curve=25,
                halo=30
            ),

            Button(
                pos=(centre_x - 220, centre_y + 100),
                function=wb.open,
                args=["https://thesilvered.itch.io/"],
                size=(380, 80),
                text="itch.io",
                text_offset=(0, -3),
                color=(245, 17, 66),
                hovered_color=(245, 54, 95),
                clicked_color=(232, 107, 134),
                curve=25,
                halo=30
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
                pos=(centre_x, centre_y - 50),
                font_size=60,
                text="TheSilvered"
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
                size=(120, 50),
                text="Reset",
                text_offset=(0, -4),
                color=(240, 0, 0),
                hovered_color=(255, 69, 69),
                clicked_color=(245, 115, 115),
                curve=9,
                halo=30
            )

        ], "statics": [
            # Background
            Image(
                pos=screen_centre,
                path="images/bg.png"
            )
        ]},
    "win_screen":
        {"buttons": [
            CLOSE_BUTTON,
            BACK_BUTTON("main_menu")

        ], "statics": [
            # Background
            Image(
                pos=screen_centre,
                path="images/bg.png"
            ),
            Label(
                pos=screen_centre,
                text="Contratulations, you won!",
                font_size=30
            )
        ]}
    }

    # next_level_button = Button(
    #     pos=
    # )


    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in layouts[current_layout]["buttons"]:
                    if i.clicked:
                        i.execute()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    s = pygame.image.load("images/1.png")
                    smooth_scale(s, screen, (1000, 1000), 10, screen_centre)


        # Resets display
        screen.fill(BG_COLOR)

        for i in layouts[current_layout]["statics"]:
            i.render(screen)

        for i in layouts[current_layout]["buttons"]:
        
            i.render(screen)
        if current_layout == "in_game":
            try:
                levels[current_level][0].render(screen)
                levels[current_level][1].render(screen)
                player1.render(screen)
                player2.render(screen)
            
            except IndexError:
                set_layout("win_screen")

            if player1.on_door and player2.on_door or level_win:
                bg = Image(screen_centre, "images/next_level_bg.png")
                bg.render(screen)
                level_win = True
                reset_level()


        pygame.display.update()


if __name__ == "__main__":
    main()
