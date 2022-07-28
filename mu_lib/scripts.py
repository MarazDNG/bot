from cgi import test
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
    # activate_window()
    # test_walking_porting()
    # go_to((69, 59), 'elbeland')
    m = get_mu_map_list("elbeland")
    p = djikstra8((99, 53), (72, 50), m)
    print(p)
