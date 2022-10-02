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
    time.sleep(2)

    # find launcher start_pixel
    hwnd = window_api.window_handler_by_title("Launcher")

    # click start
    pixel = window_api.window_pixel_to_screen_pixel(hwnd, 730, 410)    
    arduino_api.ard_mouse_to_pos(pixel)
    arduino_api.click()
    
    # sleep
    time.sleep(10)


def server_selection(hwnd: int):
    """ Logout into server selection.
    """

    arduino_api.send_ascii(KEY_ESC)
    # click select
    arduino_api.ard_mouse_to_pos(window_api.window_pixel_to_screen_pixel(hwnd, 600, 280))
    time.sleep(0.5)
    arduino_api.click()
    time.sleep(0.5)
    
    time.sleep(6)


def game_login(hwnd: int, login: str, password: str, offset: int):
    """ Log in from the server selection and
    choose character.
    """
    # pop up server selection
    
    arduino_api.ard_mouse_to_pos(window_api.window_pixel_to_screen_pixel(hwnd, 450, 305))
    time.sleep(0.5)
    arduino_api.click()
    time.sleep(0.5)

    # select server
    arduino_api.ard_mouse_to_pos(window_api.window_pixel_to_screen_pixel(hwnd, 600, 305))
    time.sleep(0.5)
    arduino_api.click()
    time.sleep(0.5)

    # click login
    arduino_api.ard_mouse_to_pos(window_api.window_pixel_to_screen_pixel(hwnd, 650, 460))
    time.sleep(0.5)
    arduino_api.click()
    time.sleep(0.5)
    arduino_api.send_string(login)

    # click password
    arduino_api.ard_mouse_to_pos(window_api.window_pixel_to_screen_pixel(hwnd, 650, 490))
    time.sleep(0.5)
    arduino_api.click()
    time.sleep(0.5)
    arduino_api.send_string(password)

    # click ok
    arduino_api.ard_mouse_to_pos(window_api.window_pixel_to_screen_pixel(hwnd, 660, 540))
    time.sleep(0.5)
    arduino_api.click()
    time.sleep(0.5)

    # click auto-login
    # arduino_api.ard_mouse_to_pos((520, 590))

    # click on character
    arduino_api.ard_mouse_to_pos(window_api.window_pixel_to_screen_pixel(hwnd, 360 + offset, 530))
    time.sleep(0.5)
    arduino_api.click()
    time.sleep(0.5)

    # load character
    arduino_api.send_ascii(KEY_RETURN)

    # wait for character loading
    time.sleep(7)
