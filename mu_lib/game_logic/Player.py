import contextlib
import os
import cv2
import numpy
import yaml
import logging
import requests
import re
import time
from cached_property import cached_property_with_ttl
import logging
from multiprocessing import Process
from datetime import datetime, timedelta
import pygetwindow as gw

import window_api
import arduino_api

from . import memory
from . import meth
from . import KEY_RETURN, ORIGIN
from . import game_menu
from . import walking_vector
from . import config
from . import browser

from .exceptions import (
    DeathException,
    WarpException,
    ResetError,
    ChatError,
    TooManyIterationsException,
)
from .meth import distance, get_online_players, _if_stucked
from .browser import do_reset_on_web
from .map import get_mu_map_list, Warp
from .djikstra import djikstra8
from .map_list import MAP_DICT


class FarmingSystem:
    def __init__(self):
        self._farming_spot_index = 0
        self._farming_flag = False
        self._farming_coords = None


class WindowSystem:
    def __init__(self, partial_title: str):
        self._partial_title = partial_title
        self.__window_id = None
        self.__window_hwnd = None

    @property
    def hwnd(self):
        if not self.__window_hwnd:
            self.__window_hwnd = window_api.window_handler_by_title(self._partial_title)
        return self.__window_hwnd

    @property
    def id(self):
        if self.__window_id is None:
            self.__window_id = window_api.window_id_by_title(self._partial_title)
        return self.__window_id


