from .reading import read_coords
from conf.conf import SURR
from mu_window import mu_window

import time
import math


def _walk_on_shortest_straight(goal: tuple) -> None:
    while True:
        current_coords = read_coords()
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
