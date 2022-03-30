# import the opencv library
import numpy as np
import cv2 as cv
import tkinter as tk
import os
import sys
import threading
import time
from PIL import Image, ImageTk # pip install pillow


img_counter = 500
numFrames = 0
timerCount = 0
cancel = False
timerArmed = False
threadUsed = False

# define a video capture object
#capture = cv.VideoCapture(0)

cmd = 'raspistill -n -t 1000 -w 1024 -h 768 -a 1036 -ae +25+25 -o test2.jpg'

capture = os.system(cmd)

#capture = set(cv.CAP_PROP_FRAME_WIDTH, 640) #no go as it changes the entirety of the function

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
    
    if not timerArmed:
        button2.place_forget()
        cancel = True
        button0.config(text="Save Image", command=saveCapture)
        button1.config(text="Discard", command=returnFromCapSave)
        button0.focus()
    else:
        cancel = False
        button0.config(text="Start Timer", command=capThread)
        button1.place_forget()
        button1.config(text="Multi-Frame", command=multiFrameWindow)


def saveCapture(event = 0):
    global img_counter, frame

    _, frame = capture.read()
    # Create screenshot variable with updating filename: /filepath/screenshot_{img_counter}.png
    screenshot = "D:/SeniorDesign/screenshot_{}.png".format(img_counter)
    # Write current frame to screenshot variable
    cv.imwrite(screenshot, frame)
    img_counter += 1
    returnFromCapSave()

def capThread(event=0):
    t3 = threading.Thread(target=threadedSaveCap)
    t3.start()

def threadedSaveCap(event = 0):
    global timerCount, timerArmed, img_counter, button1, cancel

    while timerArmed:
        if timerCount > 0:
            timerCount -= 1
            timerText = timerString()
            time.sleep(1)
            button2.config(text=timerText, command=timerRest)  
        else:
            timerArmed = False
    capThreadFinished()

def capThreadFinished():
    global button1, threadUsed
    threadUsed = True

    button1.place(bordermode=tk.INSIDE, relx=0.85, rely=0.8, anchor=tk.CENTER, width=150, height=50)
    capSaveWindow()

def returnFromCapSave(event = 0):
    global button0, button1, button2, lmain, cancel, threadUsed
    cancel = False
    
    mainWindow.bind('<Return>', capSaveWindow)
    button0.config(text="Capture", command=capSaveWindow)
    button2.config(text="Set Timer", command=timerWindow)
    button1.config(text="Multi-Frame", command=multiFrameWindow)
    button2.place(bordermode=tk.INSIDE, relx=0.85, rely=0.7, anchor=tk.CENTER, width=150, height=50)
    if threadUsed:
        threadUsed = False
        #button2.place(bordermode=tk.INSIDE, relx=0.85, rely=0.7, anchor=tk.CENTER, width=150, height=50)
        button1.config(text="Multi-Frame", command=multiFrameWindow)
    button1.place(bordermode=tk.INSIDE, relx=0.85, rely=0.8, anchor=tk.CENTER, width=150, height=50)
    lmain.after(10, show_frame)

def multiFrameWindow(event = 0):
    global cancel, button0, button2, button1, button3, numFrames
    cancel = False

    if timerArmed:
        button3.config(text=timeText, command=timerWindow)
        button3.place(bordermode=tk.INSIDE, relx=0.85, rely=0.6, anchor=tk.CENTER, width=150, height=50)
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
    global frame, numFrames, img_counter, timerArmed, timerCount, timerText

    while timerArmed:
        if timerCount > 0:
            timerCount -= 1
            timerText = timerString()
            time.sleep(1)
            button3.config(text=timerText, command=timerRest)  
        else:
            timerArmed = False
            button3.place_forget()
            button3.config(text="ADD Seconds", command=addSeconds)

    while numFrames > 0:
        _, frame = capture.read()
        # Create screenshot variable with updating filename: /filepath/screenshot_{img_counter}.png
        screenshot = "D:/SeniorDesign/screenshot_{}.png".format(img_counter)
        # Write current frame to screenshot variable
        cv.imwrite(screenshot, frame)
        img_counter += 1
        numFrames -= 1
        time.sleep(0.1)
    button2.config(text="Set Timer", command=timerWindow)
    button1.config(text="Multi-Frame", command=multiFrameWindow)
    button0.config(text="Capture", command=capSaveWindow)
        

