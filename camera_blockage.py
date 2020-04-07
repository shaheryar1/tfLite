import cv2
import numpy as np
from PIL import Image



# define a video capture object
vid = cv2.VideoCapture(0)




blackThresh=50   #30 is RGB value


while (True):

    # Capture the video frame
    # by frame
    ret, frame = vid.read()
    nblack = 0





    imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imgray = cv2.GaussianBlur(imgray, (7, 7), 0)
    ret, thresh = cv2.threshold(imgray, 70, 255, 0)



    im = Image.fromarray(thresh)
    pixels = im.getdata()

    for pixel in pixels:
        if (pixel <= blackThresh ):
            nblack = nblack + 1
    # # for pixel in pixels:
    # #     if (pixel[0] <= blackThresh and pixel[1] <= blackThresh and pixel[2] <= blackThresh):
    # #         nblack = nblack + 1
    n = len(pixels)
    print(nblack / float(n) * 100)
    blockage_percent=nblack / float(n)
    if (blockage_percent) > 0.75:  # 0.8 is 80% black
        cv2.putText(frame, "Camera is blocked", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 255, 0), 2,
                    cv2.LINE_AA)
    elif(blockage_percent>0.60):
        cv2.putText(frame, "Camera is partially blocked", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 255, 0), 2,
                    cv2.LINE_AA)


    cv2.imshow('frame', frame)
    cv2.imshow('gray', imgray)
    cv2.imshow('img', thresh)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
