import imutils
import cv2
import time
import acapture
from imutils.video import VideoStream
vs = VideoStream(src=0).start()

def generate():

    """Video streaming generator function."""
    while True:
        frame = vs.read()

        frame = imutils.resize(frame, width=720) # To save bandwidth?
        #cv2.imshow("frame", frame)
        by = cv2.imencode('.jpg', frame)[1].tostring()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + by + b'\r\n')