class Player:
    def __init__(self, char_name: str):
        self.name = char_name
        self._config = config.ConfigManager.config_for_player(self.name)
        self.zen = self._config["zen"] if "zen" in self._config else False
        self._farming = FarmingSystem()
        self._window = WindowSystem(self.name)

        self.__map = None

        logging.info(f"Initialized player {self.name}")
        self.birthtime = datetime.now()

    # PROPS
    @property
    def reset(self) -> int:
        window_title = window_api.window_title_by_handler(self._window.hwnd)
        reset_str = re.search("Reset: \d+", window_title)[0]
        return int(reset_str.split()[1])

    @property
    def lvl(self):
        window_title = window_api.window_title_by_handler(self._window.hwnd)
        lvl_str = re.search("Level: \d+", window_title)[0]
        return int(lvl_str.split()[1])

    @property
    def coords(self) -> tuple:
        return memory.my_coords(self._window.id)

    @cached_property_with_ttl(ttl=12 * 60 * 60)
    def gr(self):
        resp = requests.get(
            f"https://eternmu.cz/profile/player/req/{self.name}/", verify=False
        )
        gr_str = re.search("Grand resety</td><td>\d+", resp.text)[0]
        return int(gr_str.split("</td><td>")[1])

    @property
    def map(self):
        if self.lvl < 10:
            self.__map = self._config["starting_warp"]
        return self.__map

    @map.setter
    def map(self, map_warp_name: str):
        """Take map name or warp name."""
        self.__map = "".join(i for i in map_warp_name if i.isalpha())

    def warp(self, warp: Warp):
        if self.lvl < 10:
            self.map = self._config["starting_warp"]
            logging.info("Player is too low level to warp")
            return

        def warp_to(warp: Warp) -> None:
            """Used only when required level is met."""

            def peaceswamp1():
                self.warp(Warp(300, "peaceswamp", (139, 108)), "peaceswamp")
                self._go_to_coords((139, 125))

            tmp = self.coords

            if warp.name in locals():
                locals()[warp.name]()
            else:
                self._write_to_chat(f"/warp {warp.name}")
            time.sleep(3)

            if self.coords == tmp and self.coords != warp.coords:
                if warp.name in locals():
                    locals()[warp.name]()
                else:
                    self._write_to_chat(f"/warp {warp.name}")
                time.sleep(3)
                if self.coords == tmp:
                    raise WarpException(
                        f"Warp failed from {self.map} {self.coords} to {warp.name}"
                    )

        warp_to(warp)
        self.map = warp.name
        self._farming._farming_flag = False

    # PUBLIC METHODS

    def save_zen(self):
        if not getattr(self, "_zen_save", False):
            self._zen_save = datetime.now()

        if (datetime.now() - self._zen_save).total_seconds() < 60 * 60:
            return

        self._zen_save = datetime.now()

        game_menu.server_selection(self._window.hwnd)
        # login to eternmu.cz
        browser.save_zen(
            self._config["account"]["id"],
            self._config["account"]["pass"],
            self._config["account"]["position"],
        )
        window_api.window_activate_by_handler(self._window.hwnd)
        game_menu.game_login(
            self._window.hwnd,
            self._config["account"]["id"],
            self._config["account"]["pass"],
            self._config["account"]["select_offset"],
        )
        time.sleep(2)
        # login back to game and start helper
        self.farm()

    def buy_pots(self):
        if meth._detect_pots(self._window.hwnd):
            return

        logging.debug("Going for pots")
        # go to shop
        self.warp(Warp(20, "devias", (204, 37)))
        self._go_to_coords((226, 40))

        # click on npc 225, 41
        time.sleep(1)
        offset = walking_vector.coords_to_pixel_offset(self.coords, (225, 41))
        window_pixel = (ORIGIN[0] + offset[0], ORIGIN[1] + offset[1])
        screen_pixel = window_api.window_pixel_to_screen_pixel(
            self._window.hwnd, *window_pixel
        )
        arduino_api.ard_mouse_to_pos(screen_pixel, sleep=True)
        arduino_api.click()
        time.sleep(3)

        # click on pots n times
        screen_pixel = window_api.window_pixel_to_screen_pixel(
            self._window.hwnd, 700, 120
        )
        arduino_api.ard_mouse_to_pos(screen_pixel, sleep=True)
        for _ in range(10):
            arduino_api.click(sleep=True)

        # close shop
        window_pixel = 960, 630
        screen_pixel = window_api.window_pixel_to_screen_pixel(
            self._window.hwnd, *window_pixel
        )
        arduino_api.ard_mouse_to_pos(screen_pixel, sleep=True)
        arduino_api.click(sleep=True)

    def distribute_stats(self) -> None:
        """If stats should be distributed, distribute them."""
        if not getattr(self, "_last_dist_lvl", 0):
            self._last_dist_lvl = self.lvl
        lvl = self.lvl
        if lvl == 1:
            logging.debug("Distributing stats after reset")
            stats = self._config["stats"]
            total = self.gr * 10 * 1000 + self.reset * 500
            for stat in stats:
                if stats[stat][0] == "f":
                    # distribute flat
                    to_add = int(stats[stat][1:])
                    total -= to_add
                    self._write_to_chat(f"/add{stat} {to_add}")
            self._distribute_relativety(total)

        step = 50 if self.reset < 15 else 100

        if self.lvl < self._last_dist_lvl:
            self._last_dist_lvl = 1
        if self.lvl > self._last_dist_lvl + step:
            logging.debug("Distributing stats during gameplay")
            total = (self.lvl - self._last_dist_lvl) * 6
            self._last_dist_lvl = lvl
            self._distribute_relativety(total)

    def ensure_on_best_spot(self):
        self._update_best_spot_index()
        spot = self._config["leveling_plan"][self._farming._farming_spot_index]
        map_name = "".join(i for i in spot["map"] if i.isalpha())
        if self._is_on_place(map_name, spot["coords"]):
            return

        # choose path
        map_arr = get_mu_map_list(map_name)
        target_coords: tuple = spot["coords"]
        curr_len = None
        curr_warp = None
        if self._in_map(map_name):
            with contextlib.suppress(TooManyIterationsException):
                path = djikstra8(self.coords, target_coords, map_arr)
                curr_len = len(path)
        for warp in MAP_DICT[map_name]:
            if warp.lvl > self.lvl:
                continue
            with contextlib.suppress(TooManyIterationsException):
                path = djikstra8(warp.coords, target_coords, map_arr)
                if not curr_len or len(path) < curr_len:
                    curr_len = len(path)
                    curr_warp = warp

        if not curr_len:
            return

        if curr_warp:
            self.warp(curr_warp)

        if self._go_to_coords(target_coords):
            logging.info("Player died while trying to get to the best spot")
            self.map = None
            self._exclude_current_spot()
            self.ensure_on_best_spot()
            return

        # check if spot is taken
        units = self._surrounding_units()
        my_coords = self.coords
        units = list(filter(lambda x: distance(x.coords, my_coords) < 6, units))
        players = get_online_players()
        with contextlib.suppress(ValueError):
            # [players.remove(ally) for ally in self._allies]
            players.remove(self.name)
        players_on_spot = [unit for unit in units if unit.name in players]
        if not players_on_spot:
            i = 0
            # count monsters
            while (
                i < len(units)
                and [unit.name for unit in units].count(units[i].name) < 6
                and self._farming._farming_spot_index
                and False
            ):
                i += 1
                if i == len(units):
                    spot = self._config["leveling_plan"][
                        self._farming._farming_spot_index
                    ]
                    logging.info(
                        f"Not enough mobs on spot: {spot['map']} - {spot['coords']}"
                    )
                    self._exclude_current_spot()
                    self.ensure_on_best_spot()
                    break
            # game_methods.kill_runaway_units()
            # self._go_to_coords(spot["coords"])
            return

        logging.info(f"Someone is here: {[{unit.name: unit.coords} for unit in units]}")
        self._exclude_current_spot()
        self.ensure_on_best_spot()

    def do_reset(self) -> bool:
        """Do reset if required level is met."""
        # first 10 resets
        level_needed = 400
        if self.gr == 0 and self.reset < 10:
            level_needed = 300 + 10 * self.reset
        logging.debug(f"level_needed: {level_needed}")
        logging.debug(f"self.lvl: {self.lvl}")

        if self.lvl < level_needed:
            return False

        game_menu.server_selection(self._window.hwnd)
        self._try_reset_on_web()
        time.sleep(2)
        meth.protection_click()
        window_api.window_activate_by_handler(self._window.hwnd)
        game_menu.game_login(
            self._window.hwnd,
            self._config["account"]["id"],
            self._config["account"]["pass"],
            self._config["account"]["select_offset"],
        )
        time.sleep(2)
        self.__init__(self.name)
        return True

    def farm(self):
        if not self._farming._farming_flag:
            self._farming._farming_flag = True
            self._farming._farming_coords = self.coords
        meth.turn_helper_on(self._window.hwnd)
        time.sleep(5)

    def check_death(self):
        """Check if died during farming."""
        if (
            self._farming._farming_flag
            and distance(self.coords, self._farming._farming_coords) > 13
        ):
            logging.info("Player died while farming")
            self._farming._farming_flag = False
            self._exclude_current_spot()
            self.ensure_on_best_spot()

    def check_lifetime(self) -> bool:
        """Return True if object lives too long."""
        lifespan = timedelta(hours=2)
        return datetime.now() - self.birthtime > lifespan

    def close_game(self):
        gw.Win32Window(hWnd=self._window.hwnd).close()
        time.sleep(0.5)
        arduino_api.send_ascii(KEY_RETURN)
        time.sleep(0.5)

    # PRIVATE METHODS

    def _in_map(self, map_name: str):
        if self.map == map_name:
            return True
        if self.map:
            return False
        template_path = os.path.join(
            os.path.dirname(__file__), f"patterns/{map_name}.png"
        )
        template = cv2.imread(template_path)
        bbox = 40, 30, 100, 15
        img = numpy.array(window_api.window_grab_image(self._window.hwnd, *bbox))
        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.9
        res = bool(numpy.where(res >= threshold)[0])
        if res:
            self.map = map_name
            return True
        return False

    def _distribute_relativety(self, stats_to_distribute: int) -> None:
        stats = self._config["stats"]
        parts = sum(int(stats[key][1:]) for key in stats if stats[key][0] == "r")

        for stat in stats:
            if stats[stat][0] == "r":
                to_add = int(int(stats[stat][1:]) * stats_to_distribute / parts)
                self._write_to_chat(f"/add{stat} {to_add}")

    def _try_reset_on_web(self) -> None:
        """Start browser and reset on web."""
        logging.info("Starting reset")
        if not getattr(self, "_last_reset_time", None):
            self._last_reset_time = 0
        self._last_reset_time = self._last_reset_time or 0
        if self._last_reset_time and datetime.now() - self._last_reset_time < timedelta(
            seconds=1200
        ):
            return

        account = self._config["account"]

        for _ in range(3):
            p = Process(
                target=do_reset_on_web,
                args=(account["id"], account["pass"], account["position"]),
            )
            p.start()
            p.join(30)
            if p.exitcode == 0:
                self._last_reset_time = datetime.now()
                return

        raise ResetError("Reset failed!")

    def _go_to_coords(self, target_coords: tuple):
        """Go to target coordinates on current map."""
        map_array = get_mu_map_list(self.map)
        path = djikstra8(self.coords, target_coords, map_array)

        while distance(self_coords := self.coords, path[-1]) > 3:
            closest_path_point_index = min(
                ((i, distance(self_coords, e)) for i, e in enumerate(path)),
                key=lambda x: x[1],
            )[0]
            try:
                next_point = path[closest_path_point_index + 4]
            except IndexError:
                next_point = path[-1]
            # self.go_direction(next_point)

            offset = walking_vector.coords_to_pixel_offset(self_coords, next_point)
            game_pixel = [ORIGIN[0] + offset[0], ORIGIN[1] + offset[1]]
            game_pixel[1] = min(game_pixel[1], 650)
            screen_pixel = window_api.window_pixel_to_screen_pixel(
                self._window.hwnd, *game_pixel
            )
            arduino_api.ard_mouse_to_pos(screen_pixel)
            arduino_api.hold_left()

            if _if_stucked(self_coords):
                offset = 0.6 * offset[0], 0.6 * offset[1]
                game_pixel = [ORIGIN[0] + offset[0], ORIGIN[1] + offset[1]]
                game_pixel[1] = min(game_pixel[1], 650)
                screen_pixel = window_api.window_pixel_to_screen_pixel(
                    self._window.hwnd, *game_pixel
                )
                arduino_api.ard_mouse_to_pos(screen_pixel)
                time.sleep(2)

            time.sleep(0.02)

        screen_pixel = window_api.window_pixel_to_screen_pixel(
            self._window.hwnd, *ORIGIN
        )
        arduino_api.ard_mouse_to_pos(screen_pixel)
        arduino_api.release_buttons()

    def _exclude_current_spot(self):
        del self._config["leveling_plan"][self._farming._farming_spot_index]
        self._farming._farming_spot_index -= 1

    def _write_to_chat(self, msg: str):
        arduino_api.send_ascii(KEY_RETURN)
        time.sleep(0.5)
        if not meth._detect_chat_open(self._window.hwnd):
            arduino_api.send_ascii(KEY_RETURN)
        time.sleep(0.5)
        if not meth._detect_chat_open(self._window.hwnd):
            raise ChatError("Cannot open chat!")
        arduino_api.send_string(msg)
        time.sleep(0.5)
        arduino_api.send_ascii(KEY_RETURN)
        time.sleep(0.5)
        if meth._detect_chat_open(self._window.hwnd):
            arduino_api.send_ascii(KEY_RETURN)
        time.sleep(0.5)
        if meth._detect_chat_open(self._window.hwnd):
            raise ChatError("Cannot close chat!")

    def _warp_to(self, area: str) -> None:
        self._write_to_chat(f"/warp {area}")
        time.sleep(3)

    def _surrounding_units(self) -> list:
        return memory.get_surrounding_units(self._window.id)

    def _is_on_place(self, map_name: str, coords: tuple) -> bool:
        """Check if player is on place."""
        ret = self._in_map(map_name) and distance(self.coords, coords) < 10
        if not ret:
            logging.info(
                f"Player, {self.map} {self.coords}, is not on place {map_name} {coords}"
            )
        return ret

    def _update_best_spot_index(self):
        leveling_plan = self._config["leveling_plan"]
        f_run = True
        while self._farming._farming_spot_index + 1 < len(leveling_plan) and f_run:
            spot = leveling_plan[self._farming._farming_spot_index + 1]
            f_run = False
            map_name = "".join(i for i in spot["map"] if i.isalpha())
            logging.debug(f"Checking better spot: {spot}")
            for warp in MAP_DICT[map_name]:
                if self.lvl < warp.lvl:
                    continue
                target_coords = spot["coords"]
                with contextlib.suppress(TooManyIterationsException):
                    djikstra8(warp.coords, target_coords, get_mu_map_list(warp.map))
                    self._farming._farming_spot_index += 1
                    f_run = True
                    break
            logging.debug(
                f"lvl: {self.lvl} is enough for spot {leveling_plan[self._farming._farming_spot_index]}"
            )
