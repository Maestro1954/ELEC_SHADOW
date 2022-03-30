import numpy as np
import cv2 as cv
import tkinter as tk
import os
import shutil
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
beans = '#532a07'
eggplant = '#2a082a'
# Filepaths
btn_png_filepath = '/home/pi/ELEC_SHADOW/Button PNGs'
screenshot_filepath = "/home/pi/ELEC_SHADOW/Screenshots"
usbFilepath = "/home/pi/ELEC_SHADOW/USB File"

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
    global cancel, frame, cameFromCap
    
    if not timerArmed:
        cancel = True
        _, frame = capture.read()
        cameFromCap = True
        button0.place_forget()
        button3.place_forget()
        button1.config(text="SAVE IMAGE", fg=eggshell, command=saveCapture)
        button2.config(text="DISCARD", font=('Ariel', 13), fg=eggshell, command=restoreMenu)
        button2.place(bordermode=tk.INSIDE, y=30, relx=0.85, rely=0.7, anchor=tk.CENTER, width=120, height=20)
    else:
        cancel = False
        button1.place_forget()
        buttonX.config(text="RETURN", command=restoreMenu)
        button0.config(text="START TIMER", command=capThread)

def saveCapture(event = 0):
    global img_counter, frame, cancel

    screenshot = screenshot_filepath + "/screenshot_{}.png".format(img_counter)
    cv.imwrite(screenshot, frame)
    img_counter += 1
    restoreMenu()

# When timer is armed: thread allows live feed to work independently from 'while' loop in threadedSaveCap()
def capThread(event=0):
    global button0, button2

    button0.config(fg=beans, command="")
    button2.config(fg=beans, command="")
    t3 = threading.Thread(target=threadedSaveCap)
    t3.start()

def threadedSaveCap(event = 0):
    global timerCount, timerArmed, img_counter, cancel, btn_window, time_display

    if timerArmed:
        buttonX.config(fg=beans, command="")
    
    while timerArmed:
        if timerCount > 0:
            timerCount -= 1
            timerText = timerString()
            time.sleep(1)
            if timerCount < 11:
                btn_window.config(image=red_btn_window)
                btnX_window.config(image=red_btnX)
                time_display.config(fg=cherry)
            time_display.config(text=timerText)
        else:
            timerArmed = False
    
    button1.place(bordermode=tk.INSIDE, y=20, relx=0.85, rely=0.8, anchor=tk.CENTER, width=120, height=20)
    capSaveWindow()

###############################################
########### MULTI FRAME CAPTURE ###############
###############################################

def multiFrameWindow(event = 0):
    global cancel, numFrames, time_display, frame_display, frameText
    cancel = False

    button2.place_forget()
    
    frameString = str(numFrames)
    if numFrames < 10:
        frameText = "0" + frameString
    else:
        frameText = frameString
    frame_display.config(text=frameText, font=('Ariel', 15), fg=eggshell)

    if numFrames == 10:
        button1.config(image=dim_up_arrow, command=addFrame)
    else:
        button1.config(image=up_arrow, command=addFrame)
    if numFrames == 0:
        button0.config(image=dim_down_arrow, command=subtractFrame)
    else:
        button0.config(image=down_arrow, command=subtractFrame)
    
    if timerArmed:
        time_display.config(text=timeText)
        time_display.place(bordermode=tk.INSIDE, relx=0.85, y=40, rely=0.6, anchor=tk.CENTER, width=120, height=20)
        button3.config(text="CAPTURE:", image="", command=multiCapTimerWindow)
    else:
        button3.config(text="CAPTURE:", image="", command=multiCapThread)
    
    buttonX.config(text="RETURN", command=restoreMenu)
    button3.place_configure(bordermode=tk.INSIDE, x=2, y=32, relx=0.82, rely=0.74, anchor=tk.CENTER, width=80, height=20) # capture
    button0.place_configure(bordermode=tk.INSIDE, x=3, y=14, relx=0.91, rely=0.84, anchor=tk.CENTER, width=25, height=22) # subtract
    frame_display.place_configure(bordermode=tk.INSIDE, x=3, y=32, relx=0.91, rely=0.74, anchor=tk.CENTER, width=30, height=20) # frameText
    button1.place_configure(bordermode=tk.INSIDE, x=3, y=50, relx=0.91, rely=0.64, anchor=tk.CENTER, width=25, height=22) # add

def multiCapTimerWindow(event = 0):
    global button0, button1, button2, button3, cancel, frame_display, timerCount, frameText
    cancel = False
    
    button0.place_forget()
    button1.place_forget()
    button3.place_forget()
    frame_display.place_forget()

    button0.config(text="START TIMER", image="", command=multiCapThread)

    if timerCount < 11:
        frame_display.config(text="FRAMES: " + frameText, font=('Ariel', 13), fg=cherry)
    else:
        frame_display.config(text="FRAMES: " + frameText, font=('Ariel', 13), fg=mint)

    button0.place_configure(bordermode=tk.INSIDE, y=10, relx=0.85, rely=0.9, anchor=tk.CENTER, width=120, height=20)
    frame_display.place_configure(bordermode=tk.INSIDE, y=20, relx=0.85, rely=0.8, anchor=tk.CENTER, width=120, height=20)
    button2.place_configure(bordermode=tk.INSIDE, y=30, relx=0.85, rely=0.7, anchor=tk.CENTER, width=120, height=20)

