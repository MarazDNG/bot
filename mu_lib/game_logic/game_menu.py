#
# Game login and game logout
#

import multiprocessing
import time
import subprocess
import multiprocessing

import arduino_api
import window_api
import win32api

from . import KEY_ESC, KEY_RETURN

POSITION_OFFSET = 80

def _start_launcher():
    subprocess.call(r"C:\Users\Public\Desktop\ETERNMU.lnk", shell=True)
    print("\a")


def start_game():
    import os

    # run launcher.exe
    # os.system(r"C:\Users\Public\Desktop\ETERNMU.lnk")
    p = multiprocessing.Process(target=_start_launcher)
    p.start()
    time.sleep(4)

    # find launcher start_pixel
    hwnd = window_api.window_handler_by_title("Launcher")

    # click start
    pixel = list(map(int, window_api.window_pixel_to_screen_pixel(hwnd, 730, 410)))
    win32api.SetCursorPos(pixel)
    arduino_api.click()

    # sleep
    time.sleep(10)


def server_selection(hwnd: int):
    """Logout into server selection."""

    arduino_api.send_ascii(KEY_ESC)
    # click select
    win32api.SetCursorPos(
        list(map(int, window_api.window_pixel_to_screen_pixel(hwnd, 600, 280)))
    )
    time.sleep(0.5)
    arduino_api.click()
    time.sleep(0.5)

    time.sleep(6)


def game_login(hwnd: int, login: str, password: str, position: int):
    """Log in from the server selection and
    choose character.
    """
    # pop up server selection
    win32api.SetCursorPos(
        list(map(int, window_api.window_pixel_to_screen_pixel(hwnd, 200, 240)))
    )
    time.sleep(0.5)
    arduino_api.click()
    time.sleep(0.5)

    # select server
    # server 1: y = 305
    # server 2: y = 330
    win32api.SetCursorPos(
        list(map(int, window_api.window_pixel_to_screen_pixel(hwnd, 200, 300)))
    )
    time.sleep(0.5)
    arduino_api.click()
    time.sleep(0.5)

    # click login
    win32api.SetCursorPos(
        list(map(int, window_api.window_pixel_to_screen_pixel(hwnd, 600, 300)))
    )
    time.sleep(0.5)
    arduino_api.click()
    time.sleep(0.5)
    arduino_api.send_string(login)

    # click password
    win32api.SetCursorPos(
        list(map(int, window_api.window_pixel_to_screen_pixel(hwnd, 600, 410)))
    )
    time.sleep(0.5)
    arduino_api.click()
    time.sleep(0.5)
    arduino_api.send_string(password)

    # click ok
    win32api.SetCursorPos(
        list(map(int, window_api.window_pixel_to_screen_pixel(hwnd, 600, 520)))
    )
    time.sleep(0.5)
    arduino_api.click()
    time.sleep(0.5)

    # click auto-login
    # win32api.SetCursorPos((520, 590))

    # click on character
    win32api.SetCursorPos(
        list(map(int, window_api.window_pixel_to_screen_pixel(hwnd, 1100, 170 + position * 80)))
    )
    time.sleep(0.5)
    arduino_api.click()
    time.sleep(0.5)

    # load character
    arduino_api.send_ascii(KEY_RETURN)

    # wait for character loading
    time.sleep(7)
