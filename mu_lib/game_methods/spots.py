from collections import namedtuple
from warps_mapping import *

Spot = namedtuple('Spot', ['coords', 'map', 'warp', 'level_limit'])

BUDGE_DRAGONS = Spot((151, 60), *LORENCIA)
WEREWOLVES = Spot((57, 69), *ELBELAND2)
GREAT_BAHAMUTS = Spot((237, 50), *ATLANS2)
BLUE_GOLEMS = Spot((221, 174), *STADIUM_CITY)
SAPI_DUOS = Spot((173, 217), *PEACE_SWAMP)
