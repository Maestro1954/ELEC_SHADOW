# import the opencv library
import numpy as np
import cv2 as cv

# define a video capture object
capture = cv.VideoCapture(0)
if not capture.isOpened():
	print("Cannot open camera")
	exit()

while(True):
	# Capture the video frame-by-frame
	ret, frame = capture.read()
	
	# if frame is read correctly, ret is true
	if not ret:
		print("Can't receive frame (stream end?). Exiting ...")
		break

	# Display the resulting frame
	cv.imshow('Live Feed', frame)
	
	# wait 1ms for key input: 'q' (quit)
	if cv.waitKey(1) == ord('q'):
		break

# After the loop release the capture object
capture.release()
cv.destroyAllWindows()
