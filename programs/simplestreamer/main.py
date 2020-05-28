# import the necessary packages
import imutils
import cv2
import time
import acapture
# Why is this so slow?

def generate():
    cap = acapture.open(0)
    time.sleep(2.0)

    """Video streaming generator function."""
    while True:
        start = time.time()
        check, frame = cap.read()
        if check:
            end = time.time()
            print("capture time: {}".format(end - start))

            start = time.time()
            frame = imutils.resize(frame, width=100) # To save bandwidth?
            #cv2.imshow("frame", frame)
            by = cv2.imencode('.jpg', frame)[1].tostring()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + by + b'\r\n')

        print("Process and display time: {}".format(end - start))
