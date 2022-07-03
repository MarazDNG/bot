"""
Arduino mouse and keyboard API for python.

"""

import numpy
import pyautogui
from serial.serialwin32 import Serial

UPPER_LIMIT = 120
LOWER_LIMIT = -120
PORT = 'COM6'
ENDING_SIGN = '`'
INT_STARTING_SIGN = '|'
STRING_STARTING_SIGN = '%'


def send_string(data):
    arduino = Serial(PORT)
    arduino.write(f'{STRING_STARTING_SIGN}{data}{ENDING_SIGN}'.encode('utf-8'))


def send_ascii(data):
    arduino = Serial(PORT)
    arduino.write(f'{INT_STARTING_SIGN}{data}{ENDING_SIGN}'.encode('utf-8'))


def send(data):
    """ Send encoded data to Arduino port."""
    arduino = Serial(PORT)
    arduino.write(f'{data}{ENDING_SIGN}'.encode('utf-8'))


def hold_right():
    release_buttons()
    send('r')


def hold_left() -> None:
    release_buttons()
    send('l')


def release_buttons():
    send('x')


def click():
    send('k')


def mouse_to_pos(target_pos):
    """ Move to the given pixel. """
    pos = pyautogui.position()
    pos = numpy.array([pos.x, pos.y])
    vector = target_pos - pos
    send(f'{vector[0]}:{vector[1]}')


def mouse_move(pos):
    """ Move by delta. """
    send(f'{pos[0]}:{pos[1]}')
