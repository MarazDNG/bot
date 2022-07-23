from PIL import Image
from typing import List


def get_mu_map_list(map_name: str) -> Image:
    """
    Get map image from mu_lib/maps/
    """
    img = Image.open(f'maps/img_{map_name}.png')
    WHITE_COLOR = (255, 255, 255)
    return [[(tuple(x) == WHITE_COLOR) for x in i] for i in img]
