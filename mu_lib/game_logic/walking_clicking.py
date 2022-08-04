from .reading import read_coords
from mu_window import mu_window
from conf.conf import SURR

from datetime import datetime, timedelta
import time
import math
import numpy


_cached_pos = None
_cache_time = None


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


def clicker(q: list) -> None:
    while pos := q.get(timeout=10):
        mu_window.click_on_pixel(pos, delay=False)
    print("END!")


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
