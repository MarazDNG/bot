
from game_methods import game_methods
from .scripts import activate_window
from mu_bot import game_menu
from game_methods.reset import reset
from game_methods.spots import *

activate_window()
# 295, 30, 10, 10 - whole helper sign
# 299, 35, 1, 1 - helper pixel
# helper pixel - (74, 53, 5) - ON
# helper pixel - (239, 174, 36) - OFF

spot_sequence = [
    BUDGE_DRAGONS,
    WEREWOLVES,
    # GREAT_BAHAMUTS,
    BLUE_GOLEMS,
    SAPI_DUOS,
]

warp_name = "lorencia"
game_methods.warp_to(warp_name)

spot_sequence_counter = 0


def kill(spot: Spot, warp_name: str) -> str:
    if warp_name != spot.warp:
        game_methods.warp_to(spot.warp)
    if not game_methods.is_helper_on():
        game_methods.go_to(spot.coords, spot.map)
        game_methods.start_helper()
    return spot.warp


while True:
    lvl = game_methods.read_lvl()

    if warp_name != spot_sequence[-1].warp and \
            lvl > spot_sequence[spot_sequence_counter].level_limit:
        spot_sequence_counter += 1
        warp_name = kill(spot_sequence[spot_sequence_counter], warp_name)

    if lvl == 400:
        game_menu.server_selection()
        reset()
        activate_window()
        game_menu.game_login()
