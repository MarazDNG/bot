from PIL import Image
import os
import numpy
from . import WHITE_COLOR


def _is_white(color: numpy.iterable) -> bool:
    """
    Check if color is white
    """
    return color[0] == WHITE_COLOR[0] and color[1] == WHITE_COLOR[1] and color[2] == WHITE_COLOR[2]


def get_mu_map_list(map_name: str) -> Image:
    """
    Get map image from mu_lib/maps/
    """
    path = os.path.join(os.path.dirname(__file__), f"maps/img_{map_name}.png")
    img = numpy.array(Image.open(path))
    m = [[_is_white(x) for x in i] for i in img]
    return numpy.array(m).T