# ______________TIMER__________________

def timerWindow(event=0):
    global cancel, button0, button1, button2, button3, button4, timeText
    cancel = False

    timeText = timerString()
    button2.config(text=timeText, command=setTimerThread)
    button1.config(text="SUB Seconds", command=subtractSeconds)
    button0.config(text="SUB Minutes", command=subtractMinutes)
    button3.config(text="ADD Seconds", command=addSeconds)
    button3.place(bordermode=tk.INSIDE, relx=0.85, rely=0.6, anchor=tk.CENTER, width=150, height=50)
    button4.place(bordermode=tk.INSIDE, relx=0.85, rely=0.5, anchor=tk.CENTER, width=150, height=50)
    button2.focus()

def timerRest():
    global timerCount, numFrames
    timerCount = 0
    numFrames = 0

def setTimerThread(event=0):
    t2 = threading.Thread(target=setTimer)
    t2.start()

def setTimer(event=0):
    global button4, button3, button2, button1, button0, timeText, cancel, timerArmed, lmain
    cancel = False
    timerArmed = True

    button4.place_forget()
    button3.place_forget()
    mainWindow.bind('<Return>', timerWindow)
    button2.config(command=timerWindow)
    button1.config(text="Multi-Frame", command=multiFrameWindow)
    button0.config(text="Capture", command=capSaveWindow)

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

def addSeconds():
    global timerCount

    if timerCount < 600:
        timerCount += 1
    timerWindow()

def subtractSeconds():
    global timerCount

    if timerCount > 0:
        timerCount -= 1
    timerWindow()

def addMinutes():
    global timerCount

    if timerCount < 540:
        timerCount += 60
    else:
        timerCount = 600
    timerWindow()

def subtractMinutes():
    global timerCount

    if timerCount > 60:
        timerCount -= 60
    timerWindow()

def timerString():
    global timerCount

    floatMins = timerCount/60
    minutes = int(floatMins)
    seconds = timerCount - (minutes * 60)

    if minutes < 10:
        minString = "0"
        minString += str(minutes)
    else:
        minString = str(minutes)
    if seconds < 10:
        secString = "0"
        secString += str(seconds)
    else:
        secString = str(seconds)

    return minString + ":" + secString
#______________________________________

def exitWindow(event=0):
	mainWindow.quit()
	# Add sys.exit(0) here to close window on Raspberry Pi

mainWindow = tk.Tk()
#mainWindow.attributes('-fullscreen',True) # makes the window full screen 
mainWindow.resizable(width=False, height=False)
mainWindow.bind('<Escape>', lambda e: mainWindow.quit()) # .bind('<Escape>', ...) makes the esc key close the main window
lmain = tk.Label(mainWindow, compound=tk.CENTER, anchor=tk.CENTER, relief=tk.RAISED)
buttonX = tk.Button(mainWindow, text="Exit", command=exitWindow)
button0 = tk.Button(mainWindow, text="Capture", command=capSaveWindow)
button1 = tk.Button(mainWindow, text="Multi-Frame", command=multiFrameWindow)
button2 = tk.Button(mainWindow, text="Set Timer", command=timerWindow)
button4 = tk.Button(mainWindow, text="ADD Minutes", command=addMinutes)
button3 = tk.Button(mainWindow, text="ADD Seconds", command=addSeconds)

lmain.pack()
buttonX.place(bordermode=tk.INSIDE, relx=0.85, rely=0.1, anchor=tk.CENTER, width=150, height=50)
button0.place(bordermode=tk.INSIDE, relx=0.85, rely=0.9, anchor=tk.CENTER, width=150, height=50)
button0.focus()
button2.place(bordermode=tk.INSIDE, relx=0.85, rely=0.7, anchor=tk.CENTER, width=150, height=50)
button1.place(bordermode=tk.INSIDE, relx=0.85, rely=0.8, anchor=tk.CENTER, width=150, height=50)

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
