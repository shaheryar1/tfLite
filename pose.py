import numpy as np
import tensorflow as tf
import cv2
import time
import os
from utils.pose_utils import get_keypoints,PARTS




# Load TFLite model and allocate tensors.
def loadModel(path='posenet_model/posenet_mobilenet_v1_100_257x257_multi_kpt_stripped.tflite'):
    interpreter = tf.lite.Interpreter(model_path=path)


    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    print("== Input details ==")
    print("shape:", input_details)
    print("\n== Output details ==")
    print("shape:", output_details)
    #


    interpreter.allocate_tensors()

    return interpreter







if __name__ == '__main__':
    # load model
    interpreter=loadModel()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    frame_rate_calc = 1
    freq = cv2.getTickFrequency()
    # grab camera
    cap = cv2.VideoCapture(0)
    ret = True
    count = -1;
    while ret:


        count = count + 1;
        # Start timer (for calculating frame rate)
        t1 = cv2.getTickCount()

        # Grab frame from video stream
        ret, frame = cap.read()
        HEIGHT,WIDTH,CHANNELS=frame.shape

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (257, 257))


        if(count%3==0):
            input_data = np.expand_dims(frame_resized, axis=0)

            input_shape = input_details[0]['shape']

            t=time.time()

            floating_model = input_details[0]['dtype'] == np.float32
            if floating_model:
                input_data = (np.float32(input_data) - 127.5) / 127.5


            interpreter.set_tensor(input_details[0]['index'], input_data)
            interpreter.invoke()

            # The function `get_tensor()` returns a copy of the tensor data.
            # Use `tensor()` in order to get a pointer to the tensor.
            heat_map = np.squeeze(interpreter.get_tensor(output_details[0]['index']))
            offsets=np.squeeze(interpreter.get_tensor(output_details[1]['index']))
            stride = 32

            keypoints =get_keypoints(heat_map,offsets,32)

        for point in keypoints:

            if(point.confidence>=0.60 and (point.body_part==PARTS[9] or point.body_part==PARTS[10])):

                frame_resized=cv2.circle(frame_resized,(int(point.y),int(point.x)),2,(0,0,255),cv2.FILLED)
                print(point.confidence)

        org_size_frame= cv2.cvtColor(frame_resized, cv2.COLOR_RGB2BGR)
        org_size_frame= cv2.resize(org_size_frame,(WIDTH,HEIGHT))


        line_threshold = 150

        cv2.line(org_size_frame,(0,HEIGHT-line_threshold),(WIDTH,HEIGHT-line_threshold),(0,255,0),2)

        # Draw framerate in corner of frame
        cv2.putText(org_size_frame, 'FPS: {0:.2f}'.format(frame_rate_calc), (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2,
                    cv2.LINE_AA)
        # All the results have been drawn on the frame, so it's time to display it.
        cv2.imshow('a', org_size_frame)
        # Calculate framerate
        t2 = cv2.getTickCount()
        time1 = (t2 - t1) / freq
        frame_rate_calc = 1 / time1
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    # Destroy all the windows
    cv2.destroyAllWindows()