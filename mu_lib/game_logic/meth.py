import re
import requests
from datetime import datetime, timedelta
import math
import numpy
import itertools
import time

import window_api
import arduino_api

from . import KEY_HOME, KEY_RETURN


def distance(a: tuple, b: tuple) -> float:
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def _if_stucked(coords: tuple, recovery: callable = None, wait_time: int = 2) -> bool:
    """ Detect stucked character."""
    _if_stucked.cached_pos = getattr(_if_stucked, "cached_pos", coords)
    _if_stucked.cache_time = getattr(_if_stucked, "cache_time", datetime.now())

    time_now = datetime.now()
    if distance(_if_stucked.cached_pos, coords) > 1:
        _if_stucked.cached_pos = coords
        _if_stucked.cache_time = time_now
        return

    diff = time_now - _if_stucked.cache_time
    if diff > timedelta(seconds=wait_time):
        if recovery:
            recovery()
        _if_stucked.cached_pos = coords
        _if_stucked.cache_time = time_now
        return True
    return False


def get_online_players():
    r = requests.get("https://eternmu.cz/rankings/online/")
    return re.findall(
        r"https://eternmu.cz/profile/player/req/(.{1,10})/", r.text)


def _is_helper_on(hwnd: int) -> bool:
    on = 74, 53, 5
    img = window_api.window_grab_image(hwnd, 299, 35, 1, 1)
    img = numpy.asarray(img)
    color = tuple(img[0][0])
    return color[0] == on[0] and color[1] == on[1] and color[2] == on[2]


def _detect_ok(hwnd: int) -> bool:
    """
    Detects if OK button is on the screen.
    """
    # 600 235 30 1
    bbox = (600, 235, 30, 1)
    test_indices = (6, 8, 20, 27)
    img = window_api.window_grab_image(hwnd, *bbox)
    img_1d = [tuple(x) for x in numpy.asarray(img)[0]]
    return all(img_1d[i][c] == 255 for i, c in itertools.product(test_indices, range(3)))


def turn_helper_on(hwnd: int, fast=False) -> bool:
    """Starts helper if it is not on."""
    if not _is_helper_on(hwnd):
        arduino_api.send_ascii(KEY_HOME)
        if not fast:
            time.sleep(0.5)
    if not _is_helper_on(hwnd):
        if _detect_ok(hwnd):
            arduino_api.send_ascii(KEY_RETURN)
        if not fast:
            time.sleep(0.5)
        arduino_api.send_ascii(ord("1"))
        arduino_api.hold_right()
        time.sleep(5)
        arduino_api.release_buttons()
        return False
    return True


if __name__ == '__main__':
    print(get_online_players())
