from datetime import datetime, timedelta


_cached_pos = None
_cache_time = None


def _if_stucked(coords: tuple, recovery: callable = None, wait_time: int = 2) -> bool:
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
        if recovery:
            recovery()
        _cached_pos = coords
        _cache_time = time_now
        return True
    return False
