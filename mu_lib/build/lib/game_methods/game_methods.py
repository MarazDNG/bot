#
# Game interface.
#


from mu_window import mu_window
from mu_image_processing.info_extract import extract_lvl, extract_coords
from .djikstra import djikstra4, djikstra8
from mu_window import mu_window

import math
from datetime import datetime
from datetime import timedelta
import time
import numpy


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


def attack() -> None:
    hold_left()
    time.sleep(2)
    release_buttons()


def _check_if_stucked(coords: tuple) -> None:
    """ Detect stucked character."""
    global _cached_pos
    _cached_pos = _cached_pos or coords
    global _cache_time
    _cache_time = _cache_time or datetime.now()

    time_now = datetime.now()
    diff = time_now - _cache_time
    if diff > timedelta(seconds=1):
        attack()
    _cached_pos = coords
    _cache_time = time_now


def read_lvl_from_frame() -> int:
    img = mu_window.grab_image_from_window(960, 110, 30, 15)
    return extract_lvl(img)


def read_coords_from_frame() -> tuple:
    img = mu_window.grab_image_from_window(50, 35, 150, 13)
    return extract_coords(img)


def read_lvl() -> int:
    mu_window.press(ord("c"))
    time.sleep(1)
    lvl = read_lvl_from_frame()
    mu_window.press(ord("c"))
    return lvl


def read_coords() -> tuple:
    return read_coords_from_frame()


def _walk_on_shortest_straight(goal: tuple) -> None:
    while True:
        current_coords = read_coords_from_frame()
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
    """ Sometimes fcks up."""
    """ djiksta() works well with threshold 1.5 - 2.0"""
    global _cache_time
    _cache_time = datetime.now()
    global _cached_pos
    _cached_pos = None
    steps_made = 0

    while steps_made < len(path):
        current_coords = read_coords_from_frame()
        _check_if_stucked(current_coords)
        following_coords = path[steps_made]

        try:
            tuple_zip = tuple(zip(current_coords, following_coords))
            if numpy.linalg.norm((v1 - v2 for v1, v2 in tuple_zip)) < 2:
                steps_made += 1
                continue

            diff = tuple(numpy.subtract(
                following_coords, current_coords))

            window_pixel_position = SURR[diff]
            mu_window.click_on_pixel(window_pixel_position)

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
