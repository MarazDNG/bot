
from mu_window.mu_window import activate_window, window_id_by_title
from game_logic.reading import read_coords

from PIL import Image
import sys

if len(sys.argv) != 2:
    raise Exception("Please provide a map name as an argument!")

try:
    if sys.argv[1] == "--new":
        img = Image.open("input.png")
    else:
        img = Image.open(sys.argv[1])
except:
    raise Exception("Could not open image!")
idk = img.load()

# activate_window("Silco")
win_id = window_id_by_title("Silco")

coords_set = set()
while True:
    coords = read_coords(win_id)
    if coords == (25, 27):
        break
    print(coords)
    coords_set.add(coords)

for i in coords_set:
    idk[
        i[0], i[1]
    ] = (255, 255, 255)
img.save('mapper.png')
