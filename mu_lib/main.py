from game_logic import game_menu
from game_logic.Player import Player
from game_logic.exceptions import WrongArgumentsException

import logging
import sys
import window_api

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        filename="mu.log",
                        filemode="w",
                        datefmt="%Y/%m/%d %H:%M:%S",)

    if len(sys.argv) != 2:
        raise WrongArgumentsException("Character name is required.")

    player = Player(sys.argv[1])
    game_menu.start_game()
    hwnd = window_api.window_handler_by_regex("^MU$")
    game_menu.game_login(hwnd,
        player.config["account"]["id"], player.config["account"]["pass"])
    window_api.window_activate(player.name)

    while True:
        player.check_death()

        player.distribute_stats()

        player.try_reset()

        player.ensure_on_best_spot()

        player.farm()
