from cgi import test

from game_logic import game_methods
from game_logic.djikstra import djikstra8
from game_logic.map import get_mu_map_list
from game_logic import game_menu
from game_logic import warps_mapping
from main import go_to_spot
from main import activate_window
from main import SAPI_DUOS
import time
import os


def test_warp(map):
    # DONE
    game_methods.warp_to(map)


def test_read_lvl():
    # DONE
    print(game_methods.read_lvl())


def test_walking_porting():
    game_methods.warp_to("lorencia")
    game_methods.go_to((134, 103), 'lorencia')


if __name__ == "__main__":
    activate_window()
    # game_methods.distribute_stats()
    # game_menu.server_selection()
    # go_to_spot(SAPI_DUOS)
    # game_methods.go_to((173, 217), "peaceswamp")
    # game_methods.go_through_portal((139, 125))
    warps_mapping.warp_peace_swamp1()
