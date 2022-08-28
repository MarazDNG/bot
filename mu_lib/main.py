
from game_logic import game_methods
from game_logic import game_menu
from game_logic import reading
from game_logic import map
from game_logic.reset import reset
from conf.conf import SPOT_SEQUENCE
from mu_window.mu_window import activate_window
from game_logic.Player import Player

import time
import contextlib
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        filename="mu.log",
                        filemode="w",
                        datefmt="%Y/%m/%d %H:%M:%S",)
    activate_window()
    player = Player()
    spot_sequence_counter = 0
    f_go_to_spot = True

    while True:
        lvl = player.lvl

        player.distribute_stats()

        # level reset
        if player.try_reset():
            spot_sequence_counter = 0
            f_go_to_spot = True
            continue

        player.check_best_spot()

        player.farm()
