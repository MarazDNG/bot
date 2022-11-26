from .map import Warp

MAP_DICT = {
    "kantururuins": (
        Warp(200, "kantururuins1", (20, 218)),
        Warp(220, "kantururuins2", (206, 38)),
        # Warp(300, "kantururuins3", (70, 185)),
    ),
    "lorencia": (Warp(10, "lorencia", (138, 120)),),
    "elbeland": (
        Warp(10, "elbeland", (51, 225)),
        Warp(20, "elbeland2", (99, 56)),
        Warp(50, "elbeland3", (191, 149)),
    ),
    "atlans": (
        # Warp(70, "atlans", (0, 0)),
        Warp(80, "atlans2", (226, 53)),
        # Warp(90, "atlans3", (0, 0)),
    ),
    "devias": (Warp(20, "devias", (215, 50)),),
    "dungeon": (
        Warp(20, "dungeon", (109, 247)),
        Warp(40, "dungeon2", (231, 126)),
        Warp(70, "dungeon3", (3, 84)),
    ),
    "icarus": (Warp(150, "icarus", (15, 13)),),
    "losttower": (
        Warp(60, "losttower3", (86, 166)),
        Warp(90, "losttower6", (53, 53)),
    ),
    "peaceswamp": (
        # Warp(300, "peaceswamp", (0, 0)),
        Warp(300, "peaceswamp1", (190, 190)),
    ),
    "tarkan": (Warp(150, "tarkan", (190, 62)),),
    "aida": (
        Warp(150, "aida", (84, 10)),
        Warp(150, "aida2", (188, 176)),
    ),
}
