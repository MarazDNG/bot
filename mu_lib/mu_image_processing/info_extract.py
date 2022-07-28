#
# Information extraction from an image.
#


import cv2
import numpy
import os

# DONE


COORDS_SET = "patterns/"
LVL_SET = "y_img/y"


def _match_numbers(pattern_set: str, img: numpy.array) -> list:
    """ Return numbers in the image."""
    img = numpy.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    matches = []
    for i in range(10):
        path = f"{os.path.dirname(os.path.abspath(__file__))}/{pattern_set}{i}.png"
        pattern = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        pattern = cv2.cvtColor(pattern, cv2.COLOR_BGRA2GRAY)
        result = cv2.matchTemplate(img, pattern, cv2.TM_CCOEFF_NORMED)
        _, xloc = numpy.where(result > 0.99)
        [matches.append([x, i]) for x in xloc]
    matches = sorted(matches, key=lambda x: x[0])
    return matches


def extract_coords(img: numpy.ndarray) -> tuple:
    """ Return coordinates in given image."""
    matches = _match_numbers(COORDS_SET, img)
    deltas = [matches[i + 1][0] - matches[i][0]
              for i in range(len(matches) - 1)]
    if len(matches) == 0:
        return 0
        raise Exception("Coordinates not found!")
    index = None
    if len(deltas) != 0:
        index = deltas.index(max(deltas))
    x = matches[:index+1]
    y = matches[index+1:]
    x = [i[1] for i in x]
    y = [i[1] for i in y]
    x = "".join(map(str, x))
    y = "".join(map(str, y))
    x = int(x)
    y = int(y)
    return (x, y)


def extract_lvl(img: numpy.ndarray) -> int:
    """ Return lvl in given image.
        Return 0 if lvl couldnt be found.
    """
    matches = _match_numbers(LVL_SET, img)
    matches = [i[1] for i in matches]
    lvl = "".join(map(str, matches))
    try:
        lvl = int(lvl)
        return lvl
    except ValueError:
        return 0
