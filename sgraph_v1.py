# import the opencv library
import numpy as np
import cv2 as cv

img_counter = 0

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
	
	# Get user input
    	key = cv.waitKey(1)
    	if key == ord('q'):
        	break
    	elif key == ord('c'):
        	# Create screenshot variable with updating filename: /filepath/screenshot_{img_counter}.png
        	screenshot = "/home/pi/ELEC_SHADOW/Screenshots/screenshot_{}.png".format(img_counter)
        	# Write current frame to screenshot variable
        	cv.imwrite(screenshot, frame)
        	img_counter += 1

# After the loop release the capture object
capture.release()
cv.destroyAllWindows()
