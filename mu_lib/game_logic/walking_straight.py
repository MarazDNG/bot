from .reading import read_coords
from .meth import _if_stucked
from conf.conf import SURR
from mu_window import mu_window
from .decorators import d_logger

import time
import math
import logging


def _attack() -> None:
    mu_window.mouse_event("hold_right")
    time.sleep(3)
    mu_window.mouse_event("release_buttons")


@d_logger
def _walk_on_shortest_straight(current_coords: tuple, goal: tuple) -> bool:
    logging.debug(f"current_coords: {current_coords}")
    _if_stucked(current_coords, recovery=_attack)
    diff = (goal[0] - current_coords[0],
            goal[1] - current_coords[1],)
    if abs(diff[0]) > 10 or abs(diff[1]) > 10:
        return False
    if diff == (0, 0):
        return False
    dx = math.copysign(diff[0] == 1 or 2, diff[0]) if diff[0] else 0
    dy = math.copysign(diff[0] == 1 or 2, diff[1]) if diff[1] else 0

    ddiff = (dx, dy)
    mu_window.mouse_to_pos(SURR[ddiff])
    time.sleep(0.05)
    mu_window.mouse_event("click")
    time.sleep(0.05)
    return True
