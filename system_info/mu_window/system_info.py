#
# Provide information about the game window.
#


import win32gui


WINDOW_PARTIAL_TEXT = "Player:"


def game_start_pixel():
    """ Return starting pixel of the game."""
    if hasattr(game_start_pixel, "window"):
        return game_start_pixel.window

    h = []

    def winEnumHandler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd) and WINDOW_PARTIAL_TEXT in win32gui.GetWindowText(hwnd):
            #print(hex(hwnd), win32gui.GetWindowText(hwnd))
            h.append(hwnd)
    win32gui.EnumWindows(winEnumHandler, None)

    # If something fcks up, try converting GetWindowRect armgument
    # to hexadecimal type with hex() function.
    x, y, _, _ = win32gui.GetWindowRect(h[0])

    game_start_pixel.window = (x, y)
    return (x, y)
