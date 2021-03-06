import os
import numpy as np
from PIL import Image
from programs.pose_detect.pose_engine import PoseEngine
import imutils
import cv2
import datetime
import time
from imutils.video import VideoStream

# TODO: Implement a generator function that returns serialized
# images to the webpage.


from tools import buzzer



vc = VideoStream(src=0).start()
#vs = VideoStream(usePiCamera=False).start()
time.sleep(2.0)

engine = PoseEngine('programs/pose_detect/models/mobilenet/posenet_mobilenet_v1_075_481_641_quant_decoder_edgetpu.tflite')
def make_sounds(y_axis):
    # Presumably, the pitch of the buzzer is based on the y-axis of your arm.
    try:
        print("Setting frequency to {}".format(y_axis * 2))
        buzzer.set_freq(y_axis * 2)
    except Exception as E:
        print(y_axis, E)


def draw_image(frame, pose):
    # add a pose to the frame, then return the frame.


    for label, keypoint in pose.keypoints.items():
        if float(keypoint.score) > 0:
            if label == 'left wrist':
                coord = (keypoint.yx[1], keypoint.yx[0])
                radius = 50
                col = (255, 0, 0)
                thickness = -1
                #frame = cv2.circle(frame, coord, radius, col, thickness)
            elif label == 'right wrist':
                coord = (keypoint.yx[1], keypoint.yx[0])
                radius = 50
                col = (0, 0, 255)
                thickness = -1
                frame = cv2.circle(frame, coord, radius, col, thickness)
                make_sounds(keypoint.yx[1])
    return frame


def generate():
    buzzer.enable_buzzer()
    while True:
        frame = vc.read()
        frame = imutils.resize(frame, width=720, height=540)
        poses, inference_time = engine.DetectPosesInImage(np.uint8(frame))
        print('Inference time: %.fms' % inference_time)
        for pose in poses:
            if pose.score < 0.4: continue
            print('\nPose Score: ', pose.score)
            frame = draw_image(frame, pose)
        frame = cv2.flip(frame, 1)

        by = cv2.imencode('.jpg', frame)[1].tostring()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + by + b'\r\n')
