
from scripts import activate_window
from PIL import Image
from game_methods.game_methods import read_coords
import sys


if len(sys.argv) != 2:
    raise Exception("Please provide a map name as an argument!")

try:
    img = Image.open(sys.argv[1])
except:
    raise Exception("Could not open image!")
idk = img.load()

activate_window()

coords_set = set()
while True:
    coords = read_coords()
    if not coords:
        break
    coords_set.add(coords)

for i in coords_set:
    idk[
        i[0], i[1]
    ] = (255, 255, 255)

img.save(f'mapper.png')
