#
# Game login and game logout
#

import multiprocessing
import time
import subprocess
import multiprocessing

import arduino_api
import window_api

from . import KEY_ESC, KEY_RETURN


def _start_launcher():
    subprocess.call(r"C:\Users\Public\Desktop\ETERNMU.lnk", shell=True)
    print("\a")


def start_game():
    import os
    # run launcher.exe
    # os.system(r"C:\Users\Public\Desktop\ETERNMU.lnk")
    p = multiprocessing.Process(target=_start_launcher)
    p.start()
    time.sleep(1)

    # find launcher start_pixel
    window_api.window_start_pixel_by_title("Launcher")

    # click start
    arduino_api.ard_mouse_to_pos((730, 410))

    # sleep
    time.sleep(5)


def server_selection(hwnd: int):
    """ Logout into server selection.
    """

    arduino_api.send_ascii(KEY_ESC)
    # click select
    arduino_api.ard_mouse_to_pos(window_api.window_pixel_to_screen_pixel(600, 280))
    time.sleep(6)


def game_login(hwnd: int, login: str, password: str):
    """ Log in from the server selection and
    choose character.
    """
    # pop up server selection
    
    arduino_api.ard_mouse_to_pos(window_api.window_pixel_to_screen_pixel(450, 305))

    # select server
    arduino_api.ard_mouse_to_pos(window_api.window_pixel_to_screen_pixel(600, 305))

    # click login
    arduino_api.ard_mouse_to_pos(window_api.window_pixel_to_screen_pixel(650, 460))
    arduino_api.send_string(login)

    # click password
    arduino_api.ard_mouse_to_pos(window_api.window_pixel_to_screen_pixel(650, 490))
    arduino_api.send_string(password)

    # click ok
    arduino_api.ard_mouse_to_pos(window_api.window_pixel_to_screen_pixel(660, 540))

    # click auto-login
    # arduino_api.ard_mouse_to_pos((520, 590))

    # click on character
    arduino_api.ard_mouse_to_pos(window_api.window_pixel_to_screen_pixel(360, 530))

    # load character
    arduino_api.send_ascii(KEY_RETURN)

    # wait for character loading
    time.sleep(7)
