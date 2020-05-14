from edgetpu.classification.engine import ClassificationEngine
from imutils.video import VideoStream
from PIL import Image
import argparse
import imutils
import time
import cv2


# initialize the labels dictionary
print("[INFO] parsing class labels...")
labels = {}

# loop over the class labels file
for row in open('programs/mobilenet_demo/mobilenet_v2/imagenet_labels.txt'):
	# unpack the row and update the labels dictionary
	(classID, label) = row.strip().split(" ", maxsplit=1)
	label = label.strip().split(",", maxsplit=1)[0]
	labels[int(classID)] = label

# load the Google Coral classification model
print("[INFO] loading Coral model...")
model = ClassificationEngine('programs/mobilenet_demo/mobilenet_v2/mobilenet_v2_1.0_224_quant_edgetpu.tflite')

# initialize the video stream and allow the camera sensor to warmup
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
#vs = VideoStream(usePiCamera=False).start()
time.sleep(2.0)
def generate():
# loop over the frames from the video stream
	while True:
		# grab the frame from the threaded video stream and resize it
		# to have a maximum width of 500 pixels
		frame = vs.read()
		frame = imutils.resize(frame, width=500)
		orig = frame.copy()

		# prepare the frame for classification by converting (1) it from
		# BGR to RGB channel ordering and then (2) from a NumPy array to
		# PIL image format
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		frame = Image.fromarray(frame)

		# make predictions on the input frame
		start = time.time()
		results = model.ClassifyWithImage(frame, top_k=1)
		end = time.time()
		# ensure at least one result was found
		if len(results) > 0:
			# draw the predicted class label, probability, and inference
			# time on the output frame
			(classID, score) = results[0]
			text = "{}: {:.2f}% ({:.4f} sec)".format(labels[classID],
				score * 100, end - start)
			cv2.putText(orig, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
				0.5, (0, 0, 255), 2)

		cv2.imwrite('pic.jpg', orig)
		yield (b'--frame\r\n'
			   b'Content-Type: image/jpeg\r\n\r\n' + open('pic.jpg', 'rb').read() + b'\r\n')

vs.stop()
