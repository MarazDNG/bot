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
