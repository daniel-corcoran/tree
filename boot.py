from app.motion_detection import SingleMotionDetector
from waitress import serve
from flask import *
from flask import render_template
from flask import request
from flask import Response
import threading
import datetime
import imutils
import time
import cv2
from app import app
from tools.power import reboot, power_off
from tools.update import update
from imutils.video import VideoStream


outputFrame = None
lock = threading.Lock()

vs = VideoStream(src=0).start()
time.sleep(2.0)


def detect_motion(frameCount):
    # grab global references to the video stream, output frame, and
    # lock variables
    global vs, outputFrame, lock

    # initialize the motion detector and the total number of frames
    # read thus far
    md = SingleMotionDetector(accumWeight=0.1)
    total = 0

    # loop over frames from the video stream
    while True:
        # read the next frame from the video stream, resize it,
        # convert the frame to grayscale, and blur it
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        # grab the current timestamp and draw it on the frame
        timestamp = datetime.datetime.now()
        cv2.putText(frame, timestamp.strftime(
            "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        # if the total number of frames has reached a sufficient
        # number to construct a reasonable background model, then
        # continue to process the frame
        if total > frameCount:
            # detect motion in the image
            motion = md.detect(gray)

            # cehck to see if motion was found in the frame
            if motion is not None:
                # unpack the tuple and draw the box surrounding the
                # "motion area" on the output frame
                (thresh, (minX, minY, maxX, maxY)) = motion
                cv2.rectangle(frame, (minX, minY), (maxX, maxY),
                              (0, 0, 255), 2)

        # update the background model and increment the total number
        # of frames read thus far
        md.update(gray)
        total += 1

        # acquire the lock, set the output frame, and release the
        # lock
        with lock:
            outputFrame = frame.copy()


def generate():
    # grab global references to the output frame and lock variables
    global outputFrame, lock

    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame is None:
                continue

            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

            # ensure the frame was successfully encoded
            if not flag:
                continue

        # yield the output frame in the byte format
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encodedImage) + b'\r\n')


@app.route("/video_feed")
def video_feed():
    return Response(generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/update")
def update_helper():
    update()
    return init_config()


@app.route("/upload")
def upload():
    # user has uploaded a new file. We need to parse and install it.
    ...
    # TODO


@app.route("/reboot")
def reboot_helper():
    reboot()
    return render_template("connect.html")


@app.route("/power_off")
def power_off_helper():
    power_off()
    return render_template("connect.html")


@app.route("/")
def home_page():
    return render_template('view.html')


# Initialize flask server on boot

@app.route('/config')
def init_config():
    return render_template('config.html')


@app.route('/view')
def init_view():
    return render_template('view.html')


if __name__ == '__main__':
    # Start the current application as a daemon process
    t = threading.Thread(target=detect_motion, args=(32,))
    t.daemon = True
    t.start()



    print("Server program has begin. Beginning service.")
    try:
        print("Attempting to open on port 80")
        serve(app, host='0.0.0.0', port=80)
    except:
        print("Unsuccessful. Attempting on port 8000")
        serve(app, host='0.0.0.0', port=8001)
    print("Main sequence closed. The program has ended")
