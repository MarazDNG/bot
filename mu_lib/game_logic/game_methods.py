#
# Game interface.
#


import contextlib
from mu_window import mu_window
from conf.conf import SURR, KEY_HOME, KEY_RETURN, STR, AGI, VIT, ENE

from .djikstra import djikstra8
from .map import get_mu_map_list
from .reading import read_coords
from .walking_vector import go_through_path
from .walking_clicking import get_to2
from .walking_straight import _walk_on_shortest_straight

from datetime import datetime, timedelta
import math
import itertools
import time
import numpy


def prebihani(path: list, time_length: int = None) -> None:
    """ Run to the end of path and back."""
    start = datetime.now()
    time.sleep(3)
    get_to2(path)
    time.sleep(3)
    path.reverse()
    get_to2(path)
    path.reverse()
    if time_length:
        end = datetime.now()
        rem = end - start
        with contextlib.suppress(ValueError):
            time.sleep(time_length - rem.total_seconds() + 2)


def go_to(target_coords: tuple, map_name: str):
    current_coords = read_coords()
    path = djikstra8(
        current_coords, target_coords, get_mu_map_list(map_name))
    go_through_path(path)
    _walk_on_shortest_straight(target_coords)


def go_to_spot(spot) -> None:
    if callable(spot.warp):
        spot.warp()
    else:
        warp_to(spot.warp)
    go_to(spot.coords, spot.map)


def _is_helper_on() -> bool:
    on = (74, 53, 5)
    img = mu_window.grab_image_from_window(299, 35, 1, 1)
    img = numpy.asarray(img)
    color = tuple(img[0][0])
    res = color[0] == on[0] and color[1] == on[1] and color[2] == on[2]
    if res:
        print("Helper is on!")
    else:
        print("Helper is off!")
    return res


def _detect_ok() -> bool:
    """
        Detects if OK button is on the screen.
    """
    # 600 235 30 1
    bbox = (600, 235, 30, 1)
    test_indices = (6, 8, 20, 27)
    img = mu_window.grab_image_from_window(*bbox)
    img_1d = [tuple(x) for x in numpy.asarray(img)[0]]
    return all(img_1d[i][c] == 255 for i, c in itertools.product(test_indices, range(3)))


def start_helper() -> bool:
    if not _is_helper_on():
        mu_window.press(KEY_HOME)
    time.sleep(0.5)
    if not _is_helper_on():
        if _detect_ok():
            mu_window.press(KEY_RETURN)
        time.sleep(0.5)
        mu_window.press(ord("1"))
        mu_window.mouse_to_pos(SURR[(0, 0)])
        mu_window.mouse_event("hold_right")
        time.sleep(5)
        mu_window.mouse_event("release_buttons")
        return False
    return True


def _to_chat(msg: str) -> None:
    mu_window.press(KEY_RETURN)
    time.sleep(0.5)
    mu_window.write_text(msg)
    time.sleep(0.5)
    mu_window.press(KEY_RETURN)
    time.sleep(0.5)


def warp_to(area: str) -> None:
    _to_chat(f'/warp {area}')
    time.sleep(3)


def distribute_stats() -> None:
    _to_chat(f"/addstr {STR}")
    _to_chat(f"/addagi {AGI}")
    _to_chat(f"/addvit {VIT}")
    _to_chat(f"/addene {ENE}")


def distance(a: tuple, b: tuple) -> float:
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def go_through_portal(portal_coords: tuple) -> None:
    current_coords = read_coords()
    diff = (portal_coords[0] - current_coords[0],
            portal_coords[1] - current_coords[1],)
    _walk_on_shortest_straight(portal_coords)
    # mu_window.click_on_pixel(SURR[diff])
    time.sleep(3)
