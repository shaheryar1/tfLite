import cv2
import numpy as np
from PIL import Image

def detect_blockage(frame,blackThresh=50):


    imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imgray = cv2.GaussianBlur(imgray, (7, 7), 0)
    ret, thresh = cv2.threshold(imgray, 70, 255, 0)
    nblack = 0

    imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imgray = cv2.GaussianBlur(imgray, (7, 7), 0)
    ret, thresh = cv2.threshold(imgray, 70, 255, 0)

    im = Image.fromarray(thresh)
    pixels = im.getdata()

    for pixel in pixels:
        if (pixel <= blackThresh):
            nblack = nblack + 1
    # # for pixel in pixels:
    # #     if (pixel[0] <= blackThresh and pixel[1] <= blackThresh and pixel[2] <= blackThresh):
    # #         nblack = nblack + 1
    n = len(pixels)

    blockage_percent = nblack / float(n)
    if (blockage_percent) > 0.75:  # 0.8 is 80% black
        # cv2.putText(frame, "Camera is blocked", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
        #             (255, 255, 0), 2,
        #             cv2.LINE_AA)
        return 1
    elif (blockage_percent > 0.60):
        # cv2.putText(frame, "Camera is partially blocked", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
        #             (255, 255, 0), 2,
        #             cv2.LINE_AA)
        return 2

    return 0


