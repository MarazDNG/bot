from mu_window import mu_window
from mu_image_processing.info_extract import extract_coords

import re


def _read_coords_from_frame() -> tuple:
    img = mu_window.grab_image_from_window(50, 35, 150, 13)
    return extract_coords(img)


def read_lvl() -> int:
    win_title = mu_window.get_window_title()
    lvl_str = re.search("Level: \d+", win_title)[0]
    return int(lvl_str.split()[1])


def read_coords() -> tuple:
    return _read_coords_from_frame()
