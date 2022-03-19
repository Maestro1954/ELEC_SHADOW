import numpy as np
import cv2 as cv
import tkinter as tk
import os
import sys
import threading
import time
from PIL import Image, ImageTk # pip install pillow


#__________________GLOBAL VARIABLES__________________

img_counter = 0
numFrames = 0
timerCount = 0
cancel = False
timerArmed = False
cameFromCap = False
cameFromMultFrame = False
threadUsed = False
# Colors
orange = '#faa010'
mint = '#46fcb5'
cherry = '#f01148'
bubblegum = '#f68b82'
eggshell = '#f6f3c0'
eggplant = '#2a082a'
beans = '#532a07'
spinach = '#07453A'
black = '#000000'
# please note the difference in '' and ""
btn_png_filepath = 'C:/Users/adrie/Documents/Documents/UNC_Charlotte/Spring 2022/ECGR-4252 Senior Design II/Button PNGs'
screenshot_filepath = "C:/Users/adrie/Documents/Documents/UNC_Charlotte/Spring 2022/ECGR-4252 Senior Design II/Screenshots"

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

#__________________CAPTURE__________________

def capSaveWindow(event = 0):
    global cancel, button0, button1, button2, button3, cameFromCap
    cameFromCap = True
    
    if not timerArmed:
        button0.place_forget()
        button3.place_forget()
        cancel = True
        button1.config(text="SAVE IMAGE", fg=eggshell, command=saveCapture)
        button2.config(text="DISCARD", fg=eggshell, command=returnFromCapSave)
        button2.place(bordermode=tk.INSIDE, y=30, relx=0.85, rely=0.7, anchor=tk.CENTER, width=120, height=20)
    else:
        cancel = False
        button1.place_forget()
        button0.config(text="START TIMER", command=capThread)

def saveCapture(event = 0):
    global img_counter, frame

    _, frame = capture.read()
    # Create screenshot variable with updating filename: /filepath/screenshot_{img_counter}.png
    screenshot = screenshot_filepath + "/screenshot_{}.png".format(img_counter)
    # Write current frame to screenshot variable
    cv.imwrite(screenshot, frame)
    img_counter += 1
    returnFromCapSave()

def capThread(event=0):
    global button0

    button0.place_forget()
    t3 = threading.Thread(target=threadedSaveCap)
    t3.start()

def threadedSaveCap(event = 0):
    global timerCount, timerArmed, img_counter, button3, cancel, btn_window

    while timerArmed:
        if timerCount > 0:
            timerCount -= 1
            timerText = timerString()
            time.sleep(1)
            if timerCount < 11:
                btn_window.config(image=red_btn_window)
                button3.config(text=timerText, fg=cherry, command=timerRest)
            else:
                btn_window.config(image=green_btn_window)
                button3.config(text=timerText, fg=mint, command=timerRest)  
        else:
            timerArmed = False
    capThreadFinished()

def capThreadFinished():
    global button1, threadUsed
    threadUsed = True

    button1.place(bordermode=tk.INSIDE, y=20, relx=0.85, rely=0.8, anchor=tk.CENTER, width=120, height=20)
    capSaveWindow()

def returnFromCapSave(event = 0):
    global button0, button1, button2, button3, lmain, cancel, threadUsed, cameFromCap
    cancel = False
    cameFromCap = False
    
    mainWindow.bind('<Return>', capSaveWindow)
    restoreBtnPos()
    button0.place(bordermode=tk.INSIDE, y=10, relx=0.85, rely=0.9, anchor=tk.CENTER, width=120, height=20)
    if threadUsed:
        threadUsed = False
        button1.config(text="MULTI-FRAME", command=multiFrameWindow)
    button3.place(bordermode=tk.INSIDE, y=40, relx=0.85, rely=0.6, anchor=tk.CENTER, width=120, height=20)
    button1.place(bordermode=tk.INSIDE, y=20, relx=0.85, rely=0.8, anchor=tk.CENTER, width=120, height=20)
    lmain.after(10, show_frame)

#__________________MULTI FRAME CAPTURE__________________

