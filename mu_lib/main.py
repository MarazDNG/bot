from mu_window.mu_window import activate_window
from game_logic.Player import Player
from game_logic.exceptions import WrongArgumentsException

import logging
import sys


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        filename="mu.log",
                        filemode="w",
                        datefmt="%Y/%m/%d %H:%M:%S",)

    if len(sys.argv) != 2:
        raise WrongArgumentsException("Character name is required.")

    player = Player(sys.argv[1])
    activate_window(player.name)

    while True:
        player.check_death()

        player.distribute_stats()

        player.try_reset()

        player.ensure_on_best_spot()

        player.farm()
