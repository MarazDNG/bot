import logging
import requests
import re
import time
from cached_property import cached_property_with_ttl
import logging


from .reset import reset
from .reading import read_lvl, read_reset, read_coords, surrounding_units
from .game_methods import _to_chat
from .exceptions import DeathException, WarpException
from conf.stats import config
from mu_window import mu_window
from . import game_menu
from . import game_methods
from .meth import distance, get_online_players


class Player:

    def __init__(self, char_name: str):
        self.name = char_name
        self.config = config[char_name]
        self.name = char_name
        self.window_id = mu_window.window_id_by_title(char_name)
        self.allies = []
        self.reset = read_reset()
        self._warp = "lorencia"
        self.stats = self.config["stats"]
        self.leveling_plan = self.config["leveling_plan"]
        self.last_dist_lvl = 1
        self.farming_spot_index = 0
        self.farming = {
            "flag": False,
            "coords": None,
        }
        logging.info(f"Initialized player {self.name}")

    @property
    def lvl(self):
        return read_lvl()

    @property
    def coords(self) -> tuple:
        return read_coords(self.window_id)

    @cached_property_with_ttl(ttl=12 * 60 * 60)
    def gr(self):
        return 0
        resp = requests.get(
            f"https://eternmu.cz/profile/player/req/{self.name}/")
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
                warp_to("peaceswamp")
                self._go_to_coords((139, 125))

            tmp = self.coords

            if warp in locals():
                locals()[warp]()
            else:
                _to_chat(f"/warp {warp}")
            time.sleep(3)

            if self.coords == tmp and self.lvl > 10:
                raise WarpException(
                    f"Warp failed from {self.warp} {self.coords} to {warp}")

        warp_to(value)
        self._warp = value

        # update flag
        self.farming["flag"] = False

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
                    _to_chat(f"/add{stat} {to_add}")
            self._distribute_relativety(total)

        if self.reset < 15:
            if self.lvl < self.last_dist_lvl:
                self.last_dist_lvl = 1
            if self.lvl > self.last_dist_lvl + 50:
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

    def ensure_on_best_spot(self):
        self._update_best_spot_index()
        spot = self.leveling_plan[self.farming_spot_index]
        if not self._is_on_place(spot["warp"], spot["coords"]):
            self.warp = spot["warp"]
            try:
                self._go_to_coords(spot["coords"])
                units = surrounding_units(self.window_id)
                my_coords = self.coords
                units = filter(lambda x: distance(
                    x.coords, my_coords) < 10, units)
                players = get_online_players()
                [players.remove(ally) for ally in self.allies]
                if units := [unit for unit in units if unit.name in players]:
                    logging.info(
                        f"Someone is here: {[{unit.name: unit.coords} for unit in units]}")

                    self._exclude_current_spot()
                    self.ensure_on_best_spot()
                    return
                game_methods.kill_runaway_units()
                self._go_to_coords(spot["coords"])
            except DeathException as e:
                logging.info(
                    "Player died while trying to get to the best spot")
                self._exclude_current_spot()
                self.ensure_on_best_spot()

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
            game_menu.server_selection()
            self._reset(self.config["account"]["id"],
                        self.config["account"]["pass"])
            mu_window.activate_window(self.name)
            game_menu.game_login()
            time.sleep(2)
            self.__init__(self.name)
            return True
        return False

    def farm(self):
        if not self.farming["flag"]:
            self.farming["flag"] = True
            self.farming["coords"] = self.coords
        game_methods.turn_helper_on()
        time.sleep(5)

    def check_death(self):
        """
        Check if died during farming.
        """
        if self.farming["flag"] and distance(self.coords, self.farming["coords"]) > 13:
            logging.info("Player died while farming")
            self.farming["flag"] = False
            del self.leveling_plan[self.farming_spot_index]
            self.farming_spot_index -= 1
            self.ensure_on_best_spot()

    def _distribute_relativety(self, stats_to_distribute: int) -> None:
        parts = sum(int(self.stats[key][1:])
                    for key in self.stats if self.stats[key][0] == "r")

        for stat in self.stats:
            if self.stats[stat][0] == "r":
                to_add = int(int(self.stats[stat][1:])
                             * stats_to_distribute / parts)
                _to_chat(f"/add{stat} {to_add}")

    def _reset(self, id: str, password: str) -> None:
        logging.info("Starting reset")
        reset(id, password)

    def _go_to_coords(self, coords: tuple):
        area = "".join(i for i in self.warp if i.isalpha())
        game_methods.go_to(coords, area)

    def _exclude_current_spot(self):
        del self.leveling_plan[self.farming_spot_index]
        self.farming_spot_index -= 1
