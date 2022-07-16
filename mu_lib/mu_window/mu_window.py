import win32gui
import win32ui
import win32con
from PIL import Image


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


def grab_imgage_from_window(x: int, y: int, w: int, h: int) -> Image:
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


def press():
    pass


def wait():
    pass
