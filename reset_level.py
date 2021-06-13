from player import *
from level import *
import global_variables


def reset_level():
    try:
        player1.set_pos(levels[global_variables.current_level][0].player_pos)
        player2.set_pos(levels[global_variables.current_level][1].player_pos)
        player1.x_speed = 0
        player1.y_speed = 0
        player2.x_speed = 0
        player2.y_speed = 0
        player1.level = levels[global_variables.current_level][0]
        player2.level = levels[global_variables.current_level][1]

        if global_variables.gravity < 0:
            global_variables.switch_grav()

    except IndexError:
        pass


def next_level():
    global_variables.current_level += 1
    global_variables.level_win = False
    reset_level()
