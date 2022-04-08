import numpy as np
import cv2 as cv
import tkinter as tk
import os
import shutil
import sys
import threading
import time
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


# GLOBAL VARIABLES
img_counter = 0
mult_frame_counter = 0
mult_frame_session = 0
numFrames = 0
timerCount = 0
mfTimeCount = 0
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
    capture.set(3, 1280)
    capture.set(4, 720)

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
        buttonX.config(fg=beans, command="")
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
            timerText = clockString(timerCount)
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
    global cancel, time_display, frame_display, frameText, numFrames
    cancel = False

    if timerArmed:
        time_display.place_forget()

    frameTimeText = clockString(mfTimeCount)
    numFrames = mfTimeCount * 10
    frame_display.config(text=frameTimeText, font=('Ariel', 19), fg=eggshell)
    button3.config(text="SET FRAMES", image="", command=multiCapTimerWindow)
    
    if mfTimeCount == 900:
        button2.config(image=dim_up_arrow, command=addSecondsMF)
        button4.config(image=dim_up_arrow, command=addMinutesMF)
    else:
        button2.config(image=up_arrow, command=addSecondsMF)
        button4.config(image=up_arrow, command=addMinutesMF)

    if mfTimeCount == 0:
        button1.config(image=dim_down_arrow, command=subtractMinutesMF)
        button0.config(image=dim_down_arrow, command=subtractSecondsMF)
    elif mfTimeCount < 60:
        button1.config(image=dim_down_arrow, command=subtractMinutesMF)
        button0.config(image=down_arrow, command=subtractSecondsMF)
    else:
        button1.config(image=down_arrow, command=subtractMinutesMF)
        button0.config(image=down_arrow, command=subtractSecondsMF)

    buttonX.config(text="RETURN", command=restoreMenu) # RETURN    
    button3.place_configure(bordermode=tk.INSIDE, y=40, relx=0.85, rely=0.6, anchor=tk.CENTER, width=120, height=20) # CAPTURE/SET FRAMES
    button0.place_configure(bordermode=tk.INSIDE, y=15, relx=0.886, rely=0.85, anchor=tk.CENTER, width=25, height=22) # sub sec
    button1.place_configure(bordermode=tk.INSIDE, y=15, relx=0.811, rely=0.85, anchor=tk.CENTER, width=25, height=22) # sub min
    frame_display.place_configure(bordermode=tk.INSIDE, y=33, relx=0.85, rely=0.75, anchor=tk.CENTER, width=120, height=30) # frameTimeText
    button2.place_configure(bordermode=tk.INSIDE, y=51, relx=0.886, rely=0.65, anchor=tk.CENTER, width=25, height=22) # add sec
    button4.place_configure(bordermode=tk.INSIDE, y=51, relx=0.811, rely=0.65, anchor=tk.CENTER, width=25, height=22) # add min

def multiCapTimerWindow(event = 0):
    global button0, button1, button2, button3, button4, cancel, frame_display, timerCount, frameText
    cancel = False
    
    button0.place_forget()
    button1.place_forget()
    button2.place_forget()
    button3.place_forget()
    button4.place_forget()
    frame_display.place_forget()

    frameText = str(numFrames)

    if timerArmed:
        time_display.config(text=timeText)
        button0.config(text="START TIMER", image="", command=multiCapThread)
        button2.config(text="SET TIMER", image="", command=timerWindow)

        if timerCount < 11:
            frame_display.config(text="FRAMES: " + frameText, font=('Ariel', 13), fg=cherry)
        else:
            frame_display.config(text="FRAMES: " + frameText, font=('Ariel', 13), fg=mint)
        
        time_display.place(bordermode=tk.INSIDE, relx=0.85, y=40, rely=0.6, anchor=tk.CENTER, width=120, height=20) # 00:00
        button2.place_configure(bordermode=tk.INSIDE, y=30, relx=0.85, rely=0.7, anchor=tk.CENTER, width=120, height=20) # SET TIMER
    else:
        frame_display.config(text="FRAMES: " + frameText, font=('Ariel', 13), fg=orange)
        button0.config(text="CAPTURE", image="", command=multiCapThread)

    button0.place_configure(bordermode=tk.INSIDE, y=10, relx=0.85, rely=0.9, anchor=tk.CENTER, width=120, height=20) # START TIMER/CAPTURE
    frame_display.place_configure(bordermode=tk.INSIDE, y=20, relx=0.85, rely=0.8, anchor=tk.CENTER, width=120, height=20) # Frames: 0000


