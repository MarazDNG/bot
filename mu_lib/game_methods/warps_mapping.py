from collections import namedtuple
from mu_window import mu_window

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


STADIUM = ("stadium", "stadium", 50)
STADIUM_CITY = ("stadium", warp_stadium_city, 100)
LORENCIA = ("lorencia", "lorencia", None)
ELBELAND2 = ("elbeland", "elbeland2", 20)
PEACE_SWAMP = ("peaceswamp", "peaceswamp", 300)
ATLANS2 = ("atlans", "atlans2", 80)
