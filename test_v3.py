# import the opencv library
import numpy as np
import cv2 as cv
import tkinter as tk
import os
import sys
from PIL import Image, ImageTk # pip install pillow

img_counter = 0
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
    global cancel, capBTN, saveBTN, discBTN, setTimerBTN
    cancel = True

    capBTN.place_forget()
    setTimerBTN.place_forget()
    saveBTN = tk.Button(mainWindow, text="Save Image", command=saveAndReturn)
    discBTN = tk.Button(mainWindow, text="Discard", command=resume)
    saveBTN.place(anchor=tk.CENTER, relx=0.2, rely=0.9, width=150, height=50)
    discBTN.place(anchor=tk.CENTER, relx=0.8, rely=0.9, width=150, height=50)
    saveBTN.focus()

def saveAndReturn(event = 0):
	global img_counter

	# Create screenshot variable with updating filename: /filepath/screenshot_{img_counter}.png
	screenshot = "C:/Users/adrie/Documents/Documents/UNC_Charlotte/Spring 2022/ECGR-4252 Senior Design II/Code/Tkinter Code/Screenshots/screenshot_{}.png".format(img_counter)
	# Write current frame to screenshot variable
	cv.imwrite(screenshot, frame)
	img_counter += 1
	resume()

def resume(event = 0):
    global saveBTN, discBTN, capBTN, lmain, cancel

    cancel = False

    saveBTN.place_forget()
    discBTN.place_forget()

    mainWindow.bind('<Return>', capSaveWindow)
    capBTN.place(bordermode=tk.INSIDE, relx=0.85, rely=0.9, anchor=tk.CENTER, width=150, height=50)
    setTimerBTN.place(bordermode=tk.INSIDE, relx=0.85, rely=0.8, anchor=tk.CENTER, width=150, height=50)
    lmain.after(10, show_frame)

def exitWindow(event=0):
	mainWindow.quit()

def timerWindow(event=0):
    global cancel, capBTN, setTimerBTN, timerBTN
    cancel = False

    capBTN.place_forget()
    setTimerBTN.place_forget()
    timerBTN = tk.Button(mainWindow, text="Timer Button", command=setTimer)
    timerBTN.place(anchor=tk.CENTER, relx=0.2, rely=0.9, width=150, height=50)
    timerBTN.focus()

def setTimer(event=0):
    sys.exit(0)

mainWindow = tk.Tk()
mainWindow.resizable(width=False, height=False)
mainWindow.bind('<Escape>', lambda e: mainWindow.quit()) # .bind('<Escape>', ...) makes the esc key close the main window
lmain = tk.Label(mainWindow, compound=tk.CENTER, anchor=tk.CENTER, relief=tk.RAISED)
capBTN = tk.Button(mainWindow, text="Capture", command=capSaveWindow)
exitBTN = tk.Button(mainWindow, text="Exit", command=exitWindow)
setTimerBTN = tk.Button(mainWindow, text="Set Timer", command=timerWindow)

lmain.pack()
capBTN.place(bordermode=tk.INSIDE, relx=0.85, rely=0.9, anchor=tk.CENTER, width=150, height=50)
capBTN.focus()
exitBTN.place(bordermode=tk.INSIDE, relx=0.85, rely=0.1, anchor=tk.CENTER, width=150, height=50)
setTimerBTN.place(bordermode=tk.INSIDE, relx=0.85, rely=0.8, anchor=tk.CENTER, width=150, height=50)

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
