from conf.conf import SURR
from mu_window import mu_window

from .reading import read_coords
from .walking_straight import _walk_on_shortest_straight, _check_if_stucked

import numpy


def clicker(q: list) -> None:
    while pos := q.get(timeout=10):
        mu_window.click_on_pixel(pos, delay=False)
    print("END!")


def get_to2(path: list) -> None:
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
