import re
import requests
from datetime import datetime, timedelta
import math


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


if __name__ == '__main__':
    print(get_online_players())
