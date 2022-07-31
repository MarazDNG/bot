from collections import namedtuple
from mu_window import mu_window
from . import game_methods

import time


Loc = namedtuple('Loc', ['map', 'warp'])

"""
    : param [0]: map
    : param [1]: warp
    : paramm [2]: level limit
"""


def warp_stadium_city():
    mu_window.press(ord("m"))
    time.sleep(0.5)
    mu_window.click_on_pixel((100, 115))
    time.sleep(3)


def warp_peace_swamp(portal_close_coords: tuple, portal_coords: tuple):
    game_methods.warp_to(PEACE_SWAMP[0])
    game_methods.go_to(portal_close_coords, PEACE_SWAMP[0])
    time.sleep(2)
    if game_methods.distance(game_methods.read_coords(), portal_coords) <= 2:
        game_methods.go_through_portal(portal_coords)


STADIUM = ("stadium", "stadium", 50)
STADIUM_CITY = ("stadium", warp_stadium_city, 100)
LORENCIA = ("lorencia", "lorencia", None)
ELBELAND2 = ("elbeland", "elbeland2", 20)
PEACE_SWAMP = ("peaceswamp", "peaceswamp", 300)
PEACE_SWAMP1 = ("peaceswamp", lambda: warp_peace_swamp(
    (139, 124), (139, 125)), 300)
PEACE_SWAMP3 = ("peaceswamp", lambda: warp_peace_swamp(
    (53, 24), (53, 14)), 300)
ATLANS2 = ("atlans", "atlans2", 80)
