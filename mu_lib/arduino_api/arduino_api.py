"""
Arduino mouse and keyboard API for python.

"""

import numpy
import pyautogui
from serial.serialwin32 import Serial

UPPER_LIMIT = 120
LOWER_LIMIT = -120
PORT = 'COM12'
ENDING_SIGN = 'r'
INT_STARTING_SIGN = '|'
STRING_STARTING_SIGN = '%'


def send_string(data: str):
    """ Send string to Arduino. """
    arduino = Serial(PORT)
    arduino.write(f'{STRING_STARTING_SIGN}{data}{ENDING_SIGN}'.encode('utf-8'))


def send_ascii(data: int):
    """ Send char in ascii code. """
    arduino = Serial(PORT)
    arduino.write(f'{INT_STARTING_SIGN}{data}{ENDING_SIGN}'.encode('utf-8'))


def _send(data):
    """ Send encoded data to Arduino port."""
    arduino = Serial(PORT)
    arduino.write(f'{data}{ENDING_SIGN}'.encode('utf-8'))


def hold_right():
    release_buttons()
    _send('r')


def hold_left() -> None:
    release_buttons()
    _send('l')


def release_buttons():
    _send('x')


def click():
    _send('k')


def ard_mouse_to_pos(target_pos):
    """ Move to the given pixel the screen. """
    pos = pyautogui.position()
    pos = numpy.array([pos.x, pos.y])
    vector = (
        target_pos[0] - pos[0],
        target_pos[1] - pos[1],
    )
    _send(f'{vector[0]}:{vector[1]}')


def mouse_move(pos):
    """ Move by delta. """
    _send(f'{pos[0]}:{pos[1]}')
