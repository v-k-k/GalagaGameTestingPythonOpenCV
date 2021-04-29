from collections import namedtuple


Area = namedtuple("Area", "min, max")
Filters = namedtuple("Filters", "AREA, CIRCULARITY, CONVEXITY, INERTIA")
Coordinates = namedtuple("Coordinates", "x_coord, y_coord")
Image = namedtuple("Image", "original, threshold")
Canvas = namedtuple("Canvas", "image, grey_image")
Keypoints = namedtuple("Keypoints", "player, enemy, missile")
