from collections import namedtuple

Loc = namedtuple('Loc', ['map', 'warp'])

"""
    : param [0]: map
    : param [1]: warp
    : paramm [2]: level limit
"""
STADIUM = ("stadium", "stadium", 50)
STADIUM_CITY = ("stadium", None, 100)
LORENCIA = ("lorencia", "lorencia", None)
ELBELAND2 = ("elbeland", "elbeland2", 20)
PEACE_SWAMP = ("peaceswamp", "peaceswamp", 300)
ATLANS2 = ("atlans", "atlans2", 80)
