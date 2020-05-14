# import the necessary packages
import imutils
import cv2
import datetime
import time
from imutils.video import VideoStream

vc = VideoStream(src=0).start()
time.sleep(2.0)


def generate():
    """Video streaming generator function."""
    while True:
        frame = vc.read()
        cv2.imwrite('pic.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('pic.jpg', 'rb').read() + b'\r\n')

