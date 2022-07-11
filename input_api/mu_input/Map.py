from PIL import Image
from typing import List

class Map:
    def __init__(self, mapa: List[List[bool]] = None):
        if mapa is None:
            mapa = []
        self.mapa = mapa

    def load_img(self, img: Image) -> None:
        WHITE_COLOR = (255, 255, 255)
        self.mapa = [[(tuple(x) == WHITE_COLOR) for x in i] for i in img]

