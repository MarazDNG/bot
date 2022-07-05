from system_info import game_start_pixel
from i_arduino import mouse_to_pos


def game_mouse_to_pixel(pos: tuple):
    window_pos = game_start_pixel()
    x = window_pos[0] + pos[0]
    y = window_pos[1] + pos[1]
    mouse_to_pos((x, y))
