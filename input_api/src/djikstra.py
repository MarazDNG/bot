#
# Djikstra algorithm
#


from PIL import Image


DIFF = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]


class Map:

    def __init__(self, mapa):
        self.mapa = mapa

    def spot(self, pos):
        x, y = pos
        return self.mapa[x][y]


class Spot:

    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

    def pos(self):
        return (self.x, self.y)


def get_surrounding(x, y):

    l = []
    for dx, dy in DIFF:
        l.append((x+dx, y+dy))
    return l


def fill_map(area):
    img = Image.open(f'img/img_{area}.png')
    filling = img.load()
    a_map = []
    width, height = img.size()
    for i in range(width):
        row = []
        for j in range(height):
            if filling[i, j] == (255, 255, 255):
                row.append('Y')
            else:
                row.append('N')
        a_map.append(row)
    # print(counter)
    # Convert list or true/false into list of objects
    for i, row in enumerate(a_map):
        for j, col in enumerate(row):
            a_map[i][j] = Spot(i, j, a_map[i][j])
    a_map = Map(a_map)
    return a_map


def djikstra(start, goal, area):

    mapa = fill_map(area)

    mapa.spot(start).value = 's'
    mapa.spot(goal).value = 'g'

    # List of indices of spots - current layer X
    current = [mapa.spot(start)]

    # List of indices of spots that should be assigned a numebr. X
    distance = 1

    def filter_used(haystack, bucket):
        for index in haystack:
            if mapa.spot(index).value in ['Y', 'g'] and mapa.spot(index) not in bucket:
                bucket.append(mapa.spot(index))
    while True:
        new_layer = []
        for item in current:
            indices = get_surrounding(*item.pos())  # [(x, y),]
            filter_used(indices, new_layer)

        def find_g(haystack):
            for item in haystack:
                if item.value == 'g':
                    return item.pos()
            return 0
        if find_g(new_layer):
            #print("OMG MOREEE!")
            break
        for item in new_layer:
            item.value = distance
        distance += 1
        current = new_layer.copy()
        new_layer = []
    distance -= 1

    place = mapa.spot(goal)
    path = []

    while True:
        neighbors = get_surrounding(*place.pos())
        neighbors = [mapa.spot(i) for i in neighbors if mapa.spot(
            i).value in [distance, 's']]
        if len(neighbors) == 0:
            print("FCK!")
            break
        next_point = neighbors[0]
        path.append(next_point.pos())
        if next_point.value == 's':
            #print("FOUND IT!")
            break
        place = next_point
        distance -= 1
    path.reverse()
    return path


def djikstra4(start, goal, area):

    mapa = fill_map(area)
    mapa.spot(start).value = 's'
    mapa.spot(goal).value = 'g'

    current = [start]
    distance = 0

    while len(current):
        next_layer = set()
        for item in current:
            x, y = item
            next_layer.add((x+1, y))
            next_layer.add((x, y+1))
            next_layer.add((x-1, y))
            next_layer.add((x, y-1))

        distance += 1
        if goal in next_layer:
            break

        next_layer = [i for i in next_layer if mapa.spot(i).value == 'Y']
        for i in next_layer:
            mapa.spot(i).value = distance
        current = next_layer.copy()

    distance -= 1

    path = [goal]
    x, y = goal
    while distance:
        neighbors = set()
        neighbors.add((x+1, y))
        neighbors.add((x, y+1))
        neighbors.add((x-1, y))
        neighbors.add((x, y-1))
        for i in neighbors:
            if mapa.spot(i).value == distance:
                path.append(i)
                x, y = i
                break
        distance -= 1
    path.reverse()

    return path
