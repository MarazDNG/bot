import contextlib
from game_logic import game_menu
from game_logic.Player import Player
from game_logic.exceptions import WrongArgumentsException, TooManyIterationsException, WarpException, ChatError
from game_logic import meth
from game_logic import KEY_RETURN
from game_logic import config

import logging
import sys
import window_api
import arduino_api
import pygetwindow as gw
import queue


CONFIG_PATH = r"C:\Users\Maraz\smart\bot\mu_lib\conf"

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        filename="mu.log",
                        filemode="w",
                        datefmt="%Y/%m/%d %H:%M:%S",)

    if len(sys.argv) == 1:
        raise WrongArgumentsException("Character name is required.")

    arduino_api.ard_init(3)
    config.ConfigManager.init(CONFIG_PATH)

    player_pool = [Player(sys.argv[i]) for i in range(1, len(sys.argv))]

    q = queue.Queue()
    while True:
        with contextlib.suppress(queue.Empty):
            next_config_change = q.get(timeout=1)
            config.ConfigManager.modify(next_config_change)

        for player in player_pool:
            try:
                meth.protection_click()
                window_api.window_activate(f"Player: {player.name}")
            except IndexError:
                game_menu.start_game()
                meth.protection_click()
                hwnd = window_api.window_handler_by_regex("^EternMU$")
                window_api.window_activate_by_handler(hwnd)
                game_menu.game_login(hwnd,
                                     player._config["account"]["id"], player._config["account"]["pass"], player._config["account"]["select_offset"])
            if player.check_lifetime():
                player.__init__(player.name)

            try:
                player.check_death()

                player.buy_pots()

                player.distribute_stats()

                if player.try_reset():
                    continue

                player.ensure_on_best_spot()

                player.farm()
            except (TooManyIterationsException, WarpException, ChatError) as e:
                window_api.window_activate_by_handler(player._window_hwnd)
                player.close_game()
                arduino_api.send_ascii(KEY_RETURN)
                player.__init__(player.name)
