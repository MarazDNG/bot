
from i_game import get_to, read_lvl, read_coords
from i_arduino import hold_left, release_buttons, send_ascii, send_string
import time
from keys import KEY_RETURN, KEY_HOME


def go_to(*args):
    print('go_to start')
    get_to(*args)
    print('go_to end')


def get_lvl():
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


def get_coords():
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
