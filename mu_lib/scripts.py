from cgi import test

from yaml import SequenceStartEvent
from game_methods.game_methods import read_lvl
from mu_bot.main import go_to
from mu_bot.game_api import warp_to
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
    warp_to(map)


def test_read_lvl():
    # DONE
    print(read_lvl())


def test_walking_porting():
    warp_to("lorencia")
    go_to((134, 103), 'lorencia')


if __name__ == "__main__":
    activate_window()
    from mu_bot.game_account_actions import server_selection, game_login
    from mu_bot.reset import reset
    # server_selection()
    # reset()
    game_login()
