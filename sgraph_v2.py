# import the opencv library
import numpy as np
import cv2 as cv
import tkinter as tk
import os
import sys
from PIL import Image, ImageTk # pip install pillow

img_counter = 0
cancel = False

def prompt_ok(event = 0):
    global cancel, button, button1, button2
    cancel = True

    button.place_forget()
    button1 = tk.Button(mainWindow, text="Save Image", command=saveAndReturn)
    button2 = tk.Button(mainWindow, text="Discard", command=resume)
    button1.place(anchor=tk.CENTER, relx=0.2, rely=0.9, width=150, height=50)
    button2.place(anchor=tk.CENTER, relx=0.8, rely=0.9, width=150, height=50)
    button1.focus()

def saveAndReturn(event = 0):
	global img_counter

	# Create screenshot variable with updating filename: /filepath/screenshot_{img_counter}.png
	screenshot = "C:/Users/adrie/Documents/Documents/UNC_Charlotte/Spring 2022/ECGR-4252 Senior Design II/Code/Tkinter Code/Screenshots/screenshot_{}.png".format(img_counter)
	# Write current frame to screenshot variable
	cv.imwrite(screenshot, frame)
	img_counter += 1
	resume()

def resume(event = 0):
    global button1, button2, button, lmain, cancel

    cancel = False

    button1.place_forget()
    button2.place_forget()

    mainWindow.bind('<Return>', prompt_ok)
    button.place(bordermode=tk.INSIDE, relx=0.5, rely=0.9, anchor=tk.CENTER, width=300, height=50)
    lmain.after(10, show_frame)

def exitWindow(event=0):
	mainWindow.quit()

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

mainWindow = tk.Tk()
mainWindow.resizable(width=False, height=False)
mainWindow.bind('<Escape>', lambda e: mainWindow.quit()) # .bind('<Escape>', ...) makes the esc key close the main window
lmain = tk.Label(mainWindow, compound=tk.CENTER, anchor=tk.CENTER, relief=tk.RAISED)
button = tk.Button(mainWindow, text="Capture", command=prompt_ok)
button_changeCam = tk.Button(mainWindow, text="Exit", command=exitWindow)

lmain.pack()
button.place(bordermode=tk.INSIDE, relx=0.5, rely=0.9, anchor=tk.CENTER, width=300, height=50)
button.focus()
button_changeCam.place(bordermode=tk.INSIDE, relx=0.85, rely=0.1, anchor=tk.CENTER, width=150, height=50)

def show_frame():
    global cancel, prevImg, button

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
