from .reading import read_coords
from conf.conf import SURR
from mu_window import mu_window

import time
import math
from datetime import datetime, timedelta


_cached_pos = None
_cache_time = None


def _attack() -> None:
    mu_window.mouse_event("hold_right")
    time.sleep(3)
    mu_window.mouse_event("release_buttons")


def _check_if_stucked(coords: tuple, wait_time: int = 2) -> bool:
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
    if diff > timedelta(seconds=wait_time):
        _cached_pos = coords
        _cache_time = time_now
        return True
    return False


def _walk_on_shortest_straight(goal: tuple) -> None:
    while True:
        current_coords = read_coords()
        if _check_if_stucked(current_coords):
            _attack()
        diff = (goal[0] - current_coords[0],
                goal[1] - current_coords[1],)
        if abs(diff[0]) > 10 or abs(diff[1]) > 10:
            break
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
