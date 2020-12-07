import cv2
import numpy as np
import sys


def generateTileSet():
    img = cv2.imread('./videoImage/000000.jpg')

    # Create an empth list to store candidates
    tileSet = []

    # Initialize candidate
    tilCandidate = np.zeros((55, 5, 3), np.uint8)

    for x in range(125, 167, 2):
        for y in range(15, 255, 2):
            tilCandidate = img[x:x + 55, y:y + 5]
            tileSet.append(tilCandidate)

    return tileSet

tileSet = generateTileSet()



