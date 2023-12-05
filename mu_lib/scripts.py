import win32api
import time
import pyautogui
from game_logic import map
from game_logic import game_menu
from game_logic import browser
from game_logic import config
from game_logic import meth
from game_logic.Player import Player
import time
import os
from game_logic import memory
import window_api
import arduino_api
from game_logic.map import Warp, check_spot_accessibility


path_dev4 = [
    (72, 177),
    (73, 177),
    (74, 177),
    (75, 177),
    (76, 178),
    (77, 179),
    (78, 180),
    (79, 181),
    (80, 182),
]


def preset():
    p = Player("Consumer")
    p.try_reset()


def close():
    p = Player("Consumer")
    window_api.window_activate_by_handler(p._window_hwnd)
    p.close_game()


def modify_config():
    from game_logic import meth

    meth.modify_config("Silco:stats:str=f4000")


def save_zen():
    id = "Maraz"
    pwd = "***REMOVED***"
    position = 2
    browser.save_zen(id, pwd, position)


def go_cw():
    CONFIG_PATH = r"C:\Users\Avatar\smart\bot\mu_lib\conf"
    config.ConfigManager.init(CONFIG_PATH)
    arduino_api.ard_init(3)
    p = Player("krtecek")
    p.warp(Warp(10, "crywolf", (234, 39)))


def resize_img():
    # add 100 green pixels to the right and bottom
    from PIL import Image
    # Create a new image with green background

    img = Image.open("img_lorencia.png")
    new_image = Image.new("RGB", (300, 300), (0, 255, 0))

    # Paste the original image onto the new image
    new_image.paste(img, (0, 0))
    new_image.save("resized.png")


def incw():
    CONFIG_PATH = r"C:\Users\Avatar\smart\bot\mu_lib\conf"
    config.ConfigManager.init(CONFIG_PATH)
    arduino_api.ard_init(3)
    p = Player("krtecek")
    res = p._in_map("crywolf")
    print(res)

def initplayer(name: str):
    CONFIG_PATH = r"C:\Users\Avatar\smart\bot\mu_lib\conf"
    config.ConfigManager.init(CONFIG_PATH)
    arduino_api.ard_init(3)
    return Player(name)


def testcw():
    p = initplayer("krtecek")
    p.map = "valley"
    p._go_to_coords((162, 44))
    time.sleep(3)
    if p._in_map("crywolf"):
        print("in cw")
    if meth.distance(p.coords, (234, 39)):
        print("distance ok")
    # res =
    # print(res)

def units():
    p = initplayer("krtecek")
    res = p._surrounding_units()
    print(res)

def valley_map():
    p = initplayer("krtecek")
    bbox = 1060, 631, 100, 1
    # img.show()
    def map_open():
        img = window_api.window_grab_image(p._window.hwnd, *bbox)
        import numpy
        img_1d = [tuple(x) for x in numpy.asarray(img)[0]]
        return all(all(i < 10 for i in x) for x in img_1d)
    counter = 0
    while map_open() and counter <= 3:
        arduino_api.send_ascii(179)
        counter += 1
        time.sleep(1)
    # print(res)
    # print(img_1d)

def portal():
    p = initplayer("krtecek")
    # p.map = "peaceswamp"
    # p._walk_through_portal((139, 125))
    # p._walk_through_portal((124, 110))
    # p._walk_through_portal((161, 42))
    p._walk_through_portal((240, 15))

def menu():
    hwnd = window_api.window_handler_by_title("Switch Char")
    window_api.window_activate_by_handler(hwnd)
    for i in range(4):
        screen_pos = window_api.window_pixel_to_screen_pixel(hwnd, 1100, 170+i*80)
        win32api.SetCursorPos(screen_pos)
        time.sleep(0.5)

def res_pos():
    browser.do_reset_on_web("Zaram", "Dng163524", 1)

def test_login():
    hwnd = window_api.window_handler_by_title("Select Server")
    screen_pos = window_api.window_pixel_to_screen_pixel(hwnd, 200, 240)
    win32api.SetCursorPos(screen_pos)

    screen_pos = window_api.window_pixel_to_screen_pixel(hwnd, 200, 300)
    win32api.SetCursorPos(screen_pos)

    screen_pos = window_api.window_pixel_to_screen_pixel(hwnd, 600, 300)
    win32api.SetCursorPos(screen_pos)
    time.sleep(1)

    screen_pos = window_api.window_pixel_to_screen_pixel(hwnd, 600, 410)
    win32api.SetCursorPos(screen_pos)

    screen_pos = window_api.window_pixel_to_screen_pixel(hwnd, 600, 520)
    win32api.SetCursorPos(screen_pos)

if __name__ == "__main__":
    # win_id = mu_window.window_id_by_title("Consumer")
    # while True:
    #     [print(unit.name, unit.coords)
    #      for unit in memory.get_surrounding_units(win_id) if "rc" in unit.name]
    # exit()
    time.sleep(2)
    # hwnd = window_api.window_handler_by_title("Maraz")
    # id = window_api.window_id_by_title("Maraz")
    # print(id)
    p = initplayer("krtecek")
    print(p._config["account"]["pass"])
    # menu()
    # res_pos()
    # test_login()
    # portal()
    # go_cw()
    # valley_map()