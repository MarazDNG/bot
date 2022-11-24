from ReadWriteMemory import ReadWriteMemory
from dataclasses import dataclass
from pprint import pprint


class NotEnoughMobsException(Exception):
    pass


@dataclass
class Unit:
    """
    NPC with name, x, y.
    """

    name: str
    coords: tuple


# process_name = "main.exe"
base_addr = 0x00400000


def _distance(x1, y1, x2, y2) -> float:
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def get_surrounding_units(id: int):
    """Return surrounding units sorted closest first."""
    d0 = 0x00A7A224
    d1 = 0x8
    d2 = 0x38
    size = 1432
    rwm = ReadWriteMemory()
    process = rwm.get_process_by_id(id)
    process.open()

    p = process.get_pointer(base_addr + d0, offsets=[d1, d2])

    units = []
    while (name := process.readString(p, 2000)) != "":
        x = process.read(p + 0x74)
        y = process.read(p + 0x78)
        units.append(Unit(name, (x, y)))
        p += size

    units.sort(key=lambda unit: _distance(*unit.coords, *my_coords(id)))
    process.close()
    return units


def surrounding_units(id: int) -> list[Unit]:
    """Return 6 closest same units."""
    d0 = 0x00A7A224
    d1 = 0x8
    d2 = 0x38
    size = 1432
    rwm = ReadWriteMemory()
    process = rwm.get_process_by_id(id)
    process.open()

    p = process.get_pointer(base_addr + d0, offsets=[d1, d2])

    units = []
    while (name := process.readString(p, 2000)) != "":
        x = process.read(p + 0x74)
        y = process.read(p + 0x78)
        units.append(Unit(name, (x, y)))
        p += size

    units.sort(key=lambda unit: _distance(*unit.coords, *my_coords(id)))

    i = 0
    # count monsters
    while [unit.name for unit in units].count(units[i].name) < 6:
        i += 1
        if i > 5:
            raise NotEnoughMobsException("Not enough mobs")

    monster_name = units[i].name
    units = list(filter(lambda unit: unit.name == monster_name, units))

    units = units[:6]
    process.close()

    return units


def my_coords(id: int) -> tuple:

    d0 = 0x077C2F04
    dx = 0xAC
    rwm = ReadWriteMemory()
    process = rwm.get_process_by_id(id)
    process.open()

    p = process.get_pointer(base_addr + d0, offsets=[dx])

    x = process.read(p)
    y = process.read(p + 0x4)

    process.close()
    return x, y
