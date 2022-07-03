#
# Provide image which contains desired information.
#


import numpy
from system_info import game_start_pixel
from PIL import ImageGrab, Image
import cv2
import win32con
import win32gui
import win32ui


def get_image_of(info_type):

    #win_x, win_y = game_start_pixel()

    if info_type == "coords":
        return my_grab()
        #win_x += 70
        #win_y += 20
        #bbox = (win_x, win_y, win_x+150, win_y+30)
        #img = ImageGrab.grab(bbox=bbox)

    elif info_type == "lvl":
        screenshot = ImageGrab.grab(bbox=None)
        screenshot = numpy.array(screenshot)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        needle = cv2.imread('lvl.png', cv2.IMREAD_UNCHANGED)
        needle = cv2.cvtColor(needle, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(screenshot, needle, cv2.TM_CCOEFF_NORMED)
        max_loc = cv2.minMaxLoc(result)[3]
        x = max_loc[0] + 20
        y = max_loc[1]
        bbox = (x, y, x+25, y+8)
        img = ImageGrab.grab(bbox=bbox)

    return img


def my_grab():
    left, top = game_start_pixel()
    w = 80
    h = 8

    hdesktop = win32gui.GetDesktopWindow()
    hwndDC = win32gui.GetWindowDC(hdesktop)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    result = saveDC.BitBlt((0, 0), (w, h), mfcDC,
                           (left+110, top+36), win32con.SRCCOPY)

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