# When timer is armed: thread allows live feed to work independently from 'while' loop in multiFrameCapture()
def multiCapThread(event = 0):
    t1 = threading.Thread(target=multiFrameCapture)
    t1.start()

def multiFrameCapture(event = 0):
    global frame, numFrames, img_counter, timerArmed, timerCount, timerText, btn_window, time_display, frame_display

    if timerArmed:
        button0.config(fg=beans, command="")
        button2.config(fg=beans, command="")
        buttonX.config(fg=beans, command="")
    
    while timerArmed:
        if timerCount > 0:
            timerCount -= 1
            timerText = timerString()
            time.sleep(1)
            if timerCount < 11:
                btn_window.config(image=red_btn_window)
                btnX_window.config(image=red_btnX)
                time_display.config(fg=cherry)
                frame_display.config(fg=cherry)
            time_display.config(text=timerText)
        else:
            timerArmed = False
            time_display.place_forget()

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
    global cancel, button4, timeText, time_display, frame_display
    cancel = False

    if frame_display.winfo_ismapped():
        frame_display.place_forget()

    timeText = timerString()
    time_display.config(text=timeText, font=('Ariel', 19), fg=eggshell)
    button3.config(text="SET TIMER", command=restoreMenu)

    if timerCount == 600:
        button2.config(image=dim_up_arrow, command=addSeconds)
        button4.config(image=dim_up_arrow)
    else:
        button2.config(image=up_arrow, command=addSeconds)
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
    
    if not button3.winfo_ismapped():
        button3.place_configure(bordermode=tk.INSIDE, y=40, relx=0.85, rely=0.6, anchor=tk.CENTER, width=120, height=20) # SET TIMER

    button0.place_configure(bordermode=tk.INSIDE, y=15, relx=0.886, rely=0.85, anchor=tk.CENTER, width=25, height=22) # sub sec
    button1.place_configure(bordermode=tk.INSIDE, y=15, relx=0.811, rely=0.85, anchor=tk.CENTER, width=25, height=22) # sub min
    time_display.place_configure(bordermode=tk.INSIDE, y=33, relx=0.85, rely=0.75, anchor=tk.CENTER, width=120, height=30) # timeText
    button2.place_configure(bordermode=tk.INSIDE, y=51, relx=0.886, rely=0.65, anchor=tk.CENTER, width=25, height=22) # add sec
    button4.place_configure(bordermode=tk.INSIDE, y=51, relx=0.811, rely=0.65, anchor=tk.CENTER, width=25, height=22) # add min

    button4.lift()

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

def export(): # FIXME
    global usbFilepath

    mainWindow.filename = filedialog.askopenfilenames(initialdir=screenshot_filepath, title="Select a File", filetypes=(("png files","*.png"),("all files","*.*")))
    for f in mainWindow.filename:
        shutil.move(f, usbFilepath)  

###############################################
################ RESTORE MENU #################
###############################################

def restoreMenu(event=0):
    global btn_window, time_display, frame_display, cancel, timerArmed, cameFromCap, timerCount, numFrames 
    cancel=False
    
    button0.place_forget()
    button1.place_forget()
    button2.place_forget()
    button3.place_forget()
    button4.place_forget()
    time_display.place_forget()
    frame_display.place_forget()

    buttonX.configure(text="EXIT", font=('Ariel', 13), fg=eggshell, command=exitWindow)
    button0.config(text="CAPTURE", image="", font=('Ariel', 13), fg=eggshell, command=capSaveWindow)
    button1.config(text="MULTI-FRAME", image="", font=('Ariel', 13), fg=eggshell, command=multiFrameWindow)
    button2.config(text="SET TIMER", image="", font=('Ariel', 13), fg=eggshell, command=timerWindow)

    if timerCount == 0:
        timerArmed = False
        if numFrames > 0:
            numFrames = 0
        btn_window.config(image=orng_btn_window)
        btnX_window.config(image=orng_btnX)
        button3.config(text="EXPORT", image="", font=('Ariel', 13), fg=eggshell, command=export)
        button3.place_configure(bordermode=tk.INSIDE, y=40, relx=0.85, rely=0.6, anchor=tk.CENTER, width=120, height=20)
    else:
        timerArmed = True
        if timerCount < 11:
            btn_window.config(image=red_btn_window)
            btnX_window.config(image=red_btnX)
            time_display.config(text=timeText, font=('Ariel', 19), fg=cherry)
        else:
            btn_window.config(image=green_btn_window)
            btnX_window.config(image=green_btnX)
            time_display.config(text=timeText, font=('Ariel', 19), fg=mint)
        time_display.place_configure(bordermode=tk.INSIDE, y=40, relx=0.85, rely=0.6, anchor=tk.CENTER, width=120, height=20)

    button0.place_configure(bordermode=tk.INSIDE, y=10, relx=0.85, rely=0.9, anchor=tk.CENTER, width=120, height=20)
    button1.place_configure(bordermode=tk.INSIDE, y=20, relx=0.85, rely=0.8, anchor=tk.CENTER, width=120, height=20)
    button2.place_configure(bordermode=tk.INSIDE, y=30, relx=0.85, rely=0.7, anchor=tk.CENTER, width=120, height=20)

    if cameFromCap:
        cameFromCap = False
        lmain.after(10, show_frame)

