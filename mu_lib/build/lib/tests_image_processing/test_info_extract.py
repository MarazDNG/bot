from unittest import TestCase
from unittest.mock import patch
import cv2
import os

from mu_image_processing.info_extract import extract_coords
from mu_image_processing.info_extract import extract_lvl

# DONE


def file_name_to_coords(file_name: str) -> tuple:
    """ Return coordinates in given image.
        Return 0 if coordinates couldnt be found.
    """
    x, y = file_name.split("_")
    x = int(x)
    y = int(y[:-4])
    return (x, y)


class TestInfoExtract(TestCase):

    def test_extract_coords(self):
        path = os.path.dirname(os.path.abspath(
            __file__)) + "/test_coords_images/"
        files = os.scandir(path)
        for file in files:
            if file.name.endswith(".png"):
                img = cv2.imread(file.path, cv2.IMREAD_UNCHANGED)
                extracted_lvl = extract_coords(img)
                expected_lvl = file_name_to_coords(file.name)
                assert extracted_lvl == expected_lvl

    def test_extract_lvl(self):
        path = os.path.dirname(os.path.abspath(
            __file__)) + "/test_lvl_images/"
        files = os.scandir(path)
        for file in files:
            if file.name.endswith(".png"):
                img = cv2.imread(file.path, cv2.IMREAD_UNCHANGED)
                extracted_lvl = extract_lvl(img)
                print(file.name)
                expected_lvl = int(file.name[:-4])
                assert extracted_lvl == expected_lvl