def multiFrameWindow(event = 0):
    global cancel, button0, button2, button1, button3, numFrames, cameFromMultFrame
    cancel = False
    cameFromMultFrame = True

    if timerArmed:
        button3.config(text=timeText, command=timerWindow)
        button3.place(bordermode=tk.INSIDE, relx=0.85, y=40, rely=0.6, anchor=tk.CENTER, width=120, height=20)
    else:
        button3.place_forget()

    frameString = str(numFrames)
    frameText = "FRAMES: " + frameString
    button1.config(text=frameText, font=('Ariel', 15), command=multiCapThread)

    if numFrames == 10:
        button2.config(image=dim_up_arrow, command=addFrame)
    else:
        button2.config(image=up_arrow, command=addFrame)
    if numFrames == 0:
        button0.config(image=dim_down_arrow, command=subtractFrame)
    else:
        button0.config(image=down_arrow, command=subtractFrame)

    if not timerArmed:
        button0.place(bordermode=tk.INSIDE, y=15, relx=0.85, rely=0.84, anchor=tk.CENTER, width=100, height=30)
        button1.place(bordermode=tk.INSIDE, y=25, relx=0.85, rely=0.75, anchor=tk.CENTER, width=120, height=28)
        button2.place(bordermode=tk.INSIDE, y=35, relx=0.85, rely=0.66, anchor=tk.CENTER, width=100, height=30)
    else:
        button0.place(bordermode=tk.INSIDE, y=27, relx=0.85, rely=0.84, anchor=tk.CENTER, width=100, height=30)
        button1.place(bordermode=tk.INSIDE, y=37, relx=0.85, rely=0.75, anchor=tk.CENTER, width=120, height=28)
        button2.place(bordermode=tk.INSIDE, y=47, relx=0.85, rely=0.66, anchor=tk.CENTER, width=100, height=30)

def multiCapThread(event = 0):
    t1 = threading.Thread(target=multiFrameCapture)
    t1.start()

def multiFrameCapture(event = 0):
    global frame, numFrames, img_counter, timerArmed, timerCount, timerText, button0, button1, button2, button3, btn_window


    button2.config(image=dim_up_arrow, command="")
    button1.config(command="")
    button0.config(image=dim_down_arrow, command="")
    while timerArmed:
        if timerCount > 0:
            timerCount -= 1
            timerText = timerString()
            time.sleep(1)
            if timerCount < 11:
                btn_window.config(image=red_btn_window)
                button3.config(text=timerText, fg=cherry, command=timerRest)
            else:
                button3.config(text=timerText, command=timerRest) 
        else:
            timerArmed = False
            button3.place_forget()
            button3.config(text="ADD Seconds", command=addSeconds)

    while numFrames > 0:
        _, frame = capture.read()
        # Create screenshot variable with updating filename: /filepath/screenshot_{img_counter}.png
        screenshot = screenshot_filepath + "/screenshot_{}.png".format(img_counter)
        # Write current frame to screenshot variable
        cv.imwrite(screenshot, frame)
        img_counter += 1
        numFrames -= 1
        time.sleep(0.1)
    
    restoreBtnPos()
    button3.place(bordermode=tk.INSIDE, y=40, relx=0.85, rely=0.6, anchor=tk.CENTER, width=120, height=20)
        
# ______________TIMER__________________

def timerWindow(event=0):
    global cancel, button0, button1, button2, button3, button4, timeText, cameFromCap
    cancel = False

    timeText = timerString()
    button2.config(text=timeText, image="", font=('Ariel', 19), fg=eggshell, command=setTimerThread)

    if timerCount == 600:
        button3.config(image=dim_up_arrow, command=addSeconds)
        button4.config(image=dim_up_arrow)
    else:
        button3.config(image=up_arrow, command=addSeconds)
        button4.config(image=up_arrow)
    if timerCount == 0:
        button1.config(image=dim_down_arrow, command=subtractMinutes)
        button0.config(image=dim_down_arrow, command=subtractSeconds)
    elif timerCount < 60:
        button1.config(image=dim_down_arrow, command=subtractMinutes)
        button0.config(image=down_arrow, command=subtractSeconds)
    else:
        button1.config(image=down_arrow, command=subtractMinutes)
        button0.config(image=down_arrow, command=subtractSeconds)
    

    button0.place_configure(y=15, relx=0.894, rely=0.85, width=35, height=30)
    if cameFromCap:
        button1.place_configure(y=0, relx=0.78, rely=0.85, width=35, height=30)
        cameFromCap = False
    else:
        button1.place_configure(y=15, relx=0.806, rely=0.85, width=35, height=30)
    if timerArmed:
        button2.place(bordermode=tk.INSIDE, y=25, relx=0.85, rely=0.75, anchor=tk.CENTER, width=120, height=30)
    else:
        button2.place_configure(y=25, rely=0.75, height=30)
    button3.place(bordermode=tk.INSIDE, relx=0.894, rely=0.64, anchor=tk.CENTER, width=35, height=30)
    button4.place(bordermode=tk.INSIDE, y=50, relx=0.806, rely=0.62, anchor=tk.CENTER, width=35, height=30)

    button4.lift()

def timerRest():
    global timerCount, numFrames
    timerCount = 0
    numFrames = 0


def setTimerThread(event=0):
    t2 = threading.Thread(target=setTimer)
    t2.start()

def setTimer(event=0):
    global button4, button3, button2, button1, button0, timeText, cancel, timerArmed, lmain, timerCount
    cancel = False
    
    button4.place_forget()
    if timerCount != 0:
        timerArmed = True
        mainWindow.bind('<Return>', timerWindow)
        btn_window.config(image=green_btn_window)
        button3.config(text=timeText, font=('Ariel', 19), image="", fg=mint, command=timerWindow)
    else:
        timerArmed = False
    restoreBtnPos()

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
    elif timerCount == 60:
        timerCount = 0
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

    return minString + " : " + secString
