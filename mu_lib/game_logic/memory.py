from platform import processor
from ReadWriteMemory import ReadWriteMemory
from dataclasses import dataclass


@dataclass
class Unit:
    """ NPC with name, x, y.
    """
    name: str
    x: int
    y: int


process_name = "main.exe"
base_addr = 0x00400000


def surrounding_units() -> list[Unit]:

    d0 = 0x00A7A224
    d1 = 0x8
    d2 = 0x38
    size = 1432
    rwm = ReadWriteMemory()
    process = rwm.get_process_by_name(process_name)
    process.open()

    p = process.get_pointer(base_addr + d0, offsets=[d1, d2])

    units = []
    for _ in range(6):
        name = process.readString(p, 2000)
        x = process.read(p + 0x74)
        y = process.read(p + 0x78)
        units.append(Unit(name, x, y))
        p += size

    process.close()
    return units


def my_coords() -> tuple:

    dx = 0x7dbe38C
    dy = 0x7dbe388

    rwm = ReadWriteMemory()
    process = rwm.get_process_by_name(process_name)
    print(process)
    process.open()

    x = process.read(base_addr + dx)
    y = process.read(base_addr + dy)

    process.close()
    return x, y
