"""
Watch coordinates and lvl of players.
Beep when player dies or reaches lvl 400.
"""
import window_api
import winsound
import re

from game_logic import memory
from game_logic.meth import distance


titles = []
titles.append("DINO")
# titles.append("krtecek")

ids = [window_api.window_id_by_title(title) for title in titles]
id_coords = {id: memory.my_coords(id) for id in ids}

def beep():
    winsound.Beep(2000, 1000)
        
def has_400(i):
    window_title = window_api.window_title_by_title(titles[i])
    lvl_str = re.search("Level: \d+", window_title)[0]
    return int(lvl_str.split()[1]) == 400

while True:
    for i, id in enumerate(ids):
        coords = memory.my_coords(id)
        if distance(memory.my_coords(id), id_coords[id]) > 6:
            print(f"Player {titles[i]} moved.")
            beep()
        if has_400(i):
            print(f"Player {titles[i]} is 400.")
            beep()