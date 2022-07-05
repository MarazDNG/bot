#
# Game interface.
#


from datetime import datetime
from datetime import timedelta
from mu_image.info_extract import extract_coords
from mu_image.info_extract import extract_lvl
from mu_image.image_extract import get_image_of
from mu_image.image_extract import grab_coords
from arduino_api import hold_left
from arduino_api import release_buttons
from arduino_api import click
# from i_mouse import game_mouse_to_pixel
from djikstra import djikstra4, djikstra
from exceptions import StuckedException
import time
from numpy import cos, sin, pi
import numpy
from math import sqrt

def game_mouse_to_pixel(*args):
    pass

SURR = {
    (0, 0): (645, 323),

    (-1, 1): (640, 278),
    (0, 1): (677, 300),
    (1, 1): (715, 333),
    (1, 0): (700, 366),
    (1, -1): (635, 373),
    (0, -1): (597, 366),
    (-1, -1): (535, 330),
    (-1, 0): (600, 300),

    (-2, 0): (541, 253),
    (0, 2): (743, 263),
    (2, 0): (762, 405),
    (0, -2): (527, 409),
    (-2, -2): (424, 333),
    (-2, 2): (645, 209),
    (2, 2): (863, 333),
    (2, -2): (646, 500),

    (-2, 1): (593, 237),
    (-1, 2): (696, 237),

    (1, 2): (804, 300),
    (2, 1): (816, 366),

    (2, -1): (582, 449),
    (1, -2): (709, 449),

    (-1, -2): (476, 366),
    (-2, -1): (489, 300),
}

cached_pos = None
cache_time = None


def check_cache(coords: tuple) -> None:
    """ Detect stucked character."""
    global cached_pos
    cached_pos = cached_pos or coords
    global cache_time
    cache_time = cache_time or datetime.now()

    check_time = datetime.now()
    diff = check_time - cache_time
    if diff > timedelta(seconds=1):
        attack()
    cached_pos = coords
    cache_time = check_time


def read_lvl():
    img = get_image_of()
    return extract_lvl(img)


def read_coords() -> tuple:
    img = grab_coords()
    return extract_coords(img)


def get_to(pos, area):
    global cache_time
    global cached_pos
    """ Sometimes fcks up."""
    """ djiksta() works well with threshold 1.5 - 2.0"""
    my_coords = read_coords()
    check_cache(my_coords)
    print('coords:', my_coords)
    path = djikstra(my_coords, pos, area)
    print("Path acquired..")
    ct = 0
    while True:
        my_coords = read_coords()
        check_cache(my_coords)

        try:
            n_pos = path[ct]

            if distance(n_pos, my_coords) < 2:
                ct += 1
                n_pos = path[ct]
            diff = (n_pos[0] - my_coords[0],
                    n_pos[1] - my_coords[1],
                    )
            px_pos = SURR[diff]

        except Exception:
            print("SADGE!")
            continue
        if (ct + 1) >= len(path):
            break
        game_mouse_to_pixel(px_pos)
        # card = diff_to_card(diff)
        # mouse_to_card_dir(card)
        time.sleep(0.05)
        click()


def walk_to(pos, area):
    """ Works nicely."""
    my_coords = read_coords()
    path = djikstra4(my_coords, pos, area)

    ct = 0
    origin = SURR[(0, 0)]
    # passed = set()
    while True:
        my_coords = read_coords()
        # passed.add(my_coords)
        if distance(path[ct], my_coords) < 2:
            ct += 1
        try:
            vector = get_vector(path[ct+2], my_coords)
        except Exception:
            print("SADGE!")
            continue
        if (ct + 2) >= len(path):
            break
        vector = transform_vector(vector)
        mouse_pos = (origin[0] + vector[0],
                     origin[1] + vector[1],
                     )
        game_mouse_to_pixel(mouse_pos)
        time.sleep(0.05)
        click()


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


def transform_vector(vector):
    """Transform and scale vector by screen coordinates.
    """
    start = time.time()
    k = 100
    ox = vector[0] * k
    oy = vector[1] * k
    nx = ox * cos(1/4 * pi) + oy * sin(1/4 * pi)
    ny = - oy * sin(1/4 * pi) + ox * cos(1/4 * pi)
    end = time.time()
    # print('transform vector took:', end-start)
    return (nx, ny)


def distance(a, b):
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def attack() -> None:
    hold_left()
    time.sleep(2)
    release_buttons()
