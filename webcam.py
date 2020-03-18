
# Import packages
import os
from utils.utils import non_max_suppression_slow,get_iou
import argparse
import cv2
import numpy as np
import sys
import time
from threading import Thread
import importlib.util
from DTO.Detection_DTO import DetectionDTO
import glob
from utils.centroidtracker import CentroidTracker
from DAL.DetectionDAL import DetectionDAL

def getAvailableCamera():
    for camera in glob.glob("/dev/video?"):
        print(camera)
        cap = cv2.VideoCapture(camera)
        if (cap.isOpened()):
            return cap
        else:
            cap.release()

MODEL_NAME = "ssd_mobilenet"
GRAPH_NAME = "detect.tflite"
LABELMAP_NAME = "labelmap.txt"
min_conf_threshold = float(0.6)
resW, resH = 640,480
imW, imH = int(resW), int(resH)
use_TPU = False
# Import TensorFlow libraries
# If tensorflow is not installed, import interpreter from tflite_runtime, else import from regular tensorflow
# If using Coral Edge TPU, import the load_delegate library
# pkg = importlib.util.find_spec('tensorflow')
# if pkg is None:
#     from tflite_runtime.interpreter import Interpreter
#
#     if use_TPU:
#         from tflite_runtime.interpreter import load_delegate
# else:
from tensorflow.lite.python.interpreter import Interpreter

if use_TPU:
    from tensorflow.lite.python.interpreter import load_delegate

# If using Edge TPU, assign filename for Edge TPU model
if use_TPU:
    # If user has specified the name of the .tflite file, use that name, otherwise use default 'edgetpu.tflite'
    if (GRAPH_NAME == 'detect.tflite'):
        GRAPH_NAME = 'edgetpu.tflite'

    # Get path to current working directory
CWD_PATH = os.getcwd()

# Path to .tflite file, which contains the model that is used for object detection
PATH_TO_CKPT = os.path.join(CWD_PATH, MODEL_NAME, GRAPH_NAME)

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH, MODEL_NAME, LABELMAP_NAME)

# Load the label map
with open(PATH_TO_LABELS, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

# Have to do a weird fix for label map if using the COCO "starter model" from
# https://www.tensorflow.org/lite/models/object_detection/overview
# First label is '???', which has to be removed.
if labels[0] == '???':
    del (labels[0])



# Load the Tensorflow Lite model.
# If using Edge TPU, use special load_delegate argument
if use_TPU:
    interpreter = Interpreter(model_path=PATH_TO_CKPT,
                              experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
    print(PATH_TO_CKPT)
else:
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
    target_object_id=43
    max_disappeared=12;
    ct = CentroidTracker(max_disappeared)

    # Initialize video stream
    vid = cv2.VideoCapture(0)
    ret = True
    count=-1;
    # for frame1 in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):
    while ret:

        count=count+1;
        # Start timer (for calculating frame rate)
        t1 = cv2.getTickCount()

        # Grab frame from video stream
        ret, frame1 = vid.read()

        # Acquire frame and resize to expected shape [1xHxWx3]

        frame = frame1.copy()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (width, height))
        input_data = np.expand_dims(frame_resized, axis=0)
        if(True):

        # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
            if floating_model:
                input_data = (np.float32(input_data) - input_mean) / input_std

            # Perform the actual detection by running the model with the image as input
            interpreter.set_tensor(input_details[0]['index'], input_data)
            interpreter.invoke()

            # Retrieve detection results
            boxes = interpreter.get_tensor(output_details[0]['index'])[0]  # Bounding box coordinates of detected objects
            classes = interpreter.get_tensor(output_details[1]['index'])[0]  # Class index of detected objects
            scores = interpreter.get_tensor(output_details[2]['index'])[0]  # Confidence of detected objects

        # num = interpreter.get_tensor(output_details[3]['index'])[0]  # Total number of detected objects (inaccurate and not needed)
        #    Applying non-maxima supression
        boxes_temp = [];
        classes_temp=[]
        scores_temp=[]
        nms_idx=[]
        for i in range(len(scores)):
            if ((scores[i] > min_conf_threshold) and (scores[i] <= 1.0) and classes[i]==target_object_id):

                boxes[i][0] = int(max(1, (boxes[i][0] * imH)))
                boxes[i][1] = int(max(1, (boxes[i][1] * imW)))
                boxes[i][2] = int(min(imH, (boxes[i][2] * imH)))
                boxes[i][3] = int(min(imW, (boxes[i][3] * imW)))
                classes_temp.append(classes[i])
                boxes_temp.append(boxes[i])
                scores_temp.append(scores[i])

        boxes_temp = np.array(boxes_temp)
        boxes=boxes_temp
        scores=scores_temp
        classes=classes_temp
        # print("Before NMS", len(boxes_list))
        # nms_idx represents indices of selected bounding boxes
        nms_idx = non_max_suppression_slow(boxes_temp, 0.3)
        # print("After NMS", len(nms_idx))


        # Loop over all detections and draw detection box if confidence is above minimum threshold
        for idx in (nms_idx):
            # if ((scores[i] > min_conf_threshold) and (scores[i] <= 1.0)):
                # Get bounding box coordinates and draw box
                # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
            ymin = int(max(1, (boxes[idx][0])))
            xmin = int(max(1, (boxes[idx][1] )))
            ymax = int(min(imH, (boxes[idx][2] )))
            xmax = int(min(imW, (boxes[idx][3] )))
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
        objects = ct.update(boxes)


        for (objectID, centroid) in objects.items():
            # draw both the ID of the object and the centroid of the
            # object on the output frame

            if(ct.disappeared[objectID]==max_disappeared-1):
                dto=DetectionDTO();
                dto.object_id=target_object_id
                dto.confidence=70
                dal.insertDetection(dto)

            text = "Object {}".format(objectID)
            cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

        # Tracking and assigning unique IDs part -- end

        # Draw framerate in corner of frame
        # cv2.putText(frame, 'FPS: {0:.2f}'.format(frame_rate_calc), (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2,
        #             cv2.LINE_AA)
        # All the results have been drawn on the frame, so it's time to display it.
        cv2.imshow('Object detector', frame)
        # Calculate framerate
        t2 = cv2.getTickCount()
        time1 = (t2 - t1) / freq
        frame_rate_calc = 1 / time1

        # Press 'q' to quit
        if cv2.waitKey(1) == ord('q'):
            break

    # Clean up

    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()
