import numpy as np
import cv2
class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Sensor:
    def __init__(self, k1, k2, width, height):
        self.k1 = k1
        self.k2 = k2
        self.width = width
        self.height = height
        self.mask = np.zeros((height, width, 1), np.uint8)
        self.maskArea = abs(self.k2.x - self.k1.x) * abs(self.k2.y - self.k1.y)
        cv2.rectangle(self.mask, (self.k1.x, self.k1.y), (self.k2.x, self.k2.y), 255, -1)
        self.situation = False
        self.carCount = -1