# When timer is armed: thread allows live feed to work independently from 'while' loop in multiFrameCapture()
def multiCapThread(event = 0):
    t1 = threading.Thread(target=multiFrameCapture)
    t1.start()

def multiFrameCapture(event = 0):
    global frame, numFrames, mult_frame_counter, timerArmed, timerCount, timerText, btn_window, time_display, frame_display

    mult_frame_folderpath = createMultiFrameFolder()

    if timerArmed:
        button2.config(fg=beans, command="")

    button0.config(fg=beans, command="")
    buttonX.config(fg=beans, command="")

    while timerArmed:
        if timerCount > 0:
            timerCount -= 1
            timerText = clockString(timerCount)
            time.sleep(1)
            if timerCount < 11:
                btn_window.config(image=red_btn_window)
                btnX_window.config(image=red_btnX)
                time_display.config(fg=cherry)
                frame_display.config(fg=cherry)
            time_display.config(text=timerText)
        else:
            timerArmed = False
            time_display.config(text="CAPTURE\nIN PROGRESS", font=('Ariel', 7))

    while numFrames > 0:
        _, frame = capture.read()
        screenshot = mult_frame_folderpath + "/frame_capture_{}.png".format(mult_frame_counter)
        cv.imwrite(screenshot, frame)
        mult_frame_counter += 1
        numFrames -= 1
        time.sleep(0.1)

    restoreMenu()

def addSecondsMF():
    global mfTimeCount

    if mfTimeCount < 900:
        mfTimeCount += 1
    multiFrameWindow()

def subtractSecondsMF():
    global mfTimeCount

    if mfTimeCount > 0:
        mfTimeCount -= 1
    multiFrameWindow()

def addMinutesMF():
    global mfTimeCount

    if mfTimeCount < 840:
        mfTimeCount += 60
    else:
        mfTimeCount = 900
    multiFrameWindow()

def subtractMinutesMF():
    global mfTimeCount

    if mfTimeCount > 60:
        mfTimeCount -= 60
    elif mfTimeCount == 60:
        mfTimeCount = 0
    multiFrameWindow()
 
###############################################
################### TIMER #####################
###############################################

def timerWindow(event=0):
    global cancel, button4, timeText, time_display, frame_display
    cancel = False

    if frame_display.winfo_ismapped():
        frame_display.place_forget()

    timeText = clockString(timerCount)
    time_display.config(text=timeText, font=('Ariel', 19), fg=eggshell)
    button3.config(text="SET TIMER", command=restoreMenu)
    buttonX.config(text="RETURN", command=clearTimer)

    if timerCount == 5940:
        button2.config(image=dim_up_arrow, command=addSecondsTimer)
        button4.config(image=dim_up_arrow, command=addMinutesTimer)
    else:
        button2.config(image=up_arrow, command=addSecondsTimer)
        button4.config(image=up_arrow, command=addMinutesTimer)

    if timerCount == 0:
        button1.config(image=dim_down_arrow, command=subtractMinutesTimer)
        button0.config(image=dim_down_arrow, command=subtractSecondsTimer)
    elif timerCount < 60:
        button1.config(image=dim_down_arrow, command=subtractMinutesTimer)
        button0.config(image=down_arrow, command=subtractSecondsTimer)
    else:
        button1.config(image=down_arrow, command=subtractMinutesTimer)
        button0.config(image=down_arrow, command=subtractSecondsTimer)
    
    if not button3.winfo_ismapped():
        button3.place_configure(bordermode=tk.INSIDE, y=40, relx=0.85, rely=0.6, anchor=tk.CENTER, width=120, height=20) # SET TIMER

    button0.place_configure(bordermode=tk.INSIDE, y=15, relx=0.886, rely=0.85, anchor=tk.CENTER, width=25, height=22) # sub sec
    button1.place_configure(bordermode=tk.INSIDE, y=15, relx=0.811, rely=0.85, anchor=tk.CENTER, width=25, height=22) # sub min
    time_display.place_configure(bordermode=tk.INSIDE, y=33, relx=0.85, rely=0.75, anchor=tk.CENTER, width=120, height=30) # timeText
    button2.place_configure(bordermode=tk.INSIDE, y=51, relx=0.886, rely=0.65, anchor=tk.CENTER, width=25, height=22) # add sec
    button4.place_configure(bordermode=tk.INSIDE, y=51, relx=0.811, rely=0.65, anchor=tk.CENTER, width=25, height=22) # add min

# So you can RETURN to the main menu without arming the timer by setting the clock to 00:00
def clearTimer(event=0):
    global timerCount

    timerCount = 0
    restoreMenu()

