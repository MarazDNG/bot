
from game_logic import game_methods
from game_logic.djikstra import djikstra8
from game_logic import map
from game_logic import game_menu
from game_logic import warps_mapping
from game_logic import spots
from game_logic import reading
from mu_window import mu_window
from main import activate_window
import time
import os


def test_warp(map):
    # DONE
    game_methods.warp_to(map)


def test_read_lvl():
    # DONE
    print(game_methods.read_lvl())


def test_walking_porting():
    # game_methods.warp_to("lorencia")
    game_methods.go_to((134, 103), 'lorencia')


def test_go_to_sapi_duo():
    game_methods.go_to_spot(spots.BLUE_GOLEMS)


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


def bk_combo_helper():
    while True:
        while not game_methods._is_helper_on():
            mu_window.press(game_methods.KEY_HOME)
            time.sleep(0.5)
        mu_window.flashing_helper()
        time.sleep(20)
        mu_window.flashing_helper()


if __name__ == "__main__":

    activate_window()
    bk_combo_helper()
