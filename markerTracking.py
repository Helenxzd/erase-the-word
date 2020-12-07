import cv2
import glob
import numpy as np
import sys
import getTextBound

img = cv2.imread('./videoImage/000000.jpg')
mask_Text = getTextBound.developTextMask(img)
height, rmax, rmin, cmax, cmin = getTextBound.getTextSize(mask_Text)

def generateTileSet(height, rmax, cmax, cmin):
    img = cv2.imread('./videoImage/000000.jpg')

    # Create an empth list to store candidates
    tileSet = []

    # Initialize candidate
    tilCandidate = np.zeros((55, 5, 3), np.uint8)

    for x in range(rmax, rmax + 40, 2):
        for y in range(cmin, cmax, 2):
            tilCandidate = img[x:x + height, y:y + 5]
            tileSet.append(tilCandidate)

    return tileSet

def findCandidate(img, curW, tileSet, height):
    # bottom
    # currentPatch = img[125:180, curW:curW + 5]
    # right
    # currentPatch = img[70:125, curW+5:curW + 10]
    # top
    # currentPatch = img[25:80, curW+5:curW+10]
    # currentPatchBottom = img[125:180, curW:curW + 5]
    # currentPatchRight = img[70:125, curW + 5:curW + 10]

    rightmost = 180
    currentPatch = img[rightmost - height:rightmost, curW:curW + 5]

    min_ssd = sys.maxsize
    index = -1
    for i in range(len(tileSet)):

        ssd = np.sum(np.square(currentPatch - tileSet[i]))
        if ssd < min_ssd:
            min_ssd = ssd
            index = i

    return index

def tracking(frames, tileSet, mode = "ssd"):
    search_range = 10
    # [boxh, boxw, bh, bw] = [25, 50, 40, 40]
    # initial bounding box
    [boxh, boxw, bh, bw] = [0, 276, 50, 13]
    fst_src = cv2.imread(frames[0])
    last_frame = fst_src
    fst_img = cv2.cvtColor(fst_src, cv2.COLOR_RGB2GRAY)
    last_roi = fst_img[boxh:boxh + bh, boxw:boxw + bw]
    cv2.rectangle(fst_src, (boxw, boxh), (boxw + bw, boxh + bh), (0, 255, 0), 1)
    # cv2.imshow("fst",fst_src)
    # cv2.waitKey(0)
    fps = 15


    if mode == "ssd":
        file_path = "./test_bottom_right1.mp4"
        size = (fst_img.shape[1], fst_img.shape[0])
        out = cv2.VideoWriter(file_path, cv2.VideoWriter_fourcc(*'XVID'), fps, size)

        for i in range(1, len(frames)):
            src = cv2.imread(frames[i])
            img = cv2.cvtColor(src, cv2.COLOR_RGB2GRAY)
            min_ssd = sys.maxsize
            [px, py] = [boxh, boxw]
            for x in range(boxh - search_range, boxh + search_range):
                if x < 0 or x >= src.shape[0] - bh:
                    continue
                for y in range(boxw - search_range, boxw + search_range):
                    if y < 0 or y >= src.shape[1] - bw:
                        continue
                    roi = img[x:x + bh, y:y + bw]
                    ssd = np.sum(np.square((last_roi - roi)))
                    if ssd < min_ssd:
                        min_ssd = ssd
                        px = x
                        py = y
            boxh = px
            boxw = py
            last_roi = img[boxh:boxh + bh, boxw:boxw + bw]
            cv2.rectangle(src, (boxw, boxh), (boxw + bw, boxh + bh), (0, 255, 0), 1)

            index = findCandidate(src, boxw+bw, tileSet)

            src[rmin:rmin + height, boxw + bw + 5: 310] = last_frame[rmin:rmin + height, boxw + bw + 5:310]
            src[rmin:rmin + height, boxw + bw: boxw + bw + 5] = tileSet[index]
            last_frame = src

            out.write(src)
        out.release()


frames = sorted(glob.glob('/Users/duxinzhe/PycharmProjects/magic-eraser-cv/videoImage/*.jpg'))
tileSet = generateTileSet(height, rmax, cmax, cmin)
tracking(frames, tileSet, mode = "ssd")
