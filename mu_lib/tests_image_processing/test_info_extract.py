from unittest import TestCase
from unittest.mock import patch
import cv2

from mu_image_processing.info_extract import extract_coords
from mu_image_processing.info_extract import extract_lvl


class TestInfoExtract(TestCase):

    def test_extract_lvl(self):
        path = "test_coords_images/coords_72_179.png"
        img = cv2.imread(path)
        coords = extract_coords(img)
        print(coords)
