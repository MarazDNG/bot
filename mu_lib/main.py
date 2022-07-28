import time

from game_methods import game_methods
from mu_bot.main import go_to, warp_to, start_helper
from mu_bot.main import LORA_GOAL, ELB_GOAL, ATL_GOAL
from .scripts import activate_window
from mu_bot.game_account_actions import server_selection, game_login
from mu_bot.reset import reset


activate_window()
# 295, 30, 10, 10 - whole helper sign
# 299, 35, 1, 1 - helper pixel
# helper pixel - (74, 53, 5) - ON
# helper pixel - (239, 174, 36) - OFF


area = "lorencia"
warp_to(area)

counter = 0

while True:
    lvl = game_methods.read_lvl()
    if counter > 5:
        raise Exception("Lvl could not be retrieved!")

    if not lvl:
        counter += 1
        continue

    time.sleep(5)
    print(lvl)

    if lvl < 20:
        if area != 'lorencia':
            area = 'lorencia'
            warp_to(area)

        if lvl < 10:
            if not game_methods.is_helper_on():
                go_to(LORA_GOAL, 'lorencia')
                start_helper()
            time.sleep(10)

    elif lvl in range(20, 80):
        if area != 'elbeland':
            area = 'elbeland'
            warp_to("elbeland2")

        if not game_methods.is_helper_on():
            go_to(ELB_GOAL, 'elbeland')
            start_helper()

    elif lvl in range(80, 140):
        if area != 'atlans':
            area = 'atlans'
            warp_to("atlans2")

        if not game_methods.is_helper_on():
            go_to(ATL_GOAL, 'atlans')
            start_helper()

    elif lvl in range(140, 280):
        pass

    elif lvl in range(280, 400):
        area = 'peaceswamp'
        warp_to(area)
        print("WELL DONE!!!")
        print('\a')
        break

    elif lvl == 400:
        server_selection()
        reset()
        activate_window()
        game_login()
