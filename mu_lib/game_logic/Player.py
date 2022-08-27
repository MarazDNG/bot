from .reading import read_lvl, read_reset
import requests
import re
from cached_property import cached_property_with_ttl


from .reset import reset
from .reading import read_coords
from .game_methods import _to_chat
from conf.stats import stats


class Player:

    def __init__(self):
        self.reset = read_reset()
        self.map = None
        self.stats = stats

    @property
    def total_stats(self):
        return 20 * 1000 * self.gr + 500 * self.reset + 6 * (self.lvl - 1)

    def _distribute_relativety(self, stats_to_distribute: int) -> None:
        parts = sum(int(self.stats[key][1:])
                    for key in self.stats if self.stats[key][0] == "r")

        for stat in self.stats:
            if self.stats[stat][0] == "r":
                to_add = int(int(self.stats[stat][1:])
                             * stats_to_distribute / parts)
                _to_chat(f"/add{stat} {to_add}")

    def distribute_stats(self) -> None:
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

    def _reset():
        reset()

    def try_reset(self):
        # first 10 resets
        level_needed = 400
        if self.gr == 0 and self.reset < 10:
            level_needed = 300 + 10 * self.reset
        if self.lvl >= level_needed:
            self._reset()
