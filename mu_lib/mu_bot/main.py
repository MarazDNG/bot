#
# 1280 720
#

import time
import pygetwindow as gw

# from game_account_actions import game_login, server_selection
# from game_api import custom_attack, go_to, start_helper, warp_to
# from reset import reset

from game_methods import djikstra
from game_methods import game_methods
from game_methods import map
from arduino_api import arduino_api
from .keys import *

LORA_GOAL = (151, 73)
ELB_GOAL = (69, 59)
ATL_GOAL = (236, 50)


Lorencia = {'goal': LORA_GOAL,
            'range': (1, 20),
            'area': 'lorencia',
            }


def go_to(target_coords: tuple, map_name: str):
    current_coords = game_methods.read_coords()
    path = djikstra.djikstra8(
        current_coords, target_coords, map.get_mu_map_list(map_name))
    game_methods.get_to2(path)


def warp_to(area: str):
    arduino_api.send_ascii(KEY_RETURN)
    time.sleep(2)
    arduino_api.send_string(f'/warp {area}')
    time.sleep(2)
    arduino_api.send_ascii(KEY_RETURN)
    time.sleep(3)


def start_helper() -> None:
    arduino_api.send_ascii(KEY_HOME)


if __name__ == '__main__':
    win = gw.getWindowsWithTitle("Player")[0]
    win.activate()
    time.sleep(1.5)

    area = "lorencia"
    warp_to(area)

    while True:
        lvl = game_methods.read_lvl()
        time.sleep(1)

        if lvl < 20 and area != 'lorencia':
            area = 'lorencia'
            warp_to(area)
            time.sleep(5)

            go_to(LORA_GOAL, 'lorencia')

            if lvl < 10:
                time.sleep(10)
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
