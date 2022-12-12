import contextlib
from game_logic import game_menu
from game_logic.Player import Player
from game_logic.exceptions import (
    WrongArgumentsException,
    TooManyIterationsException,
    WarpException,
    ChatError,
)
from game_logic import meth
from game_logic import KEY_RETURN
from game_logic import config

import logging
import sys
import window_api
import arduino_api
import pygetwindow as gw

from multiprocessing import Process, Queue
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    filters,
    MessageHandler,
)


CONFIG_PATH = r"C:\Users\Maraz\smart\bot\mu_lib\conf"
TOKEN = "5738719734:AAFxl-8hEkCms58QatVz9D7FeJxCGArfP8g"


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text
    )
    return update.message.text


async def echo_wrapper(*args, q=None):
    res = await echo(*args)
    q.put(res)


def telegram_bot(q: Queue):
    application = ApplicationBuilder().token(TOKEN).build()

    callback = lambda *args: echo_wrapper(*args, q=q)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), callback)
    application.add_handler(echo_handler)

    application.run_polling()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        filename="mu.log",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S",
    )

    if len(sys.argv) == 1:
        raise WrongArgumentsException("Character name is required.")

    arduino_api.ard_init(3)
    config.ConfigManager.init(CONFIG_PATH)

    player_pool = [Player(sys.argv[i]) for i in range(1, len(sys.argv))]

    q = Queue()
    p_telegram = Process(target=telegram_bot, args=(q,))
    p_telegram.start()

    while True:
        next_config_change = None
        try:
            next_config_change = q.get(timeout=1)
        except:
            pass
        if next_config_change:
            action_type, value = next_config_change.split(" ", 1)
            if action_type == "cfg":
                config.ConfigManager.modify(value)
            elif action_type == "on":
                if value in [p.name for p in player_pool]:
                    print(f"Player {value} is already in game.")
                else:
                    player = Player(value)
                    player_pool.append(player)
            elif action_type == "off":
                player = [p for p in player_pool if p.name == value]
                if player:
                    player = player[0]
                    while True:
                        try:
                            window_api.window_activate_by_handler(player._window_hwnd)
                            break
                        except:
                            continue
                    player.close_game()
                    player_pool.remove(player)
                else:
                    print(f"Player {value} is not in game.")
            else:
                print("Not valid config change.")
            continue

        logging.debug("Initiating game loop.")
        for player in player_pool:
            logging.debug(f"Player {player.name} loop - start.")
            try:
                meth.protection_click()
                window_api.window_activate(f"Player: {player.name}")
            except IndexError:
                game_menu.start_game()
                meth.protection_click()
                hwnd = window_api.window_handler_by_regex("^EternMU$")
                window_api.window_activate_by_handler(hwnd)
                game_menu.game_login(
                    hwnd,
                    player._config["account"]["id"],
                    player._config["account"]["pass"],
                    player._config["account"]["select_offset"],
                )
            if player.zen:
                logging.debug(f"Player {player.name} is zenning. {player.zen}")
                player.save_zen()
                continue

            if player.check_lifetime():
                player.__init__(player.name)

            try:
                if player.lvl == 400 and player.reset == 100:
                    logging.info(f"Player {player.name} reached max level and reset.")
                    player.close_game()
                    player_pool.remove(player)
                    continue

                player.check_death()

                player.buy_pots()

                player.distribute_stats()

                if player.do_reset():
                    player = Player(player.name)
                    continue

                player.ensure_on_best_spot()

                player.farm()
            except (TooManyIterationsException, WarpException, ChatError) as e:
                logging.error(f"Player {player.name} error: {e}")   
                window_api.window_activate_by_handler(player._window.hwnd)
                player.close_game()
                arduino_api.send_ascii(KEY_RETURN)
                player.__init__(player.name)
        logging.debug("Ending game loop.")
