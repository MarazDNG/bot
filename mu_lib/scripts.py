from cgi import test

from game_methods import game_methods
from game_methods.djikstra import djikstra8
from game_methods.map import get_mu_map_list

import pygetwindow as gw
import time
import os


def activate_window():
    win = gw.getWindowsWithTitle("Player")[0]
    win.activate()
    time.sleep(2)


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
    from game_methods.game_menu import server_selection, game_login
    from game_methods.reset import reset
    # server_selection()
    # reset()
    game_login()
