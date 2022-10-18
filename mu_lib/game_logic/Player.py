import contextlib
import logging
import requests
import re
import time
from cached_property import cached_property_with_ttl
import logging
from multiprocessing import Process
from datetime import datetime, timedelta

import window_api
import arduino_api

from . import memory
from . import meth
from . import KEY_RETURN, ORIGIN
from . import game_menu
from . import walking_vector

from .exceptions import DeathException, WarpException, ResetError, ChatError
from .meth import distance, get_online_players, _if_stucked
from .browser import do_reset
from .map import get_mu_map_list
from .djikstra import djikstra8
from conf.stats import config


class Player:

    def __init__(self, char_name: str):
        self.name = char_name
        self.config = config[char_name]
        self.name = char_name
        self._window_id = None
        self._hwnd = None
        self.allies = []
        self._warp = "lorencia"
        self.stats = self.config["stats"]
        self.leveling_plan = self.config["leveling_plan"]
        self._last_dist_lvl = None
        self.farming_spot_index = 0
        self.farming = {
            "flag": False,
            "coords": None,
        }
        self._time_last_reset = None
        logging.info(f"Initialized player {self.name}")
        self.birthtime = datetime.now()

    # PROPS
    @property
    def hwnd(self):
        if not self._hwnd:
            self._hwnd = window_api.window_handler_by_title(self.name)
        return self._hwnd

    @property
    def last_dist_lvl(self):
        if self._last_dist_lvl is None:
            self._last_dist_lvl = self.lvl
        return self._last_dist_lvl

    @last_dist_lvl.setter
    def last_dist_lvl(self, value):
        self._last_dist_lvl = value

    @property
    def window_id(self):
        if self._window_id is None:
            self._window_id = window_api.window_id_by_title(self.name)
        return self._window_id

    @property
    def reset(self) -> int:
        window_title = window_api.window_title_by_handler(self.hwnd)
        reset_str = re.search("Reset: \d+", window_title)[0]
        return int(reset_str.split()[1])

    @property
    def lvl(self):
        window_title = window_api.window_title_by_handler(self.hwnd)
        lvl_str = re.search("Level: \d+", window_title)[0]
        return int(lvl_str.split()[1])

    @property
    def coords(self) -> tuple:
        return memory.my_coords(self.window_id)

    @cached_property_with_ttl(ttl=12 * 60 * 60)
    def gr(self):
        resp = requests.get(
            f"https://eternmu.cz/profile/player/req/{self.name}/", verify=False)
        gr_str = re.search("Grand resety</td><td>\d+", resp.text)[0]
        return int(gr_str.split("</td><td>")[1])

    @property
    def warp(self):
        return self._warp

    @warp.setter
    def warp(self, value: str):
        def warp_to(warp: str) -> None:
            """Used only when required level is met.
            """
            def peaceswamp1():
                self.warp = "peaceswamp"
                self.go_to_coords((139, 125))

            tmp = self.coords

            if warp in locals():
                locals()[warp]()
            else:
                self._write_to_chat(f"/warp {warp}")
            time.sleep(3)

            if distance(self.coords, tmp) < 5 and self.lvl > 10:
                if warp in locals():
                    locals()[warp]()
                else:
                    self._write_to_chat(f"/warp {warp}")
                time.sleep(3)
                if distance(self.coords, tmp) < 5 and self.lvl > 10:
                    raise WarpException(
                        f"Warp failed from {self.warp} {self.coords} to {warp}")

        warp_to(value)
        self._warp = value

        # update flag
        self.farming["flag"] = False

    # PUBLIC METHODS
    def surrounding_units(self) -> list:
        return memory.get_surrounding_units(self.window_id)

    def distribute_stats(self) -> None:
        """If stats should be distributed, distribute them.
        """
        lvl = self.lvl

        if lvl == 1:
            total = self.gr * 10*1000 + self.reset * 500
            for stat in self.stats:
                if self.stats[stat][0] == "f":
                    # distribute flat
                    to_add = int(self.stats[stat][1:])
                    total -= to_add
                    self._write_to_chat(f"/add{stat} {to_add}")
            self._distribute_relativety(total)

        step = 50 if self.reset < 15 else 100

        if self.lvl < self.last_dist_lvl:
            self.last_dist_lvl = 1
        if self.lvl > self.last_dist_lvl + step:
            total = (self.lvl - self.last_dist_lvl) * 6
            self.last_dist_lvl = lvl
            self._distribute_relativety(total)

    def _is_on_place(self, warp: str, coords: tuple) -> bool:
        """Check if player is on place.
        """
        ret = self.warp == warp and distance(self.coords, coords) < 10
        if not ret:
            logging.info(
                f"Player, {self.warp} {self.coords}, is not on place {warp} {coords}")
        return ret

    def _update_best_spot_index(self):
        while self.farming_spot_index + 1 < len(self.leveling_plan) and self.lvl >= self.leveling_plan[self.farming_spot_index + 1]["min_lvl"]:
            print(
                f"lvl: {self.lvl} is enough for spot {self.leveling_plan[self.farming_spot_index + 1]}")
            self.farming_spot_index += 1

    def ensure_on_best_spot(self, prefer_warp: bool = True):
        self._update_best_spot_index()
        spot = self.leveling_plan[self.farming_spot_index]
        if not self._is_on_place(spot["warp"], spot["coords"]):
            if self.warp != spot["warp"] or prefer_warp:
                self.warp = spot["warp"]
            if self.go_to_coords(spot["coords"]):
                logging.info(
                    "Player died while trying to get to the best spot")
                self._exclude_current_spot()
                self.ensure_on_best_spot()
                return
            units = self.surrounding_units()
            my_coords = self.coords
            units = filter(lambda x: distance(
                x.coords, my_coords) < 10, units)
            players = get_online_players()
            with contextlib.suppress(ValueError):
                [players.remove(ally) for ally in self.allies]
                players.remove(self.name)
            if units := [unit for unit in units if unit.name in players]:
                logging.info(
                    f"Someone is here: {[{unit.name: unit.coords} for unit in units]}")

                self._exclude_current_spot()
                self.ensure_on_best_spot(prefer_warp=False)
                return
            # game_methods.kill_runaway_units()
            self.go_to_coords(spot["coords"])

    def try_reset(self) -> bool:
        """Do reset if required level is met.
        """
        # first 10 resets
        level_needed = 400
        if self.gr == 0 and self.reset < 10:
            level_needed = 300 + 10 * self.reset
        logging.info(f"level_needed: {level_needed}")
        logging.info(f"self.lvl: {self.lvl}")
        if self.lvl >= level_needed:
            game_menu.server_selection(self.hwnd)
            self._reset(self.config["account"]["id"],
                        self.config["account"]["pass"])
            window_api.window_activate(self.name)
            game_menu.game_login(self.hwnd,
                                 self.config["account"]["id"], self.config["account"]["pass"], self.config["account"]["select_offset"])
            time.sleep(2)
            self.__init__(self.name)
            return True
        return False

    def farm(self):
        if not self.farming["flag"]:
            self.farming["flag"] = True
            self.farming["coords"] = self.coords
        meth.turn_helper_on(self.hwnd)
        time.sleep(5)

    def check_death(self):
        """
        Check if died during farming.
        """
        if self.farming["flag"] and distance(self.coords, self.farming["coords"]) > 13:
            logging.info("Player died while farming")
            self.farming["flag"] = False
            self._exclude_current_spot()
            self.ensure_on_best_spot()

    def check_lifetime(self) -> bool:
        """Return True if object lives too long.
        """
        lifespan = timedelta(hours=2)
        return datetime.now() - self.birthtime > lifespan

    def _distribute_relativety(self, stats_to_distribute: int) -> None:
        parts = sum(int(self.stats[key][1:])
                    for key in self.stats if self.stats[key][0] == "r")

        for stat in self.stats:
            if self.stats[stat][0] == "r":
                to_add = int(int(self.stats[stat][1:])
                             * stats_to_distribute / parts)
                self._write_to_chat(f"/add{stat} {to_add}")

    def _reset(self, id: str, password: str) -> None:
        logging.info("Starting reset")
        self._time_last_reset = self._time_last_reset or 0
        if self._time_last_reset and datetime.now() - self._time_last_reset < timedelta(seconds=1200):
            return

        for _ in range(3):
            p = Process(target=do_reset, args=(id, password))
            p.start()
            p.join(30)
            if p.exitcode == 0:
                self._time_last_reset = datetime.now()
                return

        raise ResetError("Reset failed!")

    def go_to_coords2(self, target_coords: tuple):
        """Go to target coordinates on current map.
        """
        map_name = "".join(i for i in self.warp if i.isalpha())
        map_array = get_mu_map_list(map_name)
        path = djikstra8(self.coords, target_coords, map_array)

        while distance(self_coords := self.coords, path[-1]) > 5:
            stucked = _if_stucked(self_coords)
            closest_path_point_index = min(
                ((i, distance(self_coords, e)) for i, e in enumerate(path)), key=lambda x: x[1])[0]
            try:
                next_point = path[closest_path_point_index + 5]
            except IndexError:
                next_point = path[-1]
            pixel_offset = walking_vector.go_next_point(
                self_coords, next_point)
            if stucked:
                pixel_offset = int(
                    pixel_offset[0] * 1.5), int(pixel_offset[1] * 1.5)
            game_pixel = ORIGIN[0] + \
                pixel_offset[0], ORIGIN[1] + pixel_offset[1]
            screen_pixel = window_api.window_pixel_to_screen_pixel(
                self.hwnd, *game_pixel)
            arduino_api.ard_mouse_to_pos(screen_pixel)
            arduino_api.hold_left()
            if stucked:
                time.sleep(2)
            time.sleep(0.02)

        screen_pixel = window_api.window_pixel_to_screen_pixel(
            self.hwnd, *ORIGIN)
        arduino_api.ard_mouse_to_pos(screen_pixel)
        arduino_api.release_buttons()

    def go_to_coords(self, target_coords: tuple):
        """Go to target coordinates on current map.
        """
        map_name = "".join(i for i in self.warp if i.isalpha())
        map_array = get_mu_map_list(map_name)
        path = djikstra8(self.coords, target_coords, map_array)

        while distance(self_coords := self.coords, path[-1]) > 3:
            closest_path_point_index = min(
                ((i, distance(self_coords, e)) for i, e in enumerate(path)), key=lambda x: x[1])[0]
            try:
                next_point = path[closest_path_point_index + 4]
            except IndexError:
                next_point = path[-1]
            # self.go_direction(next_point)
            offset = walking_vector.coords_to_pixel_offset(
                self_coords, next_point)
            game_pixel = [ORIGIN[0] + offset[0], ORIGIN[1] + offset[1]]
            game_pixel[1] = min(game_pixel[1], 650)
            screen_pixel = window_api.window_pixel_to_screen_pixel(
                self.hwnd, *game_pixel)
            arduino_api.ard_mouse_to_pos(screen_pixel)
            arduino_api.hold_left()
            if diff := _if_stucked(self_coords):
                offset = 0.6 * offset[0], 0.6 * offset[1]
                game_pixel = [ORIGIN[0] + offset[0], ORIGIN[1] + offset[1]]
                game_pixel[1] = min(game_pixel[1], 650)
                screen_pixel = window_api.window_pixel_to_screen_pixel(
                    self.hwnd, *game_pixel)
                arduino_api.ard_mouse_to_pos(screen_pixel)
                time.sleep(2)

            #     else:
            #         self.warp = self.warp
            #         path = djikstra8(self.coords, target_coords, map_array)

            time.sleep(0.02)

        screen_pixel = window_api.window_pixel_to_screen_pixel(
            self.hwnd, *ORIGIN)
        arduino_api.ard_mouse_to_pos(screen_pixel)
        arduino_api.release_buttons()

    def go_direction(self, target_coords: tuple) -> None:
        screen_pixel = window_api.window_pixel_to_screen_pixel(
            self.hwnd, *ORIGIN)
        arduino_api.ard_mouse_to_pos(screen_pixel)

        while distance(self_coords := self.coords, target_coords) > 2:
            stucked = _if_stucked(self_coords)
            pixel_offset = walking_vector.go_next_point(
                self_coords, target_coords)
            with contextlib.suppress(ValueError):
                if stucked:
                    pixel_offset = int(
                        pixel_offset[0] * 1.5), int(pixel_offset[1] * 1.5)
            game_pixel = ORIGIN[0] + \
                pixel_offset[0], ORIGIN[1] + pixel_offset[1]
            screen_pixel = window_api.window_pixel_to_screen_pixel(
                self.hwnd, *game_pixel)
            arduino_api.ard_mouse_to_pos(screen_pixel)
            arduino_api.hold_left()
            if stucked:
                time.sleep(2)
            time.sleep(0.02)

    # PRIVATE METHODS

    def _exclude_current_spot(self):
        del self.leveling_plan[self.farming_spot_index]
        self.farming_spot_index -= 1

    def _write_to_chat(self, msg: str):
        arduino_api.send_ascii(KEY_RETURN)
        time.sleep(0.5)
        if not meth._detect_chat_open(self.hwnd):
            arduino_api.send_ascii(KEY_RETURN)
        time.sleep(0.5)
        if not meth._detect_chat_open(self.hwnd):
            raise ChatError("Cannot open chat!")
        arduino_api.send_string(msg)
        time.sleep(0.5)
        arduino_api.send_ascii(KEY_RETURN)
        time.sleep(0.5)
        if meth._detect_chat_open(self.hwnd):
            arduino_api.send_ascii(KEY_RETURN)
        time.sleep(0.5)
        if meth._detect_chat_open(self.hwnd):
            raise ChatError("Cannot close chat!")

    def _warp_to(self, area: str) -> None:
        self._write_to_chat(f'/warp {area}')
        time.sleep(3)

    def _buy_pots(self):
        if meth._detect_pots(self.hwnd):
            return

        self.warp = "devias"
        self.go_to_coords((226, 40))

        # click on npc 225, 41
        time.sleep(1)
        offset = walking_vector.coords_to_pixel_offset(self.coords, (225, 41))
        total = (ORIGIN[0] + offset[0], ORIGIN[1] + offset[1])
        arduino_api.ard_mouse_to_pos(
            window_api.window_pixel_to_screen_pixel(self.hwnd, *total))
        time.sleep(0.5)
        arduino_api.click()
        time.sleep(3)

        arduino_api.ard_mouse_to_pos(
            window_api.window_pixel_to_screen_pixel(self.hwnd, 700, 120))
        for _ in range(10):
            time.sleep(0.5)
            arduino_api.click()
        time.sleep(0.5)

        # close shop
        game_pixel = 960, 630
        total = window_api.window_pixel_to_screen_pixel(self.hwnd, *game_pixel)
        arduino_api.ard_mouse_to_pos(total)
        time.sleep(0.5)
        arduino_api.click()
        time.sleep(0.5)
