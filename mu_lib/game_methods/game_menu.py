#
# Game login and game logout
#

from mu_window import mu_window
from arduino_api import arduino_api
from .keys import KEY_ESC, KEY_RETURN

import time


def server_selection():
    """ Logout into server selection.
    """

    arduino_api.send_ascii(KEY_ESC)
    # click select
    mu_window.click_on_pixel((600, 280))
    time.sleep(6)


def game_login():
    """ Log in from the server selection and
    choose character.
    """
    # pop up server selection
    mu_window.click_on_pixel((450, 305))

    # select server
    mu_window.click_on_pixel((600, 305))

    # click auto-login
    mu_window.click_on_pixel((520, 590))

    # click on character
    mu_window.click_on_pixel((360, 530))

    # load character
    arduino_api.send_ascii(KEY_RETURN)

    # wait for character loading
    time.sleep(5)
