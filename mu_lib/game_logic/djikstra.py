from .exceptions import TooManyIterationsException

from datetime import date
from itertools import product
import logging


logger = logging.getLogger(__name__)
handler = logging.FileHandler(f"{__name__}.log")
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y/%m/%d %H:%M:%S"
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.propagate = False
logger.setLevel(logging.DEBUG)


def _get_surrounding8(x: int, y: int) -> set:
    p = {i for i in product((0, 1, -1), repeat=2) if i != (0, 0)}
    return {(x + dx, y + dy) for dx, dy in p}


def _get_surrounding4(x: int, y: int) -> set:
    return {(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)}


def djikstra8(start: tuple, goal: tuple, array_map: list) -> list:
    return _djikstra_body(start, goal, array_map, _get_surrounding8)


def djikstra4(start: tuple, goal: tuple, array_map: list) -> list:
    return _djikstra_body(start, goal, array_map, _get_surrounding4)


def _djikstra_body(
    start: tuple, goal: tuple, array_map: list, neighbor_fnc: callable
) -> list:
    logger.info(f"Start: { start}, Goal: {goal}")
    if start == goal:
        return [start]
    sets = [
        {
            start,
        }
    ]
    distance = 0
    while True:
        if distance > 1000:
            raise TooManyIterationsException("Too many iterations")
        new_set = set()
        for item in sets[distance]:
            neighbors = neighbor_fnc(*item)
            neighbors = {
                (x, y)
                for x, y in neighbors
                if x >= 0 and x < len(array_map) and y >= 0 and y < len(array_map[x])
            }
            new_set = new_set.union({(x, y) for x, y in neighbors if array_map[x][y]})
        logger.debug(f"New set: {new_set}")
        if distance > 0:
            new_set.difference_update(sets[distance - 1])
        new_set.difference_update(sets[distance])

        if goal in new_set:
            break

        sets.append(new_set)
        distance += 1

    path = [
        goal,
    ]
    while distance:
        neighbors = neighbor_fnc(*path[-1])
        neighbors = neighbors.intersection(sets[distance])
        if not neighbors:
            print("FCK!")
            break
        path.append(tuple(neighbors)[0])
        if path[-1] == start:
            break
        distance -= 1

    path.append(start)
    path.reverse()
    return path
