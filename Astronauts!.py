import gameassets as ga

import pygame
import sys
from time import sleep
import webbrowser as wb
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
click = pygame.mixer.Sound("sounds/click.wav")
grav = pygame.mixer.Sound("sounds/grav.wav")


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

    screen_centre = (960, 540)
    centre_x = 960
    centre_y = 540

    scale_width = screen.get_width()
    scale_height = int(1080 * (screen.get_width()/1920))
    scale = (scale_width, scale_height)

    BACKGROUND = ga.Element(
        c_pos=screen_centre,
        size=(1920, 1080),
        texture=pygame.image.load("images/bg.png")
    )
    BACKGROUND._texture = BACKGROUND._texture.convert()  # Optimizes blitting
    
    info = ga.Label(
        c_pos=screen_centre,
        text="Loading...",
        text_size=100,
        color=WHITE
    )

    BACKGROUND.render(screen)
    info.render(screen)
    pygame.display.update()

    CLOSE_BUTTON = ga.Button(
        c_pos=(1890, 30),
        size=(40, 40),
        text_kwargs= {
            "text": "X",
            "text_style": "bold",
            "color": WHITE,
            "text_size": 30,
            "offset": (0, -2)
        },
        # color_normal=(240, 0, 0),
        # color_hovered=(255, 69, 69),
        # color_clicked=(245, 115, 115),
        make_texture=False,
        curve=10,
        halo=15,
        sound=click,
        window_scale=scale,
        function=close,
    )

    def BACK_BUTTON(layout_name):
        return ga.Button(
            c_pos=(85, 30),
            size=(150, 40),
            text_kwargs={
                "text": "Back",
                "text_size": 32,
                "color": WHITE,
                "offset": (0, -2)
            },
            # color_normal=(59, 73, 227),
            # color_hovered=(90, 102, 232),
            # color_clicked=(125, 135, 245),
            make_texture=False,
            curve=10,
            halo=15,
            sound=click,
            window_scale=scale,
            function=set_layout,
            args=[layout_name]
        )


    layouts = {
    "main_menu":
        {"buttons":[
            CLOSE_BUTTON,

            # Play button
            ga.Button(
                c_pos=(centre_x, centre_y - 60),
                size=(500, 120),
                text_kwargs={
                    "text": "Play",
                    "text_size": 75,
                    "color": WHITE,
                    "offset": (0, -9)
                },
                # color_normal=(59, 73, 227),
                # color_hovered=(90, 102, 232),
                # color_clicked=(125, 135, 245),
                make_texture=False,
                curve=30,
                halo=15,
                sound=click,
                window_scale=scale,
                function=set_layout,
                args=["in_game"],
            ),

            # Credits button
            ga.Button(
                c_pos=(centre_x, centre_y + 130),
                size=(400, 90),
                text_kwargs={
                    "text": "Credits",
                    "text_size": 68,
                    "color": WHITE,
                    "offset": (0, -5)
                },
                # color_normal=(27, 191, 71),
                # color_hovered=(35, 217, 84),
                # color_clicked=(39, 227, 89),
                make_texture=False,
                curve=25,
                halo=15,
                sound=click,
                window_scale=scale,
                function=set_layout,
                args=["credits"]
            )

        ], "statics":[
            # Title
            ga.Label(
                c_pos=(centre_x, centre_y-320),
                text="Astronauts!",
                text_size=150,
                color=WHITE,
                tilt=15
            ),

            ga.Label(
                c_pos=(centre_x, centre_y + 360),
                text="Use WASD or the arrow keys to move",
                text_size=50,
                color=WHITE
            ),
            ga.Label(
                c_pos=(centre_x, centre_y + 420),
                text="Use G or press the button to switch the gravity",
                text_size=50,
                color=WHITE
            ),
            ga.Label(
                c_pos=(centre_x, centre_y + 480),
                text="Use R or press the button to reset the level",
                text_size=50,
                color=WHITE
            )
        ]},
    "credits":
        {"buttons":[
            CLOSE_BUTTON,
            BACK_BUTTON("main_menu"),

            ga.Button(
                c_pos=(centre_x + 220, centre_y),
                size=(380, 80),
                text_kwargs={
                    "text": "GitHub",
                    "text_size": 60,
                    "color": WHITE,
                    "offset": (0, -3)
                },
                # color_normal=(27, 191, 71),
                # color_hovered=(35, 217, 84),
                # color_clicked=(39, 227, 89),
                make_texture=False,
                curve=25,
                halo=15,
                sound=click,
                window_scale=scale,
                function=wb.open,
                args=["https://github.com/TheSilvered"]
            ),

            ga.Button(
                c_pos=(centre_x - 220, centre_y),
                size=(380, 80),
                text_kwargs={
                    "text": "itch.io",
                    "text_size": 60,
                    "color": WHITE,
                    "offset": (0, -3)
                },
                # color_normal=(245, 17, 66),
                # color_hovered=(245, 54, 95),
                # color_clicked=(232, 107, 134),
                make_texture=False,
                curve=25,
                halo=15,
                sound=click,
                window_scale=scale,
                function=wb.open,
                args=["https://thesilvered.itch.io/"]
            )

        ], "statics": [
            ga.Label(
                c_pos=(centre_x, centre_y - screen1080p.get_height()//2.7),
                text="This game was made by:",
                text_size=100,
                color=WHITE
            ),

            ga.Label(
                c_pos=(centre_x, centre_y - 150),
                text="TheSilvered",
                text_size=65,
                color=WHITE
            ),

            ga.Label(
                c_pos=(centre_x, centre_y + 220),
                text="Music by:",
                text_size=80,
                color=WHITE
            ),

            ga.Label(
                c_pos=(centre_x, centre_y + 350),
                text="sscheidl",
                text_size=65,
                color=WHITE
            )

        ]},
    "in_game":
        {"buttons":[
            CLOSE_BUTTON,
            BACK_BUTTON("main_menu"),

            # Switch for gravity
            ga.Button(
                c_pos=(centre_x, 35),
                size=(310, 50),
                text_kwargs={
                    "text": "Switch gravity (G)",
                    "color": WHITE,
                    "text_size": 38,
                    "offset": (0, -4)
                },
                # color_normal=(59, 73, 227),
                # color_hovered=(90, 102, 232),
                # color_clicked=(125, 135, 245),
                make_texture=False,
                curve=9,
                halo=15,
                sound=grav,
                window_scale=scale,
                function=global_variables.switch_grav
            ),

            # Reset button
            ga.Button(
                c_pos=(centre_x+500, 35),
                size=(160, 50),
                text_kwargs={
                    "text": "Reset (R)",
                    "color": WHITE,
                    "text_size": 38,
                    "offset": (0, -4)
                },
                # color_normal=(240, 0, 0),
                # color_hovered=(255, 69, 69),
                # color_clicked=(245, 115, 115),
                make_texture=False,
                curve=9,
                halo=15,
                sound=click,
                window_scale=scale,
                function=reset_level.reset_level
            )

        ], "statics": []
    },
    "win_screen":
        {"buttons": [
            CLOSE_BUTTON,
            BACK_BUTTON("main_menu")

        ], "statics": [
            ga.Label(
                c_pos=screen_centre,
                text="Contratulations, you won!",
                text_size=100,
                color=WHITE
            )
        ]}
    }

    next_level_button = ga.Button(
        c_pos=screen_centre,
        size=(400, 100),
        text_kwargs={
            "text": "Next level",
            "color": WHITE,
            "text_size": 75,
            "offset": (0, -9)
        },
        # color_normal=(59, 73, 227),
        # color_hovered=(90, 102, 232),
        # color_clicked=(125, 135, 245),
        make_texture=False,
        curve=30,
        halo=15,
        sound=click,
        window_scale=scale,
        function=reset_level.next_level
    )

    for i in layouts:
        for idx, j in enumerate(layouts[i]["buttons"]):
            # j.save_textures(f"images/{i}{idx}")
            with open(f"images/{i}{idx}tn.texture", "rb") as f:
                tn = f.read()
            with open(f"images/{i}{idx}th.texture", "rb") as f:
                th = f.read()
            with open(f"images/{i}{idx}tc.texture", "rb") as f:
                tc = f.read()
            j.buffertexture(tn, th, tc)

    fps = ga.Label(
        text="0",
        text_size=30,
        color=WHITE,
        pos=(0, 0)
    )

    while True:
        t = clock.tick(FRAMERATE) / (1000/FRAMERATE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    close()
                elif event.key == pygame.K_g and current_layout == "in_game":
                    global_variables.switch_grav()
                    pygame.mixer.Sound.play(grav)
                elif event.key == pygame.K_r and current_layout == "in_game":
                    reset_level.reset_level()
                elif event.key == pygame.K_p:
                    print(player1.pos, player2.pos)
                elif event.key == pygame.K_F6:
                    reset_level.next_level()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in layouts[current_layout]["buttons"]:
                    if i.clicked:
                        i.run()
                if global_variables.level_win and next_level_button.clicked:
                    next_level_button.run()

        BACKGROUND.render(screen1080p)

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
                bg = ga.Element(
                    c_pos=screen_centre,
                    texture=pygame.image.load("images/next_level_bg.png"),
                    size=(592, 592)
                )
                bg.render(screen1080p)
                next_level_button.render(screen1080p)
                global_variables.level_win = True

            else:
                player1.render(screen1080p, t)
                player2.render(screen1080p, t)


            if global_variables.current_level == 0 and not global_variables.level_win:
                info_label_l1 = ga.Label(
                    c_pos=(centre_x, centre_y - 40),
                    text="Get both the astronauts on",
                    text_size=70,
                    color=WHITE
                )
                info_label_l2 = ga.Label(
                    c_pos=(centre_x, centre_y + 40),
                    text="the doors at the same time",
                    text_size=70,
                    color=WHITE
                )
                info_label_l1.render(screen1080p)
                info_label_l2.render(screen1080p)

        for i in layouts[current_layout]["statics"]:
            i.render(screen1080p)

        for i in layouts[current_layout]["buttons"]:
            i.render(screen1080p)

        fps.change_text(str(int(clock.get_fps())))
        fps.render(screen1080p)

        screen_adapted = pygame.transform.scale(screen1080p, scale)
        screen.blit(screen_adapted, (0, 0))
        pygame.display.update()


if __name__ == "__main__":
    main()
