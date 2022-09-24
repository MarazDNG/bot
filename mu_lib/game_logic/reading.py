from mu_window import mu_window
from . import memory

import re


def read_coords(window_id: int) -> tuple:
    return memory.my_coords(window_id.int)


def read_reset() -> int:
    win_title = mu_window.get_window_title()
    lvl_str = re.search("Reset: \d+", win_title)[0]
    return int(lvl_str.split()[1])


def read_lvl() -> int:
    win_title = mu_window.get_window_title()
    lvl_str = re.search("Level: \d+", win_title)[0]
    return int(lvl_str.split()[1])


def surrounding_units(window_id: int) -> list:
    return memory.get_surrounding_units(window_id)
