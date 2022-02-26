# import the opencv library
import numpy as np
import cv2 as cv
import tkinter as tk
import os
import sys
from PIL import Image, ImageTk # pip3 install pillow

img_counter = 0
numFrames = 0
cancel = False

# define a video capture object
capture = cv.VideoCapture(0)
if not capture.isOpened():
	print("Cannot open camera")
	sys.exit(1) # sys.exit(_): Exits the code, 1 indicates an error, 0 indicates success
else:
	capWidth = capture.get(3)
	capHeight = capture.get(4)

# Capture the video frame-by-frame
success, frame = capture.read()
if not success:
	print("Can't receive frame (stream end?). Exiting ...")
	sys.exit(1)

def capSaveWindow(event = 0):
    global cancel, capBTN, saveBTN, discBTN, timerBTN, multFrameBTN
    cancel = True

    capBTN.place_forget()
    timerBTN.place_forget()
    multFrameBTN.place_forget()
    saveBTN = tk.Button(mainWindow, text="Save Image", command=saveCapture)
    discBTN = tk.Button(mainWindow, text="Discard", command=returnFromCapture)
    saveBTN.place(anchor=tk.CENTER, relx=0.2, rely=0.9, width=150, height=50)
    discBTN.place(anchor=tk.CENTER, relx=0.8, rely=0.9, width=150, height=50)
    saveBTN.focus()

def saveCapture(event = 0):
	global img_counter, frame, saveBTN, discBTN

	# Create screenshot variable with updating filename: /filepath/screenshot_{img_counter}.png
	screenshot = "C:/Users/adrie/Documents/Documents/UNC_Charlotte/Spring 2022/ECGR-4252 Senior Design II/Screenshots/screenshot_{}.png".format(img_counter)
	# Write current frame to screenshot variable
	cv.imwrite(screenshot, frame)
	img_counter += 1
	returnFromCapture()

def returnFromCapture(event = 0):
    global discBTN, saveBTN
    saveBTN.place_forget()
    discBTN.place_forget()
    resume()

def multiFrameWindow(event = 0):
    global cancel, capBTN, timerBTN, multFrameBTN, numFrames, moreFramesBTN, setFramesBTN, lessFramesBTN
    cancel = False

    capBTN.place_forget()
    timerBTN.place_forget()
    multFrameBTN.place_forget()
    frameString = str(numFrames)
    frameText = "Frames: " + frameString
    moreFramesBTN = tk.Button(mainWindow, text="MORE", command=addFrame)
    setFramesBTN = tk.Button(mainWindow, text=frameText, command=multiFrameCapture)
    lessFramesBTN = tk.Button(mainWindow, text="LESS", command=subtractFrame)
    moreFramesBTN.place(anchor=tk.CENTER, relx=0.2, rely=0.7, width=150, height=50)
    setFramesBTN.place(anchor=tk.CENTER, relx=0.2, rely=0.8, width=150, height=50)
    lessFramesBTN.place(anchor=tk.CENTER, relx=0.2, rely=0.9, width=150, height=50)
    setFramesBTN.focus()

def multiFrameCapture(event = 0):
    global frame, numFrames, img_counter, prevImg, moreFramesBTN, setFramesBTN, lessFramesBTN

    while numFrames > 0:
        # Capture frame
        _, frame = capture.read()
        cvimage = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)
        prevImg = Image.fromarray(cvimage)
        imgtk = ImageTk.PhotoImage(image=prevImg)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        # Take a screenshot
        screenshot = "C:/Users/adrie/Documents/Documents/UNC_Charlotte/Spring 2022/ECGR-4252 Senior Design II/Screenshots/screenshot_{}.png".format(img_counter)
        cv.imwrite(screenshot, frame)
        img_counter += 1
        numFrames -= 1
    moreFramesBTN.place_forget()
    setFramesBTN.place_forget()
    lessFramesBTN.place_forget()
    resume()
    sys.exit(0)

def timerWindow(event=0):
    global cancel, capBTN, timerBTN, setTimerBTN, multFrameBTN
    cancel = False

    capBTN.place_forget()
    timerBTN.place_forget()
    multFrameBTN.place_forget()
    setTimerBTN = tk.Button(mainWindow, text="Timer Button", command=setTimer)
    setTimerBTN.place(anchor=tk.CENTER, relx=0.2, rely=0.9, width=150, height=50)
    setTimerBTN.focus()

def setTimer(event=0):
    sys.exit(0)

def resume(event = 0):
    global saveBTN, discBTN, capBTN, lmain, cancel
    cancel = False

    mainWindow.bind('<Return>', capSaveWindow)
    capBTN.place(bordermode=tk.INSIDE, relx=0.85, rely=0.9, anchor=tk.CENTER, width=150, height=50)
    timerBTN.place(bordermode=tk.INSIDE, relx=0.85, rely=0.7, anchor=tk.CENTER, width=150, height=50)
    multFrameBTN.place(bordermode=tk.INSIDE, relx=0.85, rely=0.8, anchor=tk.CENTER, width=150, height=50)
    lmain.after(10, show_frame)

def exitWindow(event=0):
	mainWindow.quit()

mainWindow = tk.Tk()
mainWindow.resizable(width=False, height=False)
mainWindow.bind('<Escape>', lambda e: mainWindow.quit()) # .bind('<Escape>', ...) makes the esc key close the main window
capBTN = tk.Button(mainWindow, text="Capture", command=capSaveWindow)
exitBTN = tk.Button(mainWindow, text="Exit", command=exitWindow)
timerBTN = tk.Button(mainWindow, text="Set Timer", command=timerWindow)
multFrameBTN = tk.Button(mainWindow, text="Multi-Frame", command=multiFrameWindow)

lmain.pack()
capBTN.place(bordermode=tk.INSIDE, relx=0.85, rely=0.9, anchor=tk.CENTER, width=150, height=50)
capBTN.focus()
exitBTN.place(bordermode=tk.INSIDE, relx=0.85, rely=0.1, anchor=tk.CENTER, width=150, height=50)
timerBTN.place(bordermode=tk.INSIDE, relx=0.85, rely=0.7, anchor=tk.CENTER, width=150, height=50)
multFrameBTN.place(bordermode=tk.INSIDE, relx=0.85, rely=0.8, anchor=tk.CENTER, width=150, height=50)

def addFrame():
    global numFrames

    if numFrames < 10:
        numFrames += 1
    multiFrameWindow()

def subtractFrame():
    global numFrames

    if numFrames > 0:
        numFrames -= 1
    multiFrameWindow()

def show_frame():
    global cancel, prevImg, capBTN

    # capture.read() returns true/false for if the frame was captured, and then the frame itself
    # "_," ignores the true/false and just gets the frame
    _, frame = capture.read()
    # convert between RGB and BGR color spaces (with or without alpha channel)
    cvimage = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)

    prevImg = Image.fromarray(cvimage)
    imgtk = ImageTk.PhotoImage(image=prevImg)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    if not cancel:
        lmain.after(10, show_frame)

show_frame()
mainWindow.mainloop()
