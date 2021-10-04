import cv2 as cv

print(cv.__version__) #To confirm that OpenCV is downloaded and imported by showing us what its current version is.

image = cv.imread('Photos and Videos/londoneyeview.jpg') #Creates pixel matrix 'image' equal to the photo 'londoneyeview.jpg' in the Photos file
cv.imshow('Image', image) #Opens a window named 'Image' that displays the image variable. Note that the image can be too big for the window.
                          #Image used is 650 x 488 in size.
capture = cv.VideoCapture('Photos and Videos/SanctuaryGuardian.mp4') #This can take an integer value that correpsonds to a specific camera.
                                                                #I already have a video in file, so it will use the file path instead.
while True:
    isTrue, frame = capture.read() #Videos are displayed frame by frame using a while loop. This determines if the frame was read correctly.

    cv.imshow('Video', frame) #Displaying an individual frame.

    if cv.waitKey(20) & 0xFF==ord('d'): #To stop the video from playing forever. If 'd' is pressed, we stop the video.
        break

capture.release() #The capture variable is an instance of the VideoCapture class, and we use it to grab the video frame by frame
                  #in the while loop. Here we are releasing the capture device.
cv.destroyAllWindows() #Closes all windows.


cv.waitKey(0)
