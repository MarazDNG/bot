from game_methods.game_methods import read_lvl_from_frame, read_lvl
from mu_bot.game_api import warp_to
import pygetwindow as gw
import time


def activate_window():
    win = gw.getWindowsWithTitle("Player")[0]
    win.activate()
    time.sleep(2)


def test_warp(map):
    warp_to(map)


if __name__ == "__main__":
    activate_window()
    warp_to("lorencia")
