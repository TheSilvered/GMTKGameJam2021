import pygame
import sys
from time import sleep
import webbrowser as wb
from element import *
from level import *
from player import *
import global_variables
import reset_level
# print(dir(pygame))

# Initializing pygame
pygame.init()
clock = pygame.time.Clock()

current_layout = "main_menu"
music = pygame.mixer.music.load("sounds/music.mp3")
pygame.mixer.music.set_volume(0.5)


def close():
    pygame.mixer.music.fadeout(300)
    sleep(0.3)
    sys.exit()


def set_layout(layout_name):
    global current_layout
    current_layout = layout_name
    if layout_name == "in_game":
        global_variables.current_level = 0
        global_variables.level_win = False
        reset_level.reset_level()


def main():
    size = (0, 0)
    flags = pygame.FULLSCREEN | pygame.HWSURFACE
    screen = pygame.display.set_mode(size, flags, vsync=1)

    screen1080p = pygame.Surface((1920, 1080))

    icon = pygame.image.load("images/icon.png")
    pygame.display.set_caption("Astronauts!")
    pygame.display.set_icon(icon)
     
    pygame.mixer.music.play(-1)

    screen_centre = screen1080p.get_width()/2, screen1080p.get_height()/2
    centre_x = screen1080p.get_width()/2
    centre_y = screen1080p.get_height()/2

    scale_width = screen.get_width()
    scale_height = int(1080 * (screen.get_width()/1920))
    scale = (scale_width, scale_height)

    CLOSE_BUTTON = Button(
        pos=(screen1080p.get_width()-31, 30),
        window_scale=scale,
        function=close,
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

    def BACK_BUTTON(layout_name):
        return Button(
            pos=(85, 30),
            window_scale=scale,
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
            window_scale=scale,
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

    layouts = {
    "main_menu":
        {"buttons":[
            CLOSE_BUTTON,

            # Play button
            Button(
                pos=(centre_x, centre_y - 60),
                window_scale=scale,
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
                pos=(centre_x, centre_y + 130),
                window_scale=scale,
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
                pos=(centre_x, centre_y-320),
                text="Astronauts!",
                font_size=150,
                tilt=15
            ),

            Label(
                pos=(centre_x, centre_y + 360),
                text="Use WASD or the arrow keys to move",
                font_size=50
            ),
            Label(
                pos=(centre_x, centre_y + 420),
                text="Use G or press the button to switch the gravity",
                font_size=50
            ),
            Label(
                pos=(centre_x, centre_y + 480),
                text="Use R or press the button to reset the level",
                font_size=50
            )
        ]},
    "credits":
        {"buttons":[
            CLOSE_BUTTON,
            BACK_BUTTON("main_menu"),

            Button(
                pos=(centre_x + 220, centre_y),
                window_scale=scale,
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
                pos=(centre_x - 220, centre_y),
                window_scale=scale,
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
                pos=(centre_x, centre_y - screen1080p.get_height()//2.7),
                text="This game was made by:",
                font_size=100
            ),

            Label(
                pos=(centre_x, centre_y - 150),
                font_size=65,
                text="TheSilvered"
            ),

            Label(
                pos=(centre_x, centre_y + 220),
                font_size=80,
                text="Music by:"
            ),

            Label(
                pos=(centre_x, centre_y + 350),
                font_size=65,
                text="sscheidl"
            )

        ]},
    "in_game":
        {"buttons":[
            CLOSE_BUTTON,
            BACK_BUTTON("main_menu"),

            # Switch for gravity
            Button(
                pos=(centre_x, 35),
                window_scale=scale,
                function=global_variables.switch_grav,
                size=(310, 50),
                text="Switch gravity (G)",
                text_offset=(0, -4),
                color=(59, 73, 227),
                hovered_color=(90, 102, 232),
                clicked_color=(125, 135, 245),
                sound=pygame.mixer.Sound("sounds/grav.wav"),
                curve=9,
                halo=30
            ),

            # Reset button
            Button(
                pos=(centre_x+500, 35),
                window_scale=scale,
                function=reset_level.reset_level,
                size=(160, 50),
                text="Reset (R)",
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
                font_size=100
            )
        ]}
    }

    next_level_button = Button(
        pos=screen_centre,
        window_scale=scale,
        function=reset_level.next_level,
        size=(400, 100),
        text="Next level",
        text_offset=(0, -9),
        color=(59, 73, 227),
        hovered_color=(90, 102, 232),
        clicked_color=(125, 135, 245),
        curve=30,
        halo=30
    )


    while True:
        clock.tick()

        for event in pygame.event.get():
            
            # Even in fullscreen, this might appen
            # Ex. when you right click on the icon on the taskbar
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    close()
                elif event.key == pygame.K_g:
                    global_variables.switch_grav()
                    sound = pygame.mixer.Sound("sounds/grav.wav")
                    pygame.mixer.Sound.play(sound)
                elif event.key == pygame.K_r:
                    reset_level.reset_level()
                elif event.key == pygame.K_p:
                    print(player1.pos, player2.pos)
                elif event.key == pygame.K_F6:
                    reset_level.next_level()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in layouts[current_layout]["buttons"]:
                    if i.clicked:
                        i.execute()
                if global_variables.level_win and next_level_button.clicked:
                    next_level_button.execute()

        # Resets display
        screen1080p.fill(BG_COLOR)

        for i in layouts[current_layout]["statics"]:
            i.render(screen1080p)

        for i in layouts[current_layout]["buttons"]:
            i.render(screen1080p)

        if current_layout == "in_game":
            try:
                levels[global_variables.current_level][0].render(screen1080p)
                levels[global_variables.current_level][1].render(screen1080p)
            
            except IndexError:
                set_layout("win_screen")

            if player1.on_door and player2.on_door:
                global_variables.level_win = True
            else:
                global_variables.level_win = False

            if global_variables.level_win:
                bg = Image(screen_centre, "images/next_level_bg.png")
                bg.render(screen1080p)
                next_level_button.render(screen1080p)
                global_variables.level_win = True

            else:
                player1.render(screen1080p)
                player2.render(screen1080p)


            if global_variables.current_level == 0 and not global_variables.level_win:
                info_label_l1 = Label(
                    pos=(centre_x, centre_y - 40),
                    text="Get both the astronauts on",
                    font_size=70
                )
                info_label_l2 = Label(
                    pos=(centre_x, centre_y + 40),
                    text="the doors at the same time",
                    font_size=70
                )
                info_label_l1.render(screen1080p)
                info_label_l2.render(screen1080p)

        screen_adapted = pygame.transform.scale(screen1080p, scale)
        screen.blit(screen_adapted, (0, 0))
        pygame.display.update()


if __name__ == "__main__":
    main()
