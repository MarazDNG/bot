import win32api
import time
import pyautogui
from game_logic import map
from game_logic import game_menu
from game_logic.Player import Player
import time
import os
from game_logic import memory
import window_api

path_dev4 = [
    (72, 177),
    (73, 177),
    (74, 177),
    (75, 177),
    (76, 178),
    (77, 179),
    (78, 180),
    (79, 181),
    (80, 182),
]


def preset():
    p = Player("Consumer")
    p.try_reset()


def close():
    p = Player("Consumer")
    window_api.window_activate_by_handler(p._window_hwnd)
    p.close_game()


def modify_config():
    from game_logic import meth

    meth.modify_config("Silco:stats:str=f4000")


if __name__ == "__main__":
    # win_id = mu_window.window_id_by_title("Consumer")
    # while True:
    #     [print(unit.name, unit.coords)
    #      for unit in memory.get_surrounding_units(win_id) if "rc" in unit.name]
    # exit()
    time.sleep(2)
    import arduino_api

    arduino_api.ard_init(3)
    modify_config()
