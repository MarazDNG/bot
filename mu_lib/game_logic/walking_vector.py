from .meth import _if_stucked
from . import ORIGIN
from .exceptions import DeathException

from math import sqrt, cos, sin, pi
import time
import numpy


def go_direction(target_coords: tuple) -> None:
    mouse_to_pos(ORIGIN)
    time.sleep(0.1)
    mouse_event("hold_left")

    while distance(target_coords, my_coords := read_coords()) > 2:
        print("coords:", my_coords, "target:", target_coords)
        if _if_stucked(my_coords):
            vector = get_vector(target_coords, my_coords)
            vector = transform_vector(vector, k=250)
            mouse_pos = ORIGIN[0] + vector[0], ORIGIN[1] + vector[1]
            mouse_to_pos(mouse_pos)
            time.sleep(0.5)
            continue

        vector = get_vector(target_coords, my_coords)
        vector = transform_vector(vector)
        mouse_pos = ORIGIN[0] + vector[0], ORIGIN[1] + vector[1]
        mouse_to_pos(mouse_pos)
        time.sleep(0.02)

    mouse_event("release_buttons")
    print("Finish!")


def go_next_point(start: tuple, goal: tuple) -> tuple:
    """
    Return pixel offset from character to click on to get to the goal.
    Use:mouse_click(pixel_on_characters_feet + this_offset)
    """
    vector = get_vector(goal, start)
    vector = transform_vector(vector)
    return perspective_transform(vector)


def get_vector(target_pos: tuple, current_pos: tuple):
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


def transform_vector(vector, k: int = 200):
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


def perspective_transform(vector: tuple):
    # perspective formula
    # ys/n = y/z
    n = 0.5
    alpha = pi / 4
    v = 3

    r = vector[1] / numpy.linalg.norm(vector)

    z = v - r * cos(alpha)
    y = r * sin(alpha)

    ys = n * y / z

    coeff = ys / (n * r / v)
    return (vector[0], coeff * vector[1])


def distance(a: tuple, b: tuple) -> float:
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
