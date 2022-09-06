from collections import namedtuple
from dataclasses import dataclass

from .warps_mapping import *

# Spot = namedtuple('Spot', ['coords', 'map', 'warp', 'level_limit', 'path'=None])


@dataclass
class Spot:
    coords: tuple
    map: str
    warp: str
    level_limit: int
    coords_for_overrunning: tuple = None
    overrunning_route_time: int = None


BUDGE_DRAGONS = Spot((151, 60), *LORENCIA)
WEREWOLVES = Spot((57, 69), *ELBELAND2)
GREAT_BAHAMUTS = Spot((239, 50), *ATLANS2)
BLUE_GOLEMS = Spot((221, 166), *STADIUM_CITY)
SAPI_DUOS = Spot((173, 217), *PEACE_SWAMP1)
SAPI_TRES_SHADOW = Spot((53, 28), *PEACE_SWAMP3, (53, 10), 12)

n_BUDGE_DRAGONS = {
    "warp": "lorencia",
    "min_lvl": 10,
    "coords": (151, 60),
}

n_WEREWOLVES = {
    "warp": "elbeland2",
    "min_lvl": 20,
    "coords": (57, 69),
}

n_GREAT_BAHAMUTS = {
    "warp": "atlans2",
    "min_lvl": 80,
    "coords": (239, 50),
}

n_BLUE_GOLEMS = {
    "warp": "stadium_city",
    "min_lvl": 100,
    "coords": (221, 166),
}

n_SAPI_DUOS = {
    "warp": "peaceswamp1",
    "min_lvl": 300,
    "coords": (173, 217),
}

n_GRIZZLYS_1 = {
    "warp": "elbeland3",
    "min_lvl": 50,
    "coords": (192, 92),
}

n_GRIZZLYS_2 = {
    "warp": "elbeland3",
    "min_lvl": 50,
    "coords": (184, 75),
}
