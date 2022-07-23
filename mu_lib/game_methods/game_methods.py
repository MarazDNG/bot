#
# Game interface.
#


from mu_window import mu_window
from mu_image_processing.info_extract import extract_lvl, extract_coords
# from i_mouse import game_mouse_to_pixel
from .djikstra import djikstra4, djikstra8
# from exceptions import StuckedException
from mu_window import mu_window
from arduino_api import arduino_api

import math
from datetime import datetime
from datetime import timedelta
import time
import numpy
from numpy import cos, sin, pi
from math import sqrt


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
    # TO CALIBRATE
    img = mu_window.grab_image_from_window(960, 110, 30, 15)
    return extract_lvl(img)


def read_coords_from_frame() -> tuple:
    img = mu_window.grab_image_from_window(50, 35, 150, 13)
    return extract_coords(img)


def read_lvl() -> tuple:
    arduino_api.send_ascii(ord("c"))
    time.sleep(0.1)
    coords = read_lvl_from_frame()
    arduino_api.send_ascii(ord("c"))
    return coords


def get_to(pos, area):
    global _cache_time
    global _cached_pos
    """ Sometimes fcks up."""
    """ djiksta() works well with threshold 1.5 - 2.0"""
    my_coords = read_coords_from_frame()
    _check_if_stucked(my_coords)
    print('coords:', my_coords)
    path = djikstra8(my_coords, pos, area)
    print("Path acquired..")
    ct = 0
    while True:
        my_coords = read_coords_from_frame()
        _check_if_stucked(my_coords)

        try:
            n_pos = path[ct]

            if _distance(n_pos, my_coords) < 2:
                ct += 1
                n_pos = path[ct]
            diff = (n_pos[0] - my_coords[0],
                    n_pos[1] - my_coords[1],
                    )
            px_pos = SURR[diff]

        except Exception:
            print("SADGE!")
            continue
        if (ct + 1) >= len(path):
            break
        game_mouse_to_pixel(px_pos)
        # card = diff_to_card(diff)
        # mouse_to_card_dir(card)
        time.sleep(0.05)
        click()


def get_to2(path: list) -> None:
    """ Sometimes fcks up."""
    """ djiksta() works well with threshold 1.5 - 2.0"""
    global _cache_time
    global _cached_pos
    steps_made = 0

    while steps_made < len(path):
        current_coords = read_coords_from_frame()
        # _check_if_stucked(current_coords)

        following_coords = path[steps_made]
        try:

            if _distance(following_coords, current_coords) < 2:
                steps_made += 1
                continue

            diff = tuple(numpy.subtract(
                following_coords, current_coords))
            # print(f"{diff}:{SURR[diff]}")
            window_pixel_position = SURR[diff]

            mu_window.mouse_to_pos(window_pixel_position)
            time.sleep(0.05)
            mu_window.mouse_event("click")
            time.sleep(0.05)
        except IndexError:
            print("Final destination!")
            break
        except KeyError:
            print("You got lost!")
            _walk_on_shortest_straight(path[steps_made])
            print("Back on path!")


def walk_to(pos, area):
    """ Works nicely."""
    my_coords = read_coords()
    path = djikstra4(my_coords, pos, area)

    ct = 0
    origin = SURR[(0, 0)]
    # passed = set()
    while True:
        my_coords = read_coords()
        # passed.add(my_coords)
        if _distance(path[ct], my_coords) < 2:
            ct += 1
        try:
            vector = _get_vector(path[ct+2], my_coords)
        except Exception:
            print("SADGE!")
            continue
        if (ct + 2) >= len(path):
            break
        vector = _transform_vector(vector)
        mouse_pos = (origin[0] + vector[0],
                     origin[1] + vector[1],
                     )
        game_mouse_to_pixel(mouse_pos)
        time.sleep(0.05)
        click()


def _get_vector(target_pos, current_pos):
    """Get normalized vector by ingame coordinates.
    """
    if current_pos == target_pos:
        return (0, 0)
    vector = numpy.array([target_pos[0] - current_pos[0],
                          target_pos[1] - current_pos[1],
                          ])
    # print(vector)
    vector = vector / numpy.linalg.norm(vector)
    return vector


def _transform_vector(vector):
    """Transform and scale vector by screen coordinates.
    """
    start = time.time()
    k = 100
    ox = vector[0] * k
    oy = vector[1] * k
    nx = ox * cos(1/4 * pi) + oy * sin(1/4 * pi)
    ny = - oy * sin(1/4 * pi) + ox * cos(1/4 * pi)
    end = time.time()
    # print('transform vector took:', end-start)
    return (nx, ny)


def _distance(a, b):
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def attack() -> None:
    hold_left()
    time.sleep(2)
    release_buttons()


def prebihani(path: list) -> None:
    """ Run to the end of path and back."""
    # arduino_api.send_ascii(177)
    time.sleep(3)
    # arduino_api.send_ascii(177)

    get_to2(path)

    # arduino_api.send_ascii(177)
    time.sleep(3.5)
    # arduino_api.send_ascii(177)

    path.reverse()
    get_to2(path)
    path.reverse()


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
