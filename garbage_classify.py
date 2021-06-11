from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import io
from time import sleep
import numpy as np
import picamera

import RPi.GPIO as GPIO
import time
import threading
from threading import Thread
from PIL import Image
from tflite_runtime.interpreter import Interpreter


labelExport = 0
gabIsAvail = 0
count = 3


def load_labels(path):
    with open(path, 'r') as f:
        return {i: line.strip() for i, line in enumerate(f.readlines())}


def set_input_tensor(interpreter, image):
    tensor_index = interpreter.get_input_details()[0]['index']
    input_tensor = interpreter.tensor(tensor_index)()[0]
    input_tensor[:, :] = image


def classify_image(interpreter, image, top_k=1):
    """Returns a sorted array of classification results."""
    set_input_tensor(interpreter, image)
    interpreter.invoke()
    output_details = interpreter.get_output_details()[0]
    output = np.squeeze(interpreter.get_tensor(output_details['index']))

    # If the model is quantized (uint8 data), then dequantize the results
    if output_details['dtype'] == np.uint8:
        scale, zero_point = output_details['quantization']
        output = scale * (output - zero_point)

    ordered = np.argpartition(-output, top_k)
    return [(i, output[i]) for i in ordered[:top_k]]


def countToStop():
    global count
    while count > 0:
        count = count - 1
        print(count, " s left...")
        sleep(1)
    print("count done")


def Classify():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # parser.add_argument(
    #     '--model', help='File path of .tflite file.', required=True)
    # parser.add_argument(
    #     '--labels', help='File path of labels file.', required=True)
    args = parser.parse_args()

    labels = load_labels('labels.txt')

    interpreter = Interpreter('model.tflite')

    interpreter.allocate_tensors()
    _, height, width, _ = interpreter.get_input_details()[0]['shape']
    countStop = threading.Thread(
        target=countToStop, args=())
    countStop.start()
    with picamera.PiCamera(resolution=(640, 480), framerate=30) as camera:
        camera.start_preview()
        try:
            stream = io.BytesIO()
            for _ in camera.capture_continuous(
                    stream, format='jpeg', use_video_port=True):

                stream.seek(0)
                image = Image.open(stream).convert('RGB').resize((width, height),
                                                                 Image.ANTIALIAS)
                start_time = time.time()
                results = classify_image(interpreter, image)
                elapsed_ms = (time.time() - start_time) * 1000
                label_id, prob = results[0]
                stream.seek(0)
                stream.truncate()
                camera.annotate_text = '%s %.2f\n%.1fms' % (labels[label_id], prob,
                                                            elapsed_ms)
                labelExport = label_id

                if count == 0:
                    gabIsAvail = 0
                    print("Done classify", labels[label_id])
                    sleep(1)
                    raise Exception("No garbage")
        except:
            print("Out Camera")

        finally:
            camera.stop_preview()
