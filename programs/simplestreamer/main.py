# import the necessary packages
import imutils
import cv2
import datetime
import time
from imutils.video import VideoStream



def generate():
    vc = VideoStream(src=0).start()
    time.sleep(2.0)

    """Video streaming generator function."""
    while True:
        frame = vc.read()
        frame = imutils.resize(frame, width=400) # To save bandwidth?
        by = cv2.imencode('.jpg', frame)[1].tostring()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + by + b'\r\n')

