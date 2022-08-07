from mu_window import mu_window
from . import memory

import re


def read_coords() -> tuple:
    return memory.my_coords()


def read_lvl() -> int:
    win_title = mu_window.get_window_title()
    lvl_str = re.search("Level: \d+", win_title)[0]
    return int(lvl_str.split()[1])
