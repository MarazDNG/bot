#
# Game interface.
#


from mu_image_processing.info_extract import extract_lvl, extract_coords
from mu_window import mu_window
from mu_window import mu_window
from arduino_api import arduino_api
from .keys import *
from .djikstra import djikstra8
from .map import get_mu_map_list

import math
from datetime import datetime
from datetime import timedelta
import time
import numpy
import re

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

_cached_pos = None
_cache_time = None


def read_lvl_from_frame() -> int:
    img = mu_window.grab_image_from_window(960, 110, 30, 15)
    return extract_lvl(img)


def read_coords_from_frame() -> tuple:
    img = mu_window.grab_image_from_window(50, 35, 150, 13)
    return extract_coords(img)


def read_lvl2() -> int:
    mu_window.press(ord("c"))
    time.sleep(1)
    lvl = read_lvl_from_frame()
    mu_window.press(ord("c"))
    return lvl


def read_lvl() -> int:
    win_title = mu_window.get_window_title()
    lvl_str = re.search("Level: \d+", win_title)[0]
    return int(lvl_str.split()[1])


def read_coords() -> tuple:
    return read_coords_from_frame()


def _attack() -> None:
    mu_window.mouse_event("hold_right")
    time.sleep(3)
    mu_window.mouse_event("release_buttons")


def _check_if_stucked(coords: tuple) -> None:
    """ Detect stucked character."""
    global _cached_pos
    _cached_pos = _cached_pos or coords
    global _cache_time
    _cache_time = _cache_time or datetime.now()
    time_now = datetime.now()
    # print(
    #     f"cached: {_cached_pos}, coords_now: {coords}, cache_time: {_cache_time}, time_now: {time_now}")
    if _cached_pos != coords:
        _cached_pos = coords
        _cache_time = time_now
        return

    diff = time_now - _cache_time
    if diff > timedelta(seconds=2):
        _attack()
        _cached_pos = coords
        _cache_time = time_now


def _walk_on_shortest_straight(goal: tuple) -> None:
    while True:
        current_coords = read_coords()
        diff = (goal[0] - current_coords[0],
                goal[1] - current_coords[1],)
        if diff == (0, 0):
            break
        dx = 0
        dy = 0
        if diff[0]:
            dx = math.copysign(1, diff[0])
        if diff[1]:
            dy = math.copysign(1, diff[1])

        ddiff = (dx, dy)
        mu_window.mouse_to_pos(SURR[ddiff])
        time.sleep(0.05)
        mu_window.mouse_event("click")
        time.sleep(0.05)


def get_to2(path: list) -> None:
    global _cache_time
    _cache_time = datetime.now()
    global _cached_pos
    _cached_pos = read_coords()
    steps_made = 0

    while steps_made < len(path):
        current_coords = read_coords()
        _check_if_stucked(current_coords)
        following_coords = path[steps_made]

        try:
            tuple_zip = tuple(zip(current_coords, following_coords))
            if numpy.linalg.norm(tuple(v1 - v2 for v1, v2 in tuple_zip)) < 2:
                steps_made += 1
                continue

            diff = tuple(numpy.subtract(
                following_coords, current_coords))

            window_pixel_position = SURR[diff]
            mu_window.click_on_pixel(window_pixel_position, delay=False)

        except IndexError:
            print("Final destination!")
            break

        except KeyError:
            print("You got lost!")
            _walk_on_shortest_straight(path[steps_made])
            print("Back on path!")


def prebihani(path: list) -> None:
    """ Run to the end of path and back."""
    time.sleep(3)
    get_to2(path)

    time.sleep(3.5)
    path.reverse()
    get_to2(path)
    path.reverse()


def warp_to(area: str) -> None:
    arduino_api.send_ascii(KEY_RETURN)
    time.sleep(2)
    arduino_api.send_string(f'/warp {area}')
    time.sleep(2)
    arduino_api.send_ascii(KEY_RETURN)
    time.sleep(3)


def go_to(target_coords: tuple, map_name: str):
    current_coords = read_coords()
    vector = (
        target_coords[0] - current_coords[0],
        target_coords[1] - current_coords[1],
    )
    if abs(vector[0]) <= 2 and abs(vector[1]) <= 2:
        return
    path = djikstra8(
        current_coords, target_coords, get_mu_map_list(map_name))
    get_to2(path)


def is_helper_on() -> bool:
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


def start_helper() -> bool:
    if not is_helper_on():
        arduino_api.send_ascii(KEY_HOME)
    time.sleep(0.5)
    if not is_helper_on():
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
    arduino_api.send_ascii(KEY_RETURN)
    time.sleep(0.5)
    arduino_api.send_string(msg)
    time.sleep(0.5)
    arduino_api.send_ascii(KEY_RETURN)
    time.sleep(0.5)


def distribute_stats() -> None:
    _to_chat("/addstr 2000")
    _to_chat("/addagi 40000")
    _to_chat("/addvit 1000")
    _to_chat("/addene 40000")


def distance(a: tuple, b: tuple) -> float:
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def go_through_portal(portal_coords: tuple) -> None:
    current_coords = read_coords()
    diff = (portal_coords[0] - current_coords[0],
            portal_coords[1] - current_coords[1],)
    mu_window.click_on_pixel(SURR[diff])
    time.sleep(3)
