from PIL import Image
import cv2
import os
import numpy

from . import WHITE_COLOR
from conf.spots import *


def _is_white(color: numpy.iterable) -> bool:
    """
    Check if color is white
    """
    return (
        color[0] == WHITE_COLOR[0]
        and color[1] == WHITE_COLOR[1]
        and color[2] == WHITE_COLOR[2]
    )


def get_mu_map_list(map_name: str) -> Image:
    """
    Get map image from mu_lib/maps/
    """
    path = os.path.join(os.path.dirname(__file__), f"maps/img_{map_name}.png")
    img = numpy.array(Image.open(path))
    m = [[_is_white(x) for x in i] for i in img]
    return numpy.array(m).T


def check_spot_accessibility():
    l = globals()

    def warp_to_map_name(warp: str):
        return "".join(i for i in warp if i.isalpha())

    map_coords_pairs = [
        (warp_to_map_name(l[spot]["map"]), l[spot]["coords"])
        for spot in l
        if spot.startswith("n_")
    ]
    [
        print(map_name, coords)
        for map_name, coords in map_coords_pairs
        if not get_mu_map_list(map_name)[coords[0]][coords[1]]
    ]


class Warp:
    def __init__(self, lvl, name, coords):
        self.lvl: int = lvl
        self.name: str = name
        self.coords: tuple = coords

    @property
    def map(self):
        return "".join(i for i in self.name if i.isalpha())