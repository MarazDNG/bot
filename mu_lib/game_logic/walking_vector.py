
from math import sqrt, cos, sin, pi
import time
import numpy


def go_next_point(start: tuple, goal: tuple, normalize: bool = True) -> tuple:
    """
    Return pixel offset from character to click on to get to the goal.
    Use:mouse_click(pixel_on_characters_feet + this_offset)
    """
    vector = get_vector(goal, start, normalize)
    vector = transform_vector(vector)
    # vector = vector_rotate(vector, 7/4 * pi)
    vector = perspective_transform(vector)
    return vector[0], vector[1]


def get_vector(target_pos: tuple, current_pos: tuple, normalize: bool = True) -> tuple:
    """Get normalized vector by ingame coordinates.
    """
    if current_pos == target_pos:
        return (0, 0)
    vector = numpy.array([target_pos[0] - current_pos[0],
                          target_pos[1] - current_pos[1],
                          ])
    # print(vector)
    if normalize:
        vector = vector / numpy.linalg.norm(vector)
    return vector


def transform_vector(vector, k: int = 250):
    """Take MU vector and return offset.
    """
    start = time.time()
    ox = vector[0] * k
    oy = vector[1] * k
    nx = ox * cos(1/4 * pi) + oy * sin(1/4 * pi)
    ny = - oy * sin(1/4 * pi) + ox * cos(1/4 * pi)
    end = time.time()
    # print('transform vector took:', end-start)
    return (nx, ny)


def perspective_transform(vector: tuple):
    # perspective formula
    # ys/n = y/z
    n = 0.5
    alpha = pi / 4
    v = 3

    r0 = vector[0] / numpy.linalg.norm(vector)
    r1 = vector[1] / numpy.linalg.norm(vector)

    z = v - r0 * cos(alpha)
    y = r0 * sin(alpha)

    ys = n * y / z

    coeff0 = r1 == 0 or ys / (n * r0 / v)

    z = v - r1 * cos(alpha)
    y = r1 * sin(alpha)

    ys = n * y / z

    coeff1 = r1 == 0 or ys / (n * r1 / v)

    return (coeff0 * vector[0] / 2, coeff1 * vector[1] / 2)


def vector_rotate(vector: tuple, angle: float):
    """
    Rotate vector by angle.
    """
    x = vector[0]
    y = vector[1]
    return (x * cos(angle) - y * sin(angle), x * sin(angle) + y * cos(angle))


def perspective_transform2(vector: tuple):
    # perspective formula
    # ys/n = y/z
    n = 2
    alpha = pi / 4
    v = 16

    r0 = vector[0]
    r1 = vector[1]

    z = v if r1 == 0 else v + r1 * cos(alpha)

    y = r1 * sin(alpha)
    ys = n * y / z

    x = r0
    xs = n * x / z

    coeff = 620
    return (coeff * xs, coeff * ys)

def coords_to_pixel_offset(start: tuple, goal: tuple):
    """Retun offset from start to goal in pixels.
    """
    vector = get_vector(goal, start, normalize=False)
    # vector = transform_vector(vector)
    vector = vector_rotate(vector, 7/4 * pi)
    vector = perspective_transform2(vector)
    return vector[0], - vector[1]


def distance(a: tuple, b: tuple) -> float:
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


if __name__ == '__main__':

    v = vector_rotate((3, -2), 7/4 * pi)
    v = perspective_transform2(v)
    print(v)
