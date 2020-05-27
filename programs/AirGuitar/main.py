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





vc = VideoStream(src=0).start()
#vs = VideoStream(usePiCamera=False).start()
time.sleep(2.0)

engine = PoseEngine('programs/pose_detect/models/mobilenet/posenet_mobilenet_v1_075_481_641_quant_decoder_edgetpu.tflite')
def make_sounds(y_axis):
    # Presumably, the pitch of the buzzer is based on the y-axis of your arm.



def draw_image(frame, pose):
    # add a pose to the frame, then return the frame.
    for label, keypoint in pose.keypoints.items():
        if float(keypoint.score) > 0:
            coord = (keypoint.yx[1], keypoint.yx[0])
            radius = 5
            col = (0, 0, 255)
            thickness = 2
            frame = cv2.circle(frame, coord, radius, col, thickness)
    return frame


def generate():
    while True:
        frame = vc.read()
        frame = imutils.resize(frame, width=640, height=480)
        poses, inference_time = engine.DetectPosesInImage(np.uint8(frame))
        print('Inference time: %.fms' % inference_time)
        for pose in poses:
            if pose.score < 0.4: continue
            print('\nPose Score: ', pose.score)
            frame = draw_image(frame, pose)


        by = cv2.imencode('.jpg', frame)[1].tostring()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + by + b'\r\n')
