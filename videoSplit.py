import cv2  # 导入opencv模块
import os
import time


def video_split(video_path, save_path):
    '''
    对视频文件切割成帧
    '''
    '''
    @param video_path:视频路径
    @param save_path:保存切分后帧的路径
    '''
    vc = cv2.VideoCapture(video_path)
    # 一帧一帧的分割 需要几帧写几
    c = 0
    if vc.isOpened():
        rval, frame = vc.read()
    else:
        rval = False
    while rval:
        rval, frame = vc.read()

        cv2.imwrite(save_path + "/" + str('%06d' % c) + '.jpg', frame)
        # cv2.waitKey(1)
        c = c + 1

video_split('Original.avi', '/Users/duxinzhe/PycharmProjects/magic-eraser-cv/videoImage')
print('finish!')

video = cv2.VideoCapture('Original.avi')
fps = video.get(cv2.CAP_PROP_FPS)
print(fps)
