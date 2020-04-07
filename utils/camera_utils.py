# import cv2
#
#
# def detec_blockage(image):
#
#     imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     imgray = cv2.GaussianBlur(imgray, (7, 7), 0)
#     ret, thresh = cv2.threshold(imgray, 70, 255, 0)
