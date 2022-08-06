from cgi import test

from game_logic import game_methods
from game_logic.djikstra import djikstra8
from game_logic.map import get_mu_map_list
from game_logic import game_menu
from game_logic import warps_mapping
from game_logic import spots

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
    game_methods.go_to_spot(spots.SAPI_DUOS)


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

if __name__ == "__main__":
    activate_window()
    # game_methods.distribute_stats()
    # game_menu.server_selection()
    # game_methods.go_to((173, 217), "peaceswamp")
    # game_methods.go_through_portal((139, 126))
    # warps_mapping.warp_peace_swamp1()
    # game_methods.get_to2(path_dev4)
    # test_walking_porting()
    # while True:
    #     game_methods.read_coords()
    test_go_to_sapi_duo()
