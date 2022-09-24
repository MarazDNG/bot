
from game_logic import game_methods
from game_logic.djikstra import djikstra8
from game_logic import map
from game_logic import game_menu
from game_logic import reading
from game_logic.Player import Player
from game_logic.reading import read_coords
from mu_window import mu_window
from main import activate_window
import time
import os
from game_logic import memory


def test_warp(map):
    # DONE
    game_methods.warp_to(map)


def test_read_lvl():
    # DONE
    print(game_methods.read_lvl())


def test_walking_porting():
    # game_methods.warp_to("lorencia")
    game_methods.go_to((134, 103), 'lorencia')


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
    # activate_window("Silco")
    # print(Player("Silco").coords)
    # bk_combo_helper()
    # while True:
    #     try:
    #         i = 0
    #         while True:
    #             print(i, ": ", read_coords())
    #             i += 1
    #     finally:
    #         pass
    # p.distribute_stats()
    # print(memory.my_coords_by_id(mu_window.window_id_by_title("Consumer")))
    # print(memory.my_coords_by_id(14008))
    # print(memory.my_coords_by_id(16084))
    while True:
        units = memory.get_surrounding_units()
        [print(unit.name, unit.coords)
         for unit in units if "Lunar" in unit.name]
        time.sleep(1)