def exitWindow(event=0):
	mainWindow.quit()
	sys.exit(0)

###############################################
############ WIDGET INITIALIZATION ############
###############################################

mainWindow = tk.Tk()
#mainWindow.geometry("500x200")
#mainWindow.attributes('-fullscreen',True)
mainWindow.resizable(width=False, height=False)
lmain = tk.Label(mainWindow, compound=tk.CENTER, anchor=tk.CENTER, relief=tk.RAISED)
buttonX = tk.Button(mainWindow, text="EXIT", font=('Ariel', 13), bg=eggplant, fg=eggshell, command=exitWindow, borderwidth=0, highlightthickness=0, activebackground=eggplant)
button0 = tk.Button(mainWindow, text="CAPTURE", font=('Ariel', 13), bg=eggplant, fg=eggshell, command=capSaveWindow, borderwidth=0, highlightthickness=0, activebackground=eggplant)
button1 = tk.Button(mainWindow, text="MULTI-FRAME", font=('Ariel', 13), bg=eggplant, fg=eggshell, command=multiFrameWindow, borderwidth=0, highlightthickness=0, activebackground=eggplant)
button2 = tk.Button(mainWindow, text="SET TIMER", font=('Ariel', 13), bg=eggplant, fg=eggshell, command=timerWindow, borderwidth=0, highlightthickness=0, activebackground=eggplant)
button3 = tk.Button(mainWindow, text="EXPORT", font=('Ariel', 13), bg=eggplant, fg=eggshell, command=export, borderwidth=0, highlightthickness=0, activebackground=eggplant)
button4 = tk.Button(mainWindow, text="", fg=eggshell, bg=eggplant, command=addMinutes, borderwidth=0, highlightthickness=0, activebackground=eggplant)

up_arrow = tk.PhotoImage(file=(btn_png_filepath + '/up_arrow.png'))
down_arrow = tk.PhotoImage(file=(btn_png_filepath + '/down_arrow.png'))
dim_up_arrow = tk.PhotoImage(file=(btn_png_filepath + '/dim_up_arrow.png'))
dim_down_arrow = tk.PhotoImage(file=(btn_png_filepath + '/dim_down_arrow.png'))
orng_btn_window = tk.PhotoImage(file=(btn_png_filepath + '/orng_btn_window.png'))
green_btn_window = tk.PhotoImage(file=(btn_png_filepath + '/green_btn_window.png'))
red_btn_window = tk.PhotoImage(file=(btn_png_filepath + '/red_btn_window.png'))
orng_btnX = tk.PhotoImage(file=(btn_png_filepath + '/orng_btnX.png'))
green_btnX = tk.PhotoImage(file=(btn_png_filepath + '/green_btnX.png'))
red_btnX = tk.PhotoImage(file=(btn_png_filepath + '/red_btnX.png'))

btn_window = tk.Label(mainWindow, image=orng_btn_window)
btnX_window = tk.Label(mainWindow, image=orng_btnX)
time_display = tk.Label(mainWindow, fg=eggshell, bg=eggplant)
frame_display = tk.Label(mainWindow, fg=eggshell, bg=eggplant)
btn_window.place(bordermode=tk.INSIDE, y=1, relx=0.85, rely=0.8, anchor=tk.CENTER, width=150, height=164)
btnX_window.place(bordermode=tk.INSIDE, relx=0.85, rely=0.1, anchor=tk.CENTER, width=150, height=49)

lmain.pack()
buttonX.place(bordermode=tk.INSIDE, relx=0.85, rely=0.1, anchor=tk.CENTER, width=120, height=20)
button0.place(bordermode=tk.INSIDE, y=10, relx=0.85, rely=0.9, anchor=tk.CENTER, width=120, height=20)
button1.place(bordermode=tk.INSIDE, y=20, relx=0.85, rely=0.8, anchor=tk.CENTER, width=120, height=20)
button2.place(bordermode=tk.INSIDE, y=30, relx=0.85, rely=0.7, anchor=tk.CENTER, width=120, height=20)
button3.place(bordermode=tk.INSIDE, y=40, relx=0.85, rely=0.6, anchor=tk.CENTER, width=120, height=20)

buttonX.lift()
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
