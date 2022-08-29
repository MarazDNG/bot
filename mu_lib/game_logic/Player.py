from threading import local
import requests
import re
import time
from cached_property import cached_property_with_ttl

from .reset import reset
from .reading import read_lvl, read_reset, read_coords
from .game_methods import _to_chat
from .exceptions import WarpException
from conf.stats import stats
from .spots import *
from mu_window import mu_window
from . import game_menu
from .game_methods import go_to
from mu_lib.game_logic import game_methods
from .meth import distance


class Player:

    def __init__(self):
        self.reset = read_reset()
        self._warp = "lorencia"
        self.stats = stats
        self.leveling_plan = [
            n_BUDGE_DRAGONS,
            n_WEREWOLVES,
            n_BLUE_GOLEMS,
        ]
        self.current_spot_index = 0
        self.farming = {
            "flag": False,
            "coords": None,
        }
        self.death_spots = set()

    @property
    def total_stats(self):
        return 20 * 1000 * self.gr + 500 * self.reset + 6 * (self.lvl - 1)

    @property
    def lvl(self):
        return read_lvl()

    @property
    def coords(self) -> tuple:
        return read_coords()

    @cached_property_with_ttl(ttl=12 * 60 * 60)
    def gr(self):
        resp = requests.get(
            "https://eternmu.cz/old/profile/player/req/Marshall/")
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
            def stadium_city():
                mu_window.press(ord("m"))
                time.sleep(0.5)
                mu_window.click_on_pixel((100, 115))

            def peaceswamp1():
                warp_to("peaceswamp")
                self._go_to_coords((139, 125))

            tmp = self.coords

            if warp in locals():
                locals()[warp]()
            else:
                _to_chat(f"/warp {warp}")
            time.sleep(3)

            if self.coords == tmp:
                raise WarpException("Warp failed")

        warp_to(value)
        self.warp = value

        # update flag
        self.farming["flag"] = False

    def distribute_stats(self) -> None:
        """If stats should be distributed, distribute them.
        """
        self.distribute_stats.last_lvl = getattr(
            self.distribute_stats, "last_lvl", 1)
        lvl = self.lvl

        if lvl == 1:
            total = self.gr * 10*1000 + self.reset * 500
            for stat in self.stats:
                if self.stats[stat][0] == "f":
                    to_add = int(self.stats[stat][1:])
                    total -= to_add
                    _to_chat(f"/add{stat} {to_add}")
            self._distribute_relativety(total)

        if self.reset < 15:
            if self.lvl < self.distribute_stats.last_lvl:
                self.distribute_stats.last_lvl = 1
            total += (self.lvl - self.distribute_stats.last_lvl) * 6
            self.distribute_stats.last_lvl = lvl
            self._distribute_relativety(total)

    def check_best_spot(self):
        """Go to best spot if not on it.
        """
        if self._is_on_best_spot():
            return
        self._go_to_best_spot()

    def try_reset(self) -> bool:
        """Do reset if required level is met.
        """
        # first 10 resets
        level_needed = 400
        if self.gr == 0 and self.reset < 10:
            level_needed = 300 + 10 * self.reset
        if self.lvl >= level_needed:
            game_menu.server_selection()
            self._reset()
            mu_window.activate_window()
            game_menu.game_login()
            time.sleep(2)
            self.__init__()
            return True
        return False

    def farm(self):
        if not self.farming["flag"]:
            self.farming["flag"] = True
            self.farming["coords"] = self.coords
        game_methods.start_helper()
        time.sleep(5)

    def check_death(self):
        if self.farming["flag"] and distance(self.coords, self.farming["coords"]) > 7:
            # we died
            self.farming["flag"] = False
            del self.leveling_plan[self.current_spot_index]
            self.current_spot_index -= 1
            self._go_to_best_spot()

    def _distribute_relativety(self, stats_to_distribute: int) -> None:
        parts = sum(int(self.stats[key][1:])
                    for key in self.stats if self.stats[key][0] == "r")

        for stat in self.stats:
            if self.stats[stat][0] == "r":
                to_add = int(int(self.stats[stat][1:])
                             * stats_to_distribute / parts)
                _to_chat(f"/add{stat} {to_add}")

    def _reset():
        reset()

    def _is_on_best_spot(self) -> bool:
        if self.current_spot_index + 1 == len(self.leveling_plan):
            return True
        return self.lvl < self.leveling_plan[self.current_spot_index + 1]["min_lvl"]

    def _go_to_best_spot(self):
        while not self._is_on_best_spot():
            self.current_spot_index += 1
        self.warp = self.leveling_plan[self.current_spot_index]["warp"]
        self._go_to_coords(
            self.leveling_plan[self.current_spot_index]["coords"])
        game_methods.kill_runaway_units()

    def _go_to_coords(self, coords: tuple):
        area = "".join(i for i in self.warp if i.isalpha())
        game_methods.go_to(coords, area)