#______________________________________

def restoreBtnPos(event=0):
    global button0, button1, button2, button3, timerArmed, btn_window, cameFromMultFrame

    button0.config(text="CAPTURE", image="", font=('Ariel', 13), fg=eggshell, command=capSaveWindow)
    button1.config(text="MULTI-FRAME", image="", font=('Ariel', 13), fg=eggshell, command=multiFrameWindow) 
    if cameFromMultFrame or (not timerArmed):
        cameFromMultFrame = False
        btn_window.config(image=orng_btn_window)
        button2.config(text="SET TIMER", image="", font=('Ariel', 13), fg=eggshell, command=timerWindow)
        button3.config(text="EXPORT", image="", font=('Ariel', 13), fg=eggshell, command=exitWindow)
    if timerArmed:
        button2.place_forget()
    else:
        button2.place_configure(bordermode=tk.INSIDE, y=30, relx=0.85, rely=0.7, anchor=tk.CENTER, width=120, height=20)
    button0.place_configure(bordermode=tk.INSIDE, y=10, relx=0.85, rely=0.9, anchor=tk.CENTER, width=120, height=20)
    button1.place_configure(bordermode=tk.INSIDE, y=20, relx=0.85, rely=0.8, anchor=tk.CENTER, width=120, height=20)
    button3.place_configure(bordermode=tk.INSIDE, y=40, relx=0.85, rely=0.6, anchor=tk.CENTER, width=120, height=20)

    

def exitWindow(event=0):
	mainWindow.quit()
    # Add sys.exit(0) here to close window on Raspberry Pi

mainWindow = tk.Tk()
#mainWindow.geometry("500x200")
#mainWindow.attributes('-fullscreen',True)
mainWindow.resizable(width=False, height=False)
mainWindow.bind('<Escape>', lambda e: mainWindow.quit()) # .bind('<Escape>', ...) makes the esc key close the main window
lmain = tk.Label(mainWindow, compound=tk.CENTER, anchor=tk.CENTER, relief=tk.RAISED)
buttonX = tk.Button(mainWindow, text="Exit", command=exitWindow, borderwidth=0)
button0 = tk.Button(mainWindow, text="CAPTURE", font=('Ariel', 13), bg=eggplant, fg=eggshell, command=capSaveWindow, borderwidth=0, activebackground=eggplant)
button1 = tk.Button(mainWindow, text="MULTI-FRAME", font=('Ariel', 13), bg=eggplant, fg=eggshell, command=multiFrameWindow, borderwidth=0, activebackground=eggplant)
button2 = tk.Button(mainWindow, text="SET TIMER", font=('Ariel', 13), bg=eggplant, fg=eggshell, command=timerWindow, borderwidth=0, activebackground=eggplant)
button3 = tk.Button(mainWindow, text="EXPORT", font=('Ariel', 13), bg=eggplant, fg=eggshell, command=exitWindow, borderwidth=0, activebackground=eggplant)
button4 = tk.Button(mainWindow, text="ADD Minutes", bg=eggplant, command=addMinutes, borderwidth=0, activebackground=eggplant)

up_arrow = tk.PhotoImage(file=(btn_png_filepath + '/up_arrow.png'))
down_arrow = tk.PhotoImage(file=(btn_png_filepath + '/down_arrow.png'))
dim_up_arrow = tk.PhotoImage(file=(btn_png_filepath + '/dim_up_arrow.png'))
dim_down_arrow = tk.PhotoImage(file=(btn_png_filepath + '/dim_down_arrow.png'))
orng_btn_window = tk.PhotoImage(file=(btn_png_filepath + '/orng_btn_window.png'))
green_btn_window = tk.PhotoImage(file=(btn_png_filepath + '/green_btn_window.png'))
red_btn_window = tk.PhotoImage(file=(btn_png_filepath + '/red_btn_window.png'))

btn_window = tk.Label(mainWindow, image=orng_btn_window)
btn_window.place(bordermode=tk.INSIDE, y=1, relx=0.85, rely=0.8, anchor=tk.CENTER, width=150, height=164)

lmain.pack()
buttonX.place(bordermode=tk.INSIDE, relx=0.85, rely=0.1, anchor=tk.CENTER, width=150, height=50)
button0.place(bordermode=tk.INSIDE, y=10, relx=0.85, rely=0.9, anchor=tk.CENTER, width=120, height=20)
button1.place(bordermode=tk.INSIDE, y=20, relx=0.85, rely=0.8, anchor=tk.CENTER, width=120, height=20)
button2.place(bordermode=tk.INSIDE, y=30, relx=0.85, rely=0.7, anchor=tk.CENTER, width=120, height=20)
button3.place(bordermode=tk.INSIDE, y=40, relx=0.85, rely=0.6, anchor=tk.CENTER, width=120, height=20)

button0.lift()
button1.lift()
button2.lift()
button3.lift()

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
