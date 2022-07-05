
from mu_input.game_api import get_to
from mu_input.game_api import read_coords
from mu_input.game_api import read_lvl
from mu_input.arduino_api import send_ascii
from mu_input.arduino_api import release_buttons
from mu_input.arduino_api import hold_left
from mu_input.arduino_api import send_string

import time
from .keys import KEY_RETURN, KEY_HOME


def move_to_coords(*args):
    # TODO
    print('go_to start')
    get_to(*args)
    print('go_to end')


def get_my_lvl() -> int:
    send_string('c')
    time.sleep(1)
    lvl = read_lvl()
    if lvl == 0:
        send_string('c')
        time.sleep(1)
    lvl = read_lvl()
    if lvl == 0:
        raise Exception("Lvl could not be retrieved!")
    send_string('c')
    time.sleep(1)
    return lvl


def get_my_coords() -> tuple:
    return read_coords()


def custom_attack():
    send_string('5')
    hold_left()
    time.sleep(10)
    release_buttons()


def warp_to(area):
    send_ascii(KEY_RETURN)
    send_string(f'/warp {area}')
    send_ascii(KEY_RETURN)


def start_helper():
    send_ascii(KEY_HOME)
