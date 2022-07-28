from arduino_api.arduino_api import send_string, send_ascii
from mu_window import mu_window
import pygetwindow as gw
import time

from game_methods import game_methods
from arduino_api import arduino_api
from mu_bot.main import go_to, warp_to, start_helper
from mu_bot.main import LORA_GOAL, ELB_GOAL, ATL_GOAL
from scripts import activate_window


activate_window()

while True:

    area = "lorencia"
    warp_to(area)

    while True:
        lvl = game_methods.read_lvl()
        time.sleep(5)
        print(lvl)

        if lvl < 20:
            if area != 'lorencia':
                area = 'lorencia'
                warp_to(area)

            go_to(LORA_GOAL, 'lorencia')

            if lvl < 10:
                time.sleep(10)
            else:
                start_helper()

        elif lvl in range(20, 80):
            if area != 'elbeland':
                area = 'elbeland'
                warp_to("elbeland2")
            go_to(ELB_GOAL, 'elbeland')
            start_helper()

        elif lvl in range(80, 140):
            if area != 'atlans':
                area = 'atlans'
                warp_to("atlans2")
            go_to(ATL_GOAL, 'atlans')
            start_helper()

        elif lvl in range(140, 280):
            pass

        elif lvl in range(280, 400):
            area = 'swampofpeace'
            warp_to(area)
            print("WELL DONE!!!")
            print('\a')
            break

        # elif lvl == 400:
        #     server_selection()
        #     reset()
        #     game_login()
