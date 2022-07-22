#
# 1280 720
#

from math import sqrt
import time
from game_account_actions import game_login, server_selection
from i_arduino import *
from i_game import get_lvl
from mu.mu_bot.game_api import custom_attack, go_to, start_helper, warp_to
from mu_lib.game_methods.djikstra import djikstra8
from reset import reset
from mu_lib.game_methods import game_methods
from mu_lib.game_methods.Map import get_mu_map_list

SURR = {
    (0, 0): (645, 323),

    (-1, 1): (640, 278),
    (0, 1): (677, 300),
    (1, 1): (715, 333),
    (1, 0): (700, 366),
    (1, -1): (635, 373),
    (0, -1): (597, 366),
    (-1, -1): (535, 330),
    (-1, 0): (600, 300),

    (-2, 0): (541, 253),
    (0, 2): (743, 263),
    (2, 0): (762, 405),
    (0, -2): (527, 409),
    (-2, -2): (424, 333),
    (-2, 2): (645, 209),
    (2, 2): (863, 333),
    (2, -2): (646, 500),

    (-2, 1): (593, 237),
    (-1, 2): (696, 237),

    (1, 2): (804, 300),
    (2, 1): (816, 366),

    (2, -1): (582, 449),
    (1, -2): (709, 449),

    (-1, -2): (476, 366),
    (-2, -1): (489, 300),
}
LORA_GOAL = (151, 73)
ELB_GOAL = (69, 59)
ATL_GOAL = (236, 50)


Lorencia = {'goal': LORA_GOAL,
            'range': (1, 20),
            'area': 'lorencia',
            }


def go_to(target_coords: tuple, map_name: str):
    current_coords = game_methods.read_coords()
    path = djikstra8(current_coords, target_coords, get_mu_map_list(map_name))
    game_methods.get_to2(path)


if __name__ == '__main__':

    time.sleep(1)
    area = None
    in_process = False

    while True:
        lvl = get_lvl()
        time.sleep(1)

        if lvl < 20 and area != 'lorencia':
            area = 'lorencia'
            warp_to(area)
            time.sleep(5)

            go_to(LORA_GOAL, 'lorencia')

            if lvl < 10:
                custom_attack()
            else:
                start_helper()

        elif lvl in range(20, 80) and area != 'elbeland':
            area = 'elbeland'
            warp_to(area)
            time.sleep(5)
            go_to(ELB_GOAL, 'elbeland')
            start_helper()

        elif lvl in range(80, 140) and area != 'atlans':
            area = 'atlans'
            warp_to(area)
            time.sleep(5)
            go_to(ATL_GOAL, 'atlans')
            start_helper()

        elif lvl in range(140, 280):
            pass

        elif lvl in range(280, 400):
            area = 'swampofpeace'
            warp_to(area)
            print("WELL DONE!!!")
            print('\a')
            break

        elif lvl == 400:
            server_selection()
            reset()
            game_login()
