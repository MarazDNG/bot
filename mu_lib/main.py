
import contextlib
from game_logic import game_methods
from game_logic import game_menu
from game_logic import reading
from game_logic.reset import reset
from conf.conf import SPOT_SEQUENCE
from mu_window.mu_window import activate_window

import time
from game_logic import map
# 295, 30, 10, 10 - whole helper sign
# 299, 35, 1, 1 - helper pixel
# helper pixel - (74, 53, 5) - ON
# helper pixel - (239, 174, 36) - OFF


if __name__ == "__main__":
    activate_window()
    # warp_name = "unset"
    # game_methods.warp_to(warp_name)
    spot_sequence_counter = 0
    f_go_to_spot = True

    while True:
        lvl = reading.read_lvl()

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

            # [print(i) for i in SPOT_SEQUENCE[spot_sequence_counter + 1]]
            if lvl >= SPOT_SEQUENCE[spot_sequence_counter + 1].level_limit:
                spot_sequence_counter += 1
                f_go_to_spot = True
                continue

        if f_go_to_spot:
            f_go_to_spot = False
            game_methods.go_to_spot(SPOT_SEQUENCE[spot_sequence_counter])

        game_methods.start_helper()

        if SPOT_SEQUENCE[spot_sequence_counter].coords_for_overrunning is not None:
            path = game_methods.djikstra8(
                SPOT_SEQUENCE[spot_sequence_counter].coords,
                SPOT_SEQUENCE[spot_sequence_counter].coords_for_overrunning,
                map.get_mu_map_list(SPOT_SEQUENCE[spot_sequence_counter].map))
            game_methods.prebihani(
                path, SPOT_SEQUENCE[spot_sequence_counter].overrunning_route_time)
        else:
            time.sleep(10)
