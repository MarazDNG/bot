from .reading import read_coords
from .meth import _if_stucked
from mu_window.mu_window import mouse_to_pos, mouse_event
from conf.conf import SURR

from math import sqrt, cos, sin, pi
import time
import numpy


def go_direction(target_coords: tuple) -> None:
    origin = SURR[0, 0]

    mouse_to_pos(origin)
    time.sleep(0.1)
    mouse_event("hold_left")

    while distance(target_coords, my_coords := read_coords()) > 2:
        print("coords:", my_coords, "target:", target_coords)
        if _if_stucked(my_coords):
            vector = get_vector(target_coords, my_coords)
            vector = transform_vector(vector, k=250)
            mouse_pos = origin[0] + vector[0], origin[1] + vector[1]
            mouse_to_pos(mouse_pos)
            time.sleep(0.5)
            continue

        vector = get_vector(target_coords, my_coords)
        vector = transform_vector(vector)
        mouse_pos = origin[0] + vector[0], origin[1] + vector[1]
        mouse_to_pos(mouse_pos)
        time.sleep(0.02)

    mouse_event("release_buttons")
    print("Finish!")


def go_through_path(path: list) -> None:
    """ Works nicely."""
    ct = 0
    origin = SURR[0, 0]
    path_len = len(path)
    ahead = 5
    mouse_to_pos(origin)
    mouse_event("hold_left")
    while ct < path_len - 1:
        my_coords = read_coords()

        # next square in path
        try:
            ahead_coords = path[ct + ahead]
        except IndexError:
            ahead_coords = path[-1]
        if distance(ahead_coords, my_coords) < ahead:
            ct += 1

        # stuck protection
        if _if_stucked(my_coords):
            vector = get_vector(ahead_coords, my_coords)
            vector = transform_vector(vector, k=250)
            mouse_pos = origin[0] + vector[0], origin[1] + vector[1]
            mouse_to_pos(mouse_pos)
            time.sleep(0.5)
            continue

        # standard movement
        vector = get_vector(ahead_coords, my_coords)
        vector = transform_vector(vector)
        mouse_pos = origin[0] + vector[0], origin[1] + vector[1]
        mouse_to_pos(mouse_pos)
        time.sleep(0.02)

    mouse_event("release_buttons")
    print("Finish!")


def get_vector(target_pos, current_pos):
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


def transform_vector(vector, k: int = 120):
    """Transform and scale vector by screen coordinates.
    """
    start = time.time()
    ox = vector[0] * k
    oy = vector[1] * k
    nx = ox * cos(1/4 * pi) + oy * sin(1/4 * pi)
    ny = - oy * sin(1/4 * pi) + ox * cos(1/4 * pi)
    end = time.time()
    # print('transform vector took:', end-start)
    return (nx, ny)


def distance(a, b):
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
