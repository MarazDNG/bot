from re import A
from PIL import Image
from typing import List
import os
import numpy


def get_mu_map_list(map_name: str) -> Image:
    """
    Get map image from mu_lib/maps/
    """
    path = os.path.join(os.path.dirname(__file__), f"maps/img_{map_name}.png")
    img = numpy.array(Image.open(path))
    WHITE_COLOR = (255, 255, 255)
    m = [[(tuple(x) == WHITE_COLOR) for x in i] for i in img]
    return numpy.array(m).T
