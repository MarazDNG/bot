from arduino_api.arduino_api import send_string, send_ascii
from mu_window import mu_window
import pygetwindow as gw
import time

from game_methods.game_methods import read_lvl_from_frame, read_lvl
from game_methods.game_methods import get_to2
from game_methods.game_methods import prebihani
from game_methods.game_methods import _walk_on_shortest_straight
from arduino_api import arduino_api

win = gw.getWindowsWithTitle("Player")[0]
win.activate()
time.sleep(1.5)

# print(read_coords_from_frame())

path1 = [
    (77, 172),
    (78, 172),
    (79, 172),
    (80, 172),
    (81, 172),
    (82, 172),
    (83, 173),
    (84, 174),
    (83, 174),
    (83, 175),
    (82, 176),
]

# 189, 153
# 194, 146

path2 = [
    (189, 153),
    (190, 152),
    (191, 151),
    (192, 150),
    (193, 149),
    (194, 148),
    (194, 147),
    (194, 146),
]

path3 = [
    (53, 14),
    (53, 15),
    (53, 16),
    (53, 17),
    (53, 18),
    (53, 19),
    (53, 20),
    (53, 21),
    (53, 22),
    (53, 23),
    (53, 24),
    (53, 25),
]

# send_ascii(ord("c"))

lvl = read_lvl()
print("LVL:", lvl)
# while True:
#     prebihani(path3)
# send
