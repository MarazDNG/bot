#
# Game login and game logout
#


from curses import KEY_SELECT
from time import time
from i_arduino import click, send_ascii
from i_mouse import game_mouse_to_pixel
from system_info import game_start_pixel
from keys import KEY_ESC, KEY_RETURN


def server_selection():
    """ Logout into server selection.
    """

    send_ascii(KEY_ESC)
    # click select
    game_mouse_to_pixel((400, 100))
    click()
    time.sleep(6)


def game_login():
    """ Log in from the server selection and
    choose character.
    """
    # pop up server selection
    game_mouse_to_pixel((1, 2))
    click()

    # select server
    game_mouse_to_pixel((1, 2))
    click()

    # click auto-login
    game_start_pixel((1, 2))
    click()

    # click on character
    game_mouse_to_pixel((1, 2))
    click()

    # load character
    send_ascii(KEY_RETURN)

    # wait for character loading
    time.sleep(5)
