import cv2
import glob
import numpy as np
import sys

def developTextMask(frame_HSVImg):

    frame_height = frame_HSVImg.shape[0]  # 240

    # Initialize kernel for morphological operations
    kernel = np.ones((3,3), np.uint8)

    # Set color boundary for text
    red_LB = np.array([0,0,0])
    red_UB = np.array([25,255,255])


    mask_base = cv2.inRange(frame_HSVImg, red_LB, red_UB)
    mask_erode = cv2.erode(mask_base, kernel, iterations=1)
    mask_dilate = cv2.dilate(mask_erode, kernel, iterations=5)

    # Isolate the text
    for x in range(0, 64, 1):
        mask_dilate[x] = np.zeros(mask_dilate[x].shape[0])

    for y in range(220, frame_height, 1):
        mask_dilate[y] = np.zeros(mask_dilate[y].shape[0])

    return mask_dilate


def getTextSize(mask_dilated):

    text = np.where(mask_dilated == 255)

    rmax = np.max(text[0]) # rmax = 127
    rmin = np.min(text[0]) # rmin = 68
    mask_height = rmax - rmin # height = 59

    cmax = np.max(text[1]) # cmax = 292
    cmin = np.min(text[1]) # cmin = 53

    return mask_height, rmax, rmin, cmax, cmin