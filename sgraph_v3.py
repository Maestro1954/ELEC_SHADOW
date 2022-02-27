# import the opencv library
import numpy as np
import cv2 as cv
import tkinter as tk
import os
import sys
from PIL import Image, ImageTk # pip install pillow
import threading
import time

img_counter = 0
numFrames = 0
cancel = False

# define a video capture object
capture = cv.VideoCapture(0)

if not capture.isOpened():
	print("Cannot open camera")
	sys.exit(1)
else:
	capWidth = capture.get(3)
	capHeight = capture.get(4)

# Capture the video frame-by-frame
success, frame = capture.read()

if not success:
	print("Can't receive frame (stream end?). Exiting ...")
	sys.exit(1)

def capSaveWindow(event = 0):
    global cancel, button0, button1, button2
    cancel = True

    button1.place_forget()
    button0.config(text="Save Image", command=saveCapture)
    button2.config(text="Discard", command=returnFromCapSave)
    button0.focus()

def saveCapture(event = 0):
    global img_counter, frame

    # Create screenshot variable with updating filename: /filepath/screenshot_{img_counter}.png
    screenshot = "C:/Users/adrie/Documents/Documents/UNC_Charlotte/Spring 2022/ECGR-4252 Senior Design II/Screenshots/screenshot_{}.png".format(img_counter)
    # Write current frame to screenshot variable
    cv.imwrite(screenshot, frame)
    img_counter += 1
    returnFromCapSave()

def returnFromCapSave(event = 0):
    global button0, button1, button2, lmain, cancel
    cancel = False
    
    mainWindow.bind('<Return>', capSaveWindow)
    button0.config(text="Capture", command=capSaveWindow)
    button1.place(bordermode=tk.INSIDE, relx=0.85, rely=0.8, anchor=tk.CENTER, width=150, height=50)
    button2.config(text="Set Timer", command=timerWindow)
    lmain.after(10, show_frame)

def multiFrameWindow(event = 0):
    global cancel, button0, button2, button1, numFrames
    cancel = False

    frameString = str(numFrames)
    frameText = "Frames: " + frameString
    button2.config(text="MORE", command=addFrame)
    button1.config(text=frameText, command=multiCapThread)
    button0.config(text="LESS", command=subtractFrame)
    button1.focus()

def multiCapThread(event = 0):
    t1 = threading.Thread(target=multiFrameCapture)
    t1.start()

def multiFrameCapture(event = 0):
    global frame, numFrames, img_counter

    while numFrames > 0:
        _, frame = capture.read()
        # Create screenshot variable with updating filename: /filepath/screenshot_{img_counter}.png
        screenshot = "C:/Users/adrie/Documents/Documents/UNC_Charlotte/Spring 2022/ECGR-4252 Senior Design II/Screenshots/screenshot_{}.png".format(img_counter)
        # Write current frame to screenshot variable
        cv.imwrite(screenshot, frame)
        img_counter += 1
        numFrames -= 1
        time.sleep(0.1)
    button0.config(text="Capture", command=capSaveWindow)
    button2.config(text="Set Timer", command=timerWindow)
    button1.config(text="Multi-Frame", command=multiFrameWindow)

# ______________TIMER__________________

def timerWindow(event=0):
    global cancel, button0, button2, setbutton2, button1
    cancel = False

    button0.place_forget()
    button2.place_forget()
    button1.place_forget()
    setbutton2 = tk.Button(mainWindow, text="Timer Button", command=setTimer)
    setbutton2.place(anchor=tk.CENTER, relx=0.2, rely=0.9, width=150, height=50)
    setbutton2.focus()

def setTimer(event=0):
    sys.exit(0)

#______________________________________

def exitWindow(event=0):
	mainWindow.quit()

mainWindow = tk.Tk()
mainWindow.resizable(width=False, height=False)
mainWindow.bind('<Escape>', lambda e: mainWindow.quit()) # .bind('<Escape>', ...) makes the esc key close the main window
lmain = tk.Label(mainWindow, compound=tk.CENTER, anchor=tk.CENTER, relief=tk.RAISED)
buttonX = tk.Button(mainWindow, text="Exit", command=exitWindow)
button0 = tk.Button(mainWindow, text="Capture", command=capSaveWindow)
button1 = tk.Button(mainWindow, text="Multi-Frame", command=multiFrameWindow)
button2 = tk.Button(mainWindow, text="Set Timer", command=timerWindow)

lmain.pack()
buttonX.place(bordermode=tk.INSIDE, relx=0.85, rely=0.1, anchor=tk.CENTER, width=150, height=50)
button0.place(bordermode=tk.INSIDE, relx=0.85, rely=0.9, anchor=tk.CENTER, width=150, height=50)
button0.focus()
button2.place(bordermode=tk.INSIDE, relx=0.85, rely=0.7, anchor=tk.CENTER, width=150, height=50)
button1.place(bordermode=tk.INSIDE, relx=0.85, rely=0.8, anchor=tk.CENTER, width=150, height=50)

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
    global cancel, prevImg, button0

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
