from game_logic import game_menu
from game_logic.Player import Player
from game_logic.exceptions import WrongArgumentsException

import logging
import sys
import window_api
import arduino_api

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        filename="mu.log",
                        filemode="w",
                        datefmt="%Y/%m/%d %H:%M:%S",)

    if len(sys.argv) == 1:
        raise WrongArgumentsException("Character name is required.")

    arduino_api.ard_init(6)

    player_pool = [Player(sys.argv[i]) for i in range(1, len(sys.argv))]

    # try:
    #     window_api.window_handler_by_title(f"Player: {player.name}")
    # except Exception:
    #     game_menu.start_game()
    #     hwnd = window_api.window_handler_by_regex("^MU$")
    #     window_api.window_activate_by_handler(hwnd)
    #     game_menu.game_login(hwnd,
    #                          player.config["account"]["id"], player.config["account"]["pass"], player.config["account"]["select_offset"])

    # window_api.window_activate(f"Player: {player.name}")

    while True:
        for player in player_pool:
            try:
                window_api.window_activate(f"Player: {player.name}")
            except IndexError:
                game_menu.start_game()
                hwnd = window_api.window_handler_by_regex("^MU$")
                window_api.window_activate_by_handler(hwnd)
                game_menu.game_login(hwnd,
                                     player.config["account"]["id"], player.config["account"]["pass"], player.config["account"]["select_offset"])
            if player.check_lifetime():
                player.__init__(player.name)

            player.check_death()

            player._buy_pots()

            player.distribute_stats()

            if player.try_reset():
                continue

            player.ensure_on_best_spot()

            player.farm()
