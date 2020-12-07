import cv2


def video_split(video_path, save_path):

    vc = cv2.VideoCapture(video_path)
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
