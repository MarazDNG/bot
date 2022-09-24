#
# Game login and game logout
#

from mu_window import mu_window
from arduino_api import arduino_api
from conf.conf import KEY_ESC, KEY_RETURN

import time


def server_selection():
    """ Logout into server selection.
    """

    arduino_api.send_ascii(KEY_ESC)
    # click select
    mu_window.click_on_pixel((600, 280))
    time.sleep(6)


def game_login(login: str, password: str):
    """ Log in from the server selection and
    choose character.
    """
    # TODO
    # pop up server selection
    mu_window.click_on_pixel((450, 305))

    # select server
    mu_window.click_on_pixel((600, 305))

    # click login
    mu_window.click_on_pixel((650, 460))
    mu_window.send_string(login)

    # click password
    mu_window.click_on_pixel((650, 490))
    mu_window.send_string(password)

    # click ok
    mu_window.click_on_pixel((660, 540))

    # click auto-login
    # mu_window.click_on_pixel((520, 590))

    # click on character
    mu_window.click_on_pixel((360, 530))

    # load character
    arduino_api.send_ascii(KEY_RETURN)

    # wait for character loading
    time.sleep(7)
