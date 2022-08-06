
from game_logic import game_methods
from game_logic import game_menu
from game_logic import reading
from game_logic import map
from game_logic.reset import reset
from conf.conf import SPOT_SEQUENCE
from mu_window.mu_window import activate_window

import time
import contextlib


if __name__ == "__main__":
    activate_window()
    spot_sequence_counter = 0
    f_go_to_spot = True

    while True:
        lvl = reading.read_lvl()

        if lvl == 1:
            game_methods.distribute_stats()

        # level reset
        if lvl == 400:
            spot_sequence_counter = 0
            f_go_to_spot = True
            game_menu.server_selection()
            reset()
            activate_window()
            game_menu.game_login()
            time.sleep(2)
            continue

        # check for better spot
        with contextlib.suppress(IndexError):
            if lvl >= SPOT_SEQUENCE[spot_sequence_counter + 1].level_limit:
                spot_sequence_counter += 1
                f_go_to_spot = True
                continue

        # go to spot
        if f_go_to_spot:
            f_go_to_spot = False
            game_methods.go_to_spot(SPOT_SEQUENCE[spot_sequence_counter])

        game_methods.start_helper()
        # if possible, do overrunning
        if SPOT_SEQUENCE[spot_sequence_counter].coords_for_overrunning is not None:
            path = game_methods.djikstra8(
                SPOT_SEQUENCE[spot_sequence_counter].coords,
                SPOT_SEQUENCE[spot_sequence_counter].coords_for_overrunning,
                map.get_mu_map_list(SPOT_SEQUENCE[spot_sequence_counter].map))
            game_methods.prebihani(
                path, SPOT_SEQUENCE[spot_sequence_counter].overrunning_route_time)
        else:
            time.sleep(10)