def addSecondsTimer():
    global timerCount

    if timerCount < 5940:
        timerCount += 1
    timerWindow()

def subtractSecondsTimer():
    global timerCount

    if timerCount > 0:
        timerCount -= 1
    timerWindow()

def addMinutesTimer():
    global timerCount

    if timerCount < 5880:
        timerCount += 60
    else:
        timerCount = 5940
    timerWindow()

def subtractMinutesTimer():
    global timerCount

    if timerCount > 60:
        timerCount -= 60
    elif timerCount == 60:
        timerCount = 0
    timerWindow()

# Creates string of clock time "00:00" for clock display
def clockString(timeCount):

    floatMins = timeCount/60
    minutes = int(floatMins)
    seconds = timeCount - (minutes * 60)

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
    global btn_window, time_display, frame_display, cancel, timerArmed, cameFromCap, timerCount, numFrames, mfTimeCount, mult_frame_counter
    cancel=False
    
    button0.place_forget()
    button1.place_forget()
    button2.place_forget()
    button3.place_forget()
    button4.place_forget()
    time_display.place_forget()
    frame_display.place_forget()

    buttonX.configure(text="EXIT", font=('Ariel', 13), fg=eggshell, command=warningMessage)
    button0.config(text="CAPTURE", image="", font=('Ariel', 13), fg=eggshell, command=capSaveWindow)
    button1.config(text="MULTI-FRAME", image="", font=('Ariel', 13), fg=eggshell, command=multiFrameWindow)
    button2.config(text="SET TIMER", image="", font=('Ariel', 13), fg=eggshell, command=timerWindow)

    numFrames = 0
    mfTimeCount = 0
    mult_frame_counter = 0

    if timerCount == 0:
        timerArmed = False
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



###############################################
################ WARNING MESSAGE ##############
###############################################
def warningMessage(event = 0):
    reply = messagebox.askyesno('confirmation', 'All images stored on this device will be deleted upon exiting, do you want to proceed?')
    if reply == True:
        messagebox.showinfo('exiting.. ', 'Exiting application')
        mainWindow.destroy()
        sys.exit(0) #added function from the old "exitWindow" function
    else: 
        messagebox.showinfo ('', 'Thanks for Staying')

###############################################
############ WIDGET INITIALIZATION ############
###############################################

mainWindow = tk.Tk()
mainWindow.geometry("800x480")
mainWindow.resizable(width=False, height=False)
mainWindow.config(bg='black')
mainWindow.attributes('-fullscreen',True)
lmain = tk.Label(mainWindow, compound=tk.CENTER, anchor=tk.CENTER, relief=tk.RAISED)
buttonX = tk.Button(mainWindow, text="EXIT", font=('Ariel', 13), bg=eggplant, fg=eggshell, command=warningMessage, borderwidth=0, highlightthickness=0, activebackground=eggplant)
button0 = tk.Button(mainWindow, text="CAPTURE", font=('Ariel', 13), bg=eggplant, fg=eggshell, command=capSaveWindow, borderwidth=0, highlightthickness=0, activebackground=eggplant)
button1 = tk.Button(mainWindow, text="MULTI-FRAME", font=('Ariel', 13), bg=eggplant, fg=eggshell, command=multiFrameWindow, borderwidth=0, highlightthickness=0, activebackground=eggplant)
button2 = tk.Button(mainWindow, text="SET TIMER", font=('Ariel', 13), bg=eggplant, fg=eggshell, command=timerWindow, borderwidth=0, highlightthickness=0, activebackground=eggplant)
button3 = tk.Button(mainWindow, text="EXPORT", font=('Ariel', 13), bg=eggplant, fg=eggshell, command=export, borderwidth=0, highlightthickness=0, activebackground=eggplant)
button4 = tk.Button(mainWindow, text="", fg=eggshell, bg=eggplant, command="", borderwidth=0, highlightthickness=0, activebackground=eggplant)

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

#lmain.config(width=640, height=480)
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
button4.lift()

def rescale_frame(frame, percent):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv.resize(frame, dim, interpolation =cv.INTER_AREA)

# Update live feed frame
def show_frame():
    global cancel, prevImg

    _, frame = capture.read()
    scaledFrame = rescale_frame(frame, percent=65)
    cvimage = cv.cvtColor(scaledFrame, cv.COLOR_BGR2RGBA)

    prevImg = Image.fromarray(cvimage)
    imgtk = ImageTk.PhotoImage(image=prevImg)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    #lmain.configure(bg='#041e41') # Electrolux blue
    if not cancel:
        lmain.after(10, show_frame)

show_frame()
mainWindow.mainloop()
