#
# Game interface.
#


import numpy
import time
import itertools
from datetime import datetime, timedelta

from .exceptions import DeathException
from .meth import distance
from .memory import surrounding_units
from .walking_straight import _walk_on_shortest_straight
from .walking_vector import go_through_path, go_direction
from .map import get_mu_map_list
from .djikstra import djikstra8
import contextlib
from arduino_api import arduino_api
import window_api
# from conf.conf import SURR, KEY_HOME, KEY_RETURN, STR, AGI, VIT, ENE

KEY_RETURN = 176
KEY_HOME = 210
SURR = {
    (0, 0): (645, 323),

    (-1, 1): (640, 278),
    (0, 1): (677, 300),
    (1, 1): (715, 333),
    (1, 0): (700, 366),
    (1, -1): (635, 373),
    (0, -1): (597, 366),
    (-1, -1): (535, 330),
    (-1, 0): (600, 300),

    (-2, 0): (541, 253),
    (0, 2): (743, 263),
    (2, 0): (762, 405),
    (0, -2): (527, 409),
    (-2, -2): (424, 333),
    (-2, 2): (645, 209),
    (2, 2): (863, 333),
    (2, -2): (646, 500),

    (-2, 1): (593, 237),
    (-1, 2): (696, 237),

    (1, 2): (804, 300),
    (2, 1): (816, 366),

    (2, -1): (582, 449),
    (1, -2): (709, 449),

    (-1, -2): (476, 366),
    (-2, -1): (489, 300),
}


def go_to(target_coords: tuple, map_name: str, read_coords: callable):
    """
    Go to target coordinates on current map. Return True if player dies.
    """
    current_coords = read_coords()
    path = djikstra8(
        current_coords, target_coords, get_mu_map_list(map_name))
    try:
        go_through_path(path, read_coords)
    except DeathException as e:
        return True

    while _walk_on_shortest_straight(read_coords(), target_coords):
        pass


def _is_helper_on() -> bool:
    on = 74, 53, 5
    img = window_api.window_grab_image(299, 35, 1, 1)
    img = numpy.asarray(img)
    color = tuple(img[0][0])
    return color[0] == on[0] and color[1] == on[1] and color[2] == on[2]


def _detect_ok() -> bool:
    """
    Detects if OK button is on the screen.
    """
    # 600 235 30 1
    bbox = (600, 235, 30, 1)
    test_indices = (6, 8, 20, 27)
    img = window_api.window_grab_image(*bbox)
    img_1d = [tuple(x) for x in numpy.asarray(img)[0]]
    return all(img_1d[i][c] == 255 for i, c in itertools.product(test_indices, range(3)))


def turn_helper_on(fast=False) -> bool:
    """Starts helper if it is not on."""
    if not _is_helper_on():
        arduino_api.send_ascii(KEY_HOME)
        if not fast:
            time.sleep(0.5)
    if not _is_helper_on():
        if _detect_ok():
            arduino_api.send_ascii(KEY_RETURN)
        if not fast:
            time.sleep(0.5)
        arduino_api.send_ascii(ord("1"))
        mu_window.mouse_to_pos(SURR[(0, 0)])
        arduino_api.hold_right()
        time.sleep(5)
        arduino_api.release_buttons()
        return False
    return True


def turn_helper_off(fast=False) -> None:
    if _is_helper_on():
        arduino_api.send_ascii(KEY_HOME)
        if not fast:
            time.sleep(0.5)


def kill_runaway_units() -> None:
    units = surrounding_units()
    my_coords = read_coords()
    turn_helper_on()
    for u in units:
        if (dist := distance(my_coords, u.coords)) > 5 and dist < 12:
            go_direction(u.coords)
            time.sleep(2)
