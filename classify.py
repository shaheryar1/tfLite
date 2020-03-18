import numpy as np
import tensorflow as tf
import cv2
import time
import os

# Load TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(model_path="classfication_model/mobilenet_v1_1.0_224_quant.tflite")


# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print("== Input details ==")
print("shape:", input_details[0]['shape'])
print("\n== Output details ==")
print("shape:", output_details[0]['shape'])
#
# interpreter.resize_tensor_input(input_details[0]['index'], (2, 224, 224, 3))
# interpreter.resize_tensor_input(output_details[0]['index'], (2, 1001))

interpreter.allocate_tensors()

# Load labels
PATH_TO_LABELS = os.path.join('classfication_model','labels_mobilenet_quant_v1_224.txt')

# Load the label map
with open(PATH_TO_LABELS, 'r') as f:
    labels = [line.strip() for line in f.readlines()]




# Test model on random input data.

frame=cv2.imread('testing_data/cat.jpg')
frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
frame_resized = cv2.resize(frame_rgb, (224, 224))

# input_data=np.array([frame_resized,frame_resized])
input_data = np.expand_dims(frame_resized, axis=0)
print(input_data.shape)
input_shape = input_details[0]['shape']

t=time.time()
# print(t)

interpreter.set_tensor(input_details[0]['index'], input_data)
interpreter.invoke()
print(time.time()-t)
# The function `get_tensor()` returns a copy of the tensor data.
# Use `tensor()` in order to get a pointer to the tensor.
output_data = interpreter.get_tensor(output_details[0]['index'])
if output_details[0]['dtype'] == np.uint8:
    scale, zero_point = output_details[0]['quantization']
    output = scale * (output_data - zero_point)





score = np.max(output)
idx = np.argmax(output)

print(labels[idx],score)




