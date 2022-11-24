from game_logic import Player

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
p = Player.Player("Connie")

coords_set = set()
while True:
    coords = p.coords
    if coords == (25, 27):
        break
    print(coords)
    coords_set.add(coords)

for i in coords_set:
    idk[i[0], i[1]] = (255, 255, 255)
img.save("mapper.png")
