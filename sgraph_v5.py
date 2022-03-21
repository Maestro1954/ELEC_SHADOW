import numpy as np
import cv2 as cv
import tkinter as tk
import os
import sys
import threading
import time
from tkinter import filedialog
from PIL import Image, ImageTk

# GLOBAL VARIABLES
img_counter = 0
numFrames = 0
timerCount = 0
cancel = False
timerArmed = False
cameFromCap = False
# Colors
orange = '#faa010'
mint = '#46fcb5'
cherry = '#f01148'
bubblegum = '#f68b82'
eggshell = '#f6f3c0'
eggplant = '#2a082a'
# Filepaths
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

###############################################
################### CAPTURE ###################
###############################################

def capSaveWindow(event = 0):
    global cancel, button0, button1, button2, button3, cameFromCap
    
    if not timerArmed:
        cancel = True
        cameFromCap = True
        button0.place_forget()
        button3.place_forget()
        button1.config(text="SAVE IMAGE", fg=eggshell, command=saveCapture)
        button2.config(text="DISCARD", font=('Ariel', 13), fg=eggshell, command=restoreMenu)
        button2.place(bordermode=tk.INSIDE, y=30, relx=0.85, rely=0.7, anchor=tk.CENTER, width=120, height=20)
    else:
        cancel = False
        button1.place_forget()
        button0.config(text="START TIMER", command=capThread)

def saveCapture(event = 0):
    global img_counter, frame

    _, frame = capture.read()
    screenshot = screenshot_filepath + "/screenshot_{}.png".format(img_counter)
    cv.imwrite(screenshot, frame)
    img_counter += 1
    restoreMenu()

# When timer is armed: thread allows live feed to work independently from 'while' loop in threadedSaveCap()
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
                button3.config(fg=cherry)
            button3.config(text=timerText, command=killTimer) # FIXME
        else:
            timerArmed = False
    capThreadFinished()

def capThreadFinished():
    global button1

    button1.place(bordermode=tk.INSIDE, y=20, relx=0.85, rely=0.8, anchor=tk.CENTER, width=120, height=20)
    capSaveWindow()

###############################################
########### MULTI FRAME CAPTURE ###############
###############################################

def multiFrameWindow(event = 0):
    global cancel, button0, button2, button1, button3, numFrames
    cancel = False

    if timerArmed:
        button3.config(text=timeText, command=timerWindow)
        
    else:
        button3.config(text="RETURN", command=returnThread)
    
    button3.place(bordermode=tk.INSIDE, relx=0.85, y=40, rely=0.6, anchor=tk.CENTER, width=120, height=20)

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

    button0.place(bordermode=tk.INSIDE, y=27, relx=0.85, rely=0.84, anchor=tk.CENTER, width=100, height=30)
    button1.place(bordermode=tk.INSIDE, y=37, relx=0.85, rely=0.75, anchor=tk.CENTER, width=120, height=28)
    button2.place(bordermode=tk.INSIDE, y=47, relx=0.85, rely=0.66, anchor=tk.CENTER, width=100, height=30)

# When timer is armed: thread allows live feed to work independently from 'while' loop in multiFrameCapture()
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
                button3.config(fg=cherry)
            button3.config(text=timerText, command=killTimer) # FIXME
        else:
            timerArmed = False
            button3.place_forget()
            button3.config(text="ADD Seconds", command=addSeconds)

    while numFrames > 0:
        _, frame = capture.read()
        screenshot = screenshot_filepath + "/screenshot_{}.png".format(img_counter)
        cv.imwrite(screenshot, frame)
        img_counter += 1
        numFrames -= 1
        time.sleep(0.1)

    restoreMenu()

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
        
###############################################
################### TIMER #####################
###############################################

def timerWindow(event=0):
    global cancel, button0, button1, button2, button3, button4, timeText, cameFromCap
    cancel = False

    timeText = timerString()
    button2.config(text=timeText, image="", font=('Ariel', 19), fg=eggshell, command=returnThread)

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
    
    if timerArmed:
        button2.place(bordermode=tk.INSIDE, y=25, relx=0.85, rely=0.75, anchor=tk.CENTER, width=120, height=30)
    else:
        button2.place_configure(y=25, rely=0.75, height=30)

    button0.place_configure(y=15, relx=0.894, rely=0.85, width=35, height=30)
    button1.place_configure(bordermode=tk.INSIDE, y=15, relx=0.806, rely=0.85, anchor=tk.CENTER, width=35, height=30)
    button3.place_configure(bordermode=tk.INSIDE, relx=0.894, rely=0.64, anchor=tk.CENTER, width=35, height=30)
    button4.place_configure(bordermode=tk.INSIDE, y=50, relx=0.806, rely=0.62, anchor=tk.CENTER, width=35, height=30)

    button4.lift()

