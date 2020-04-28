
# Import packages
import os
from utils.utils import non_max_suppression,get_iou
import argparse
import cv2
from utils.camera_utils import detect_blockage
import numpy as np
import sys
import time
from threading import Thread
import importlib.util
from DTO.Detection_DTO import DetectionDTO
import glob
from utils.centroidtracker import CentroidTracker
from DAL.DetectionDAL import DetectionDAL


from tflite_runtime.interpreter import Interpreter

MODEL_NAME = "ssd_mobilenet"
GRAPH_NAME = "detect.tflite"
LABELMAP_NAME = "labelmap.txt"
min_conf_threshold = float(0.55)
resW, resH = 640,480
imW, imH = int(resW), int(resH)
use_TPU = False






CWD_PATH = os.getcwd()

# Path to .tflite file, which contains the model that is used for object detection
PATH_TO_CKPT = os.path.join(CWD_PATH, MODEL_NAME, GRAPH_NAME)

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH, MODEL_NAME, LABELMAP_NAME)

# Load the label map
with open(PATH_TO_LABELS, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

if labels[0] == '???':
    del (labels[0])



# Load the Tensorflow Lite model.
interpreter = Interpreter(model_path=PATH_TO_CKPT)

interpreter.allocate_tensors()

# Get model details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

floating_model = (input_details[0]['dtype'] == np.float32)

input_mean = 127.5
input_std = 127.5


if __name__ == '__main__':
    # Initialize frame rate calculation
    frame_rate_calc = 1
    freq = cv2.getTickFrequency()
    dal=DetectionDAL()
    target_objects=np.arange(0,90) #only targetting bottle object
    max_disappeared=6; # frames count for max disappeared
    line_threshold=200
    ct = CentroidTracker(max_disappeared)

    previous_points={}
    # Initialize video stream
    vid = cv2.VideoCapture('cam.mp4')
    ret = True
    count=-1;


    # for frame1 in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):
    while ret:



        count=count+1;
        # Start timer (for calculating frame rate)
        t1 = cv2.getTickCount()

        # Grab frame from video stream
        ret, frame1 = vid.read()




        frame = frame1.copy()
        HEIGHT, WIDTH, CHANNELS = frame.shape
        # check camera blockage




        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (width, height))
        input_data = np.expand_dims(frame_resized, axis=0)
        if(True):

        # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
            if floating_model:
                input_data = (np.float32(input_data) - input_mean) / input_std
                print("floating model")

            now = time.time()
            # Perform the actual detection by running the model with the image as input
            interpreter.set_tensor(input_details[0]['index'], input_data)
            interpreter.invoke()
            print(time.time() - now)

            # Retrieve detection results
            boxes = interpreter.get_tensor(output_details[0]['index'])[0]  # Bounding box coordinates of detected objects
            classes = interpreter.get_tensor(output_details[1]['index'])[0]  # Class index of detected objects
            scores = interpreter.get_tensor(output_details[2]['index'])[0]  # Confidence of detected objects




            boxes_temp = [];
            classes_temp=[]
            scores_temp=[]
            for i in range(len(scores)):
                if ((scores[i] > min_conf_threshold) and (scores[i] <= 1.0)  and classes[i] in target_objects ):

                    y1 = int(max(1, (boxes[i][0] * imH)))
                    x1 = int(max(1, (boxes[i][1] * imW)))
                    y2 = int(min(imH, (boxes[i][2] * imH)))
                    x2 = int(min(imW, (boxes[i][3] * imW)))
                    classes_temp.append(classes[i])
                    boxes_temp.append([y1,x1,y2,x2])
                    scores_temp.append(scores[i])
            boxes_temp = np.array(boxes_temp)
            classes_temp=np.array(classes_temp)
            nms_idx = non_max_suppression(boxes_temp, 0.3)


        # Loop over all detections and draw detection box if confidence is above minimum threshold
        for idx in (nms_idx):
            # if ((scores[i] > min_conf_threshold) and (scores[i] <= 1.0)):
                # Get bounding box coordinates and draw box
                # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
            ymin = int(max(1, (boxes_temp[idx][0])))
            xmin = int(max(1, (boxes_temp[idx][1] )))
            ymax = int(min(imH, (boxes_temp[idx][2] )))
            xmax = int(min(imW, (boxes_temp[idx][3] )))

            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (10, 255, 0), 2)
            # Draw label
            object_name = labels[int(classes[idx])]  # Look up object name from "labels" array using class index
            label = '%s: %d%%' % (object_name, int(scores[idx] * 100))  # Example: 'person: 72%'
            labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)  # Get font size
            label_ymin = max(ymin, labelSize[1] + 10)  # Make sure not to draw label too close to top of window
            cv2.rectangle(frame, (xmin, label_ymin - labelSize[1] - 10),
                          (xmin + labelSize[0], label_ymin + baseLine - 10), (255, 255, 255),
                          cv2.FILLED)  # Draw white box to put label text in

            cv2.putText(frame, label, (xmin, label_ymin - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0),
                        2)  # Draw label text

        # Tracking and assigning unique IDs part -- start

        objects,c = ct.update(boxes_temp[nms_idx],classes[nms_idx])



        for (objectID, centroid) in objects.items():

            thresh = HEIGHT-line_threshold
            #
            # if(ct.disappeared[objectID]==max_disappeared-1):
            #     dto=DetectionDTO();
            #     dto.object_id=target_object_id
            #     dto.confidence=70
            #     dal.insertDetection(dto)
            # draw both the ID of the object and the centroid of the
            # object on the output frame
            x=centroid[0]
            y=centroid[1]


            # Dropping and picking items from cart is started
            if(True):
                if(previous_points.get(objectID) is None):
                    previous_points[objectID]=0
                else:
                    if ( y > thresh and previous_points[objectID] < y and previous_points[objectID] < thresh):
                        print("Putting down  ",labels[int(c[objectID])])
                    elif (y < thresh and previous_points[objectID] > y and previous_points[objectID] > thresh):
                        print("Picking out ", labels[int(c[objectID])])

                previous_points[objectID]=y




            text = "Object {}".format(objectID)
            cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

        # Tracking and assigning unique IDs part -- end

        # Draw framerate in corner of frame


        cv2.putText(frame, 'FPS: {0:.2f}'.format(frame_rate_calc), (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2,
                        cv2.LINE_AA)


        cv2.line(frame, (0, HEIGHT - line_threshold), (WIDTH, HEIGHT - line_threshold), (0, 255, 0), 2)

        t2 = cv2.getTickCount()
        time1 = (t2 - t1) / freq
        frame_rate_calc = 1 / time1

        # All the results have been drawn on the frame, so it's time to display it.
        cv2.imshow('Object detector', frame)
        # Calculate framerate


        # Press 'q' to quit
        if cv2.waitKey(1) == ord('q'):
            break

    # Clean up

    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()