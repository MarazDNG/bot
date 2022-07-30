
import contextlib
from game_logic import game_methods
from game_logic import game_menu
from game_logic.reset import reset
from game_logic.spots import *
import pygetwindow as gw

# 295, 30, 10, 10 - whole helper sign
# 299, 35, 1, 1 - helper pixel
# helper pixel - (74, 53, 5) - ON
# helper pixel - (239, 174, 36) - OFF


def go_to_spot(spot: Spot) -> None:
    if callable(spot.warp):
        spot.warp()
    else:
        game_methods.warp_to(spot.warp)
    game_methods.go_to(spot.coords, spot.map)


def activate_window():
    win = gw.getWindowsWithTitle("Player")[0]
    win.activate()
    time.sleep(2)


spot_sequence = [
    BUDGE_DRAGONS,
    WEREWOLVES,
    GREAT_BAHAMUTS,
    # BLUE_GOLEMS,
    SAPI_DUOS,
]

if __name__ == "__main__":
    activate_window()
    # warp_name = "unset"
    # game_methods.warp_to(warp_name)
    spot_sequence_counter = 0
    f_go_to_spot = True

    while True:
        lvl = game_methods.read_lvl()

        if lvl == 1:
            game_methods.distribute_stats()

        if lvl == 400:
            spot_sequence_counter = 0
            f_go_to_spot = True

            game_menu.server_selection()
            reset()
            activate_window()
            game_menu.game_login()
            continue

        with contextlib.suppress(IndexError):
            if lvl >= spot_sequence[spot_sequence_counter + 1].level_limit:
                spot_sequence_counter += 1
                f_go_to_spot = True
                continue
        if f_go_to_spot:
            f_go_to_spot = False
            go_to_spot(spot_sequence[spot_sequence_counter])

        if game_methods.start_helper():
            time.sleep(10)
