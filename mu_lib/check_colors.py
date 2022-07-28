from PIL import Image
import numpy as np

m = "elbeland"
path = f"game_methods/maps/img_{m}.png"

img = Image.open(path)
img = np.asarray(img)

s = set()

WHITE_COLOR = (255, 255, 255)
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        s.add(tuple(img[i][j]))

print(s)
