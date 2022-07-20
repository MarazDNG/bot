import win32gui
import win32ui
import win32con
import time
from PIL import Image

from arduino_api.arduino_api import ard_mouse_to_pos, send_string
from arduino_api.arduino_api import click
from arduino_api.arduino_api import hold_left
from arduino_api.arduino_api import hold_right
from arduino_api.arduino_api import release_buttons


def _game_start_pixel() -> tuple:
    """ Return starting pixel of the game."""
    if hasattr(_game_start_pixel, "window"):
        return _game_start_pixel.window

    h = []

    def winEnumHandler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd) and WINDOW_PARTIAL_TEXT in win32gui.GetWindowText(hwnd):
            #print(hex(hwnd), win32gui.GetWindowText(hwnd))
            h.append(hwnd)
    win32gui.EnumWindows(winEnumHandler, None)

    # If something fcks up, try converting GetWindowRect armgument
    # to hexadecimal type with hex() function.
    x, y, _, _ = win32gui.GetWindowRect(h[0])

    _game_start_pixel.window = (x, y)
    return (x, y)


def grab_image_from_window(x: int, y: int, w: int, h: int) -> Image:
    """Return image with coordinates."""
    hdesktop = win32gui.GetDesktopWindow()
    hwndDC = win32gui.GetWindowDC(hdesktop)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    result = saveDC.BitBlt((0, 0), (w, h), mfcDC,
                           (x, y), win32con.SRCCOPY)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hdesktop, hwndDC)
    return im


def press(keys: str):
    send_string(keys)


def wait(time_sec: int):
    time.sleep(time_sec)


def mouse_event(event):
    if event == "click":
        click()
    if event == "hold_left":
        hold_left()
    if event == "hold_right":
        hold_right()
    if event == "release_buttons":
        release_buttons()


def mouse_to_pos(game_pos):
    """Move mouse to given position in the window."""
    ard_mouse_to_pos(
        _game_start_pixel() + game_pos
    )