def killTimer():
    global timerCount, timerArmed
    timerCount = 0

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

# Creates string of clock time "00:00" for clock display
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

###############################################
################### EXPORT ####################
###############################################

def export():
    global my_image
    mainWindow.filename = filedialog.askopenfilename(initialdir=screenshot_filepath, title="Select a File", filetypes=(("png files","*.png"),("all files","*.*")))

###############################################
############## HELPER FUNCTIONS ###############
###############################################

def returnThread(event=0):
    t0 = threading.Thread(target=restoreMenu)
    t0.start()

def restoreMenu(event=0):
    global button0, button1, button2, button3, button4, btn_window, cancel, timerArmed, cameFromCap, timerCount, numFrames
    cancel=False
    
    button0.place_forget()
    button1.place_forget()
    button2.place_forget()
    button3.place_forget()
    button4.place_forget()

    button0.config(text="CAPTURE", image="", font=('Ariel', 13), fg=eggshell, command=capSaveWindow)
    button1.config(text="MULTI-FRAME", image="", font=('Ariel', 13), fg=eggshell, command=multiFrameWindow)
    
    if timerCount == 0:
        timerArmed = False
        if numFrames > 0:
            numFrames = 0
        btn_window.config(image=orng_btn_window)
        button2.config(text="SET TIMER", image="", font=('Ariel', 13), fg=eggshell, command=timerWindow)
        button3.config(text="EXPORT", image="", font=('Ariel', 13), fg=eggshell, command=exitWindow)
        button2.place_configure(bordermode=tk.INSIDE, y=30, relx=0.85, rely=0.7, anchor=tk.CENTER, width=120, height=20)
    else:
        timerArmed = True
        if timerCount < 11:
            btn_window.config(image=red_btn_window)
            button3.config(text=timeText, font=('Ariel', 19), image="", fg=cherry, command=timerWindow)
        else:
            btn_window.config(image=green_btn_window)
            button3.config(text=timeText, font=('Ariel', 19), image="", fg=mint, command=timerWindow)
        if button2.winfo_ismapped:
            button2.place_forget()

    button0.place_configure(bordermode=tk.INSIDE, y=10, relx=0.85, rely=0.9, anchor=tk.CENTER, width=120, height=20)
    button1.place_configure(bordermode=tk.INSIDE, y=20, relx=0.85, rely=0.8, anchor=tk.CENTER, width=120, height=20)
    button3.place_configure(bordermode=tk.INSIDE, y=40, relx=0.85, rely=0.6, anchor=tk.CENTER, width=120, height=20)
    if cameFromCap:
        cameFromCap = False
        lmain.after(10, show_frame)


def exitWindow(event=0):
	mainWindow.quit()
    # Add sys.exit(0) here to close window on Raspberry Pi

###############################################
############ WIDGET INITIALIZATION ############
###############################################

mainWindow = tk.Tk()
#mainWindow.geometry("500x200")
#mainWindow.attributes('-fullscreen',True)
mainWindow.resizable(width=False, height=False)
mainWindow.bind('<Escape>', lambda e: mainWindow.quit()) # .bind('<Escape>', ...) makes the esc key close the main window
lmain = tk.Label(mainWindow, compound=tk.CENTER, anchor=tk.CENTER, relief=tk.RAISED)
buttonX = tk.Button(mainWindow, text="EXIT", command=exitWindow, borderwidth=0)
button0 = tk.Button(mainWindow, text="CAPTURE", font=('Ariel', 13), bg=eggplant, fg=eggshell, command=capSaveWindow, borderwidth=0, activebackground=eggplant)
button1 = tk.Button(mainWindow, text="MULTI-FRAME", font=('Ariel', 13), bg=eggplant, fg=eggshell, command=multiFrameWindow, borderwidth=0, activebackground=eggplant)
button2 = tk.Button(mainWindow, text="SET TIMER", font=('Ariel', 13), bg=eggplant, fg=eggshell, command=timerWindow, borderwidth=0, activebackground=eggplant)
button3 = tk.Button(mainWindow, text="EXPORT", font=('Ariel', 13), bg=eggplant, fg=eggshell, command=export, borderwidth=0, activebackground=eggplant)
button4 = tk.Button(mainWindow, text="", fg=eggshell, bg=eggplant, command=addMinutes, borderwidth=0, activebackground=eggplant)

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

# Update live feed frame
def show_frame():
    global cancel, prevImg, button0

    _, frame = capture.read()
    cvimage = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)

    prevImg = Image.fromarray(cvimage)
    imgtk = ImageTk.PhotoImage(image=prevImg)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    if not cancel:
        lmain.after(10, show_frame)

show_frame()
mainWindow.mainloop()
