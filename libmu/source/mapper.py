
from PIL import Image
from i_game import read_coords
import time


time.sleep(1)

img = Image.open(f'mapper.png')
idk = img.load()

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
