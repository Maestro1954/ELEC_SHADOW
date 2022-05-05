import cv2 as cv
import tkinter as tk
import os
import shutil
import sys
import threading
import time
from tkinter import messagebox
from PIL import Image, ImageTk
from subprocess import call

###############################################
############# GLOBAL VARIABLES ################
###############################################

# Counters
imgCounter = 0
multFrameCounter = 0
multFrameSession = 0
exportCounter = 0
numFrames = 0
timerCount = 0
mfTimeCount = 0
# Booleans
pause_feed = False
timer_Armed = False
schedule_frame = False
place_clock = True
# Colors (Constant)
ORANGE = '#faa010'
MINT = '#46fcb5'
CHERRY = '#f01148'
PAPAYA = '#fb8f6d'
EGGSHELL = '#f6f3c0'
BEANS = '#532a07'
EGGPLANT = '#2a082a'
# Filepaths (Constant)
PNG_PATH = '/home/pi/ELEC_SHADOW/Button PNGs'
SCREENSHOT_PATH = "/home/pi/ELEC_SHADOW/Screenshots"
USB_PATH = "/media/pi"

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
    global pause_feed, frame, schedule_frame, place_clock
    
    if timer_Armed:
        pause_feed = False
        place_clock = True
        button1.place_forget()
        buttonX.config(text="RETURN", command=restoreMenu)
        button0.config(text="START TIMER", command=threader)
    else:
        pause_feed = True
        _, frame = capture.read()
        schedule_frame = True
        button0.config(text="", command="")
        button3.config(text="", command="")
        buttonX.config(state='disabled')
        button1.config(text="SAVE IMAGE", command=saveCapture)
        button2.config(text="DISCARD", command=restoreMenu, state='normal')
        button2.place(bordermode=tk.INSIDE, relx=0.5, rely=0.388, anchor=tk.CENTER, width=120, height=22)

def saveCapture(event = 0):
    global imgCounter, frame, pause_feed

    screenshot = SCREENSHOT_PATH + "/screenshot_{}.png".format(imgCounter)
    cv.imwrite(screenshot, frame)
    imgCounter += 1
    restoreMenu()

def threadedSaveCap(event = 0):
    global timer_Armed, timerCount

    button0.config(state='disabled')
    button2.config(state='disabled')
    buttonX.config(state='disabled')

    while timer_Armed:
        if timerCount > 0:
            timerCount -= 1
            timerText = clockString(timerCount)
            time.sleep(0.96)
            if timerCount < 11:
                btn_window.config(image=red_btn_window)
                btnX_window.config(image=red_btnX)
                top_label.config(fg=CHERRY)
            top_label.config(text=timerText)
        else:
            top_label.config(text=timerText)
            time.sleep(0.96)
            top_label.place_forget()
            timer_Armed = False
    
    button1.place(bordermode=tk.INSIDE, relx=0.5, rely=0.612, anchor=tk.CENTER, width=120, height=22)
    capSaveWindow()

###############################################
########### MULTI FRAME CAPTURE ###############
###############################################

def multiFrameWindow(event = 0):
    global pause_feed, numFrames, place_clock
    pause_feed = False

    if place_clock:
        forgetAllWidgets()

    frameTimeText = clockString(mfTimeCount)
    numFrames = mfTimeCount * 10
    bottom_label.config(text=frameTimeText, font=('Ariel', 19), fg=EGGSHELL)
    buttonX.config(text="RETURN", command=restoreMenu) # RETURN 
    
    if mfTimeCount == 900:
        button2.config(image=dim_up_arrow, command=addSecondsMF)
        button4.config(image=dim_up_arrow, command=addMinutesMF)
    else:
        button2.config(image=up_arrow, command=addSecondsMF)
        button4.config(image=up_arrow, command=addMinutesMF)

    if mfTimeCount == 0:
        button1.config(image=dim_down_arrow, command=subtractMinutesMF)
        button0.config(image=dim_down_arrow, command=subtractSecondsMF)
        button3.config(text="SET FRAMES", state='disabled')
    elif mfTimeCount < 60:
        button1.config(image=dim_down_arrow, command=subtractMinutesMF)
        button0.config(image=down_arrow, command=subtractSecondsMF)
        button3.config(text="SET FRAMES", command=multiFramePhaseTwo, state='normal')
    else:
        button1.config(image=down_arrow, command=subtractMinutesMF)
        button0.config(image=down_arrow, command=subtractSecondsMF)
        button3.config(text="SET FRAMES", command=multiFramePhaseTwo, state='normal')
    
    if place_clock:
        place_clock = False
        placeClockAndArrows(False)

def multiFramePhaseTwo(event = 0):
    global pause_feed, place_clock
    pause_feed = False
    
    # For a smooth transition, clear menu of all buttons before configuring and then placing
    forgetAllWidgets()

    frameText = str(numFrames)

    if timer_Armed:
        place_clock = True
        top_label.config(text=timeText)
        button0.config(text="START TIMER", image="", command=threader)
        button2.config(text="SET TIMER", image="", command=timerWindow)

        if timerCount < 11:
            bottom_label.config(text="FRAMES: " + frameText, font=('Ariel', 13), fg=CHERRY)
        else:
            bottom_label.config(text="FRAMES: " + frameText, font=('Ariel', 13), fg=MINT)
        
        top_label.place(bordermode=tk.INSIDE, relx=0.5, rely=0.164, anchor=tk.CENTER, width=120, height=22) # 00:00
        button2.place(bordermode=tk.INSIDE, relx=0.5, rely=0.388, anchor=tk.CENTER, width=120, height=22) # SET TIMER
    else:
        bottom_label.config(text="FRAMES: " + frameText, font=('Ariel', 13), fg=ORANGE)
        button0.config(text="CAPTURE", image="", command=threader)

    button0.place(bordermode=tk.INSIDE, relx=0.5, rely=0.836, anchor=tk.CENTER, width=120, height=22) # START TIMER/CAPTURE
    bottom_label.place(bordermode=tk.INSIDE, relx=0.5, rely=0.612, anchor=tk.CENTER, width=120, height=22) # Frames: 0000

def multiFrameCapture(event = 0):
    global multFrameSession, timer_Armed, numFrames, multFrameCounter, timerCount, pause_feed, schedule_frame

    mult_frame_folderpath, multFrameSession = createFolder("Multi-Frame Captures ", SCREENSHOT_PATH, multFrameSession)

    if timer_Armed:
        button2.config(state='disabled')
    else:
        top_label.config(text="CAPTURE\nIN PROGRESS", font=('Ariel', 10), fg=ORANGE)
        top_label.place(bordermode=tk.INSIDE, relx=0.5, rely=0.164, anchor=tk.CENTER, width=120, height=30) # 00:00

    button0.config(state='disabled')
    buttonX.config(state='disabled')

    while timer_Armed:
        if timerCount > 0:
            timerCount -= 1
            timerText = clockString(timerCount)
            time.sleep(0.96)
            if timerCount < 11:
                btn_window.config(image=red_btn_window)
                btnX_window.config(image=red_btnX)
                top_label.config(fg=CHERRY)
                bottom_label.config(fg=CHERRY)
            top_label.config(text=timerText)
        else:
            top_label.config(text=timerText)
            time.sleep(0.96)
            timer_Armed = False
            top_label.config(text="CAPTURE\nIN PROGRESS", font=('Ariel', 10))
            top_label.place(height=30)
    
    captureArr = []

    while numFrames > 0:
        _, frame = capture.read()
        captureArr.append(frame)
        numFrames -= 1
        time.sleep(0.08)
    
    top_label.config(text="PROCESSING\nCAPTURES")
    bottom_label.config(fg=BEANS)
    pause_feed = True

    for cap in captureArr:
        screenshot = mult_frame_folderpath + "/frame_capture_{}.png".format(multFrameCounter)
        cv.imwrite(screenshot, cap)
        multFrameCounter += 1

    schedule_frame = True
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
    global pause_feed, timeText, place_clock
    pause_feed = False

    if place_clock:
        forgetAllWidgets()

    timeText = clockString(timerCount)
    top_label.config(text=timeText, font=('Ariel', 19), fg=EGGSHELL)
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

    if place_clock:
        place_clock = False
        placeClockAndArrows(True)

# Allows you to RETURN to the main menu without arming the timer by setting the clock equal to 00:00
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

def export():
    global exportCounter, pause_feed, schedule_frame
    pause_feed = True
    usbDetected = False
    
    # Finding the USB directory
    for _, usb_list, _ in os.walk(USB_PATH): 
        for usb_name in usb_list:
            usb_path = os.path.join(USB_PATH, usb_name)
            usb_path, exportCounter = createFolder("Export ", usb_path, exportCounter)
            usbDetected = True
        usb_list[:] = []

    standByMenu(usbDetected)
    # Moving PNGs and PNG folders to USB
    if usbDetected:
        path = SCREENSHOT_PATH
        directory = os.listdir(path)

        for file_name in directory:
            file_path = os.path.join(path, file_name)
            shutil.move(file_path, usb_path)
        
        messagebox.showinfo('EXPORT', 'All stored images have been exported.')
        usbDetected = False
    else:
        messagebox.showinfo('ERROR!', 'No USB storage device detected.')
    
    schedule_frame = True
    restoreMenu()

###############################################
################### EXIT ######################
###############################################

def warningMessage(event = 0):
    global pause_feed, schedule_frame

    pause_feed = True
    standByMenu(False)
    reply = messagebox.askyesno('WARNING!', 'All images stored on this device will be deleted upon exiting.\nAre you sure you want to exit?')
    if reply == True:
        eraseStoredImages()
        capture.release()
        root.destroy()
        call("sudo nohup shutdown -h now", shell=True) # Shuts down raspberry pi
    else: 
        schedule_frame = True
        restoreMenu()

###############################################
############## HELPER FUNCTIONS ###############
###############################################

# Restores the main menu to its default button mapping or timer mapping if timer is armed
def restoreMenu(event=0):
    global pause_feed, timer_Armed, numFrames, mfTimeCount, multFrameCounter, schedule_frame, place_clock
    pause_feed = False
    place_clock = True
    
    # For a smooth transition, clear menu of all buttons before configuring and then placing
    button0.config(text="", command="")
    button1.config(text="", command="")
    button2.config(text="", command="")
    button3.config(text="", command="")
    button4.place_forget()
    top_label.place_forget()
    bottom_label.place_forget()

    buttonX.config(text="EXIT", command=warningMessage, state='normal')
    button0.config(text="CAPTURE", image="", command=capSaveWindow, state='normal')
    button1.config(text="MULTI-FRAME", image="", command=multiFrameWindow, state='normal')
    button2.config(text="SET TIMER", image="", command=timerWindow, state='normal')

    numFrames = 0
    mfTimeCount = 0
    multFrameCounter = 0

    if timerCount == 0:
        timer_Armed = False
        btn_window.config(image=orng_btn_window)
        btnX_window.config(image=orng_btnX)
        button3.config(text="EXPORT", command=threader, state='normal')
        button3.place(bordermode=tk.INSIDE, relx=0.5, rely=0.164, anchor=tk.CENTER, width=120, height=22)
    else:
        timer_Armed = True
        if timerCount < 11:
            btn_window.config(image=red_btn_window)
            btnX_window.config(image=red_btnX)
            top_label.config(text=timeText, font=('Ariel', 19), fg=CHERRY)
        else:
            btn_window.config(image=green_btn_window)
            btnX_window.config(image=green_btnX)
            top_label.config(text=timeText, font=('Ariel', 19), fg=MINT)
        top_label.place(bordermode=tk.INSIDE, relx=0.5, rely=0.164, anchor=tk.CENTER, width=120, height=22)

    button0.place(bordermode=tk.INSIDE, relx=0.5, rely=0.836, anchor=tk.CENTER, width=120, height=22)
    button1.place(bordermode=tk.INSIDE, relx=0.5, rely=0.612, anchor=tk.CENTER, width=120, height=22)
    button2.place(bordermode=tk.INSIDE, relx=0.5, rely=0.388, anchor=tk.CENTER, width=120, height=22)

    if schedule_frame:
        schedule_frame = False
        live_feed.after(10, show_frame)

# Turns the menu to red when EXITing, or displays the EXPORT in progress notification
def standByMenu(exporting):
    buttonX.config(state='disabled')
    button3.config(state='disabled')
    button2.config(state='disabled')
    button1.config(state='disabled')
    button0.config(state='disabled')
    
    if not exporting:
        btnX_window.config(image=red_btnX)
        btn_window.config(image=red_btn_window)
        if top_label.winfo_ismapped() == True:
            top_label.config(fg=CHERRY)
    else:
        top_label.config(text="EXPORT\nIN PROGRESS", fg=ORANGE, font=('Ariel', 10))
        top_label.place(bordermode=tk.INSIDE, relx=0.5, rely=0.164, anchor=tk.CENTER, width=120, height=30)

def forgetAllWidgets():
    button0.place_forget()
    button1.place_forget()
    button2.place_forget()
    button3.place_forget()
    button4.place_forget()
    top_label.place_forget()
    bottom_label.place_forget()

def placeClockAndArrows(useTopLabel):
    button0.place(bordermode=tk.INSIDE, relx=0.7, rely=0.734, anchor=tk.CENTER, width=30, height=25) # sub sec
    button1.place(bordermode=tk.INSIDE, relx=0.31, rely=0.734, anchor=tk.CENTER, width=30, height=25) # sub min
    button2.place(bordermode=tk.INSIDE, relx=0.7, rely=0.377, anchor=tk.CENTER, width=30, height=25) # add sec
    button3.place(bordermode=tk.INSIDE, relx=0.5, rely=0.164, anchor=tk.CENTER, width=120, height=22) # SET
    button4.place(bordermode=tk.INSIDE, relx=0.31, rely=0.377, anchor=tk.CENTER, width=30, height=25) # add min

    if useTopLabel:
        top_label.place(bordermode=tk.INSIDE, relx=0.5, rely=0.556, anchor=tk.CENTER, width=120, height=30) # timeText
    else:
        bottom_label.place(bordermode=tk.INSIDE, relx=0.5, rely=0.556, anchor=tk.CENTER, width=120, height=30) # frameTimeText

# Allows the live-feed to work independently from any 'while' loops in the program that need to run
def threader(event=0):
    if button3.cget("text") == "EXPORT":
        t = threading.Thread(target=export)
    elif bottom_label.winfo_ismapped() == True:
        t = threading.Thread(target=multiFrameCapture)
    else:
        t = threading.Thread(target=threadedSaveCap)
    t.start()

def createFolder(folderName, parent_dir, counter):
    directory = folderName + "{}".format(counter)
    path = os.path.join(parent_dir, directory)
    if not os.path.isdir(path):
        os.mkdir(path)
        counter += 1
    else:
        folderName += "{}.".format(counter)
        path, counter = createFolder(folderName, parent_dir, counter)

    return path, counter

def eraseStoredImages():
    path = SCREENSHOT_PATH
    directory = os.listdir(path)
    for file_name in directory:
        file_path = os.path.join(path, file_name)
        if os.path.isfile(file_path): # Deleting PNG files
            os.remove(file_path)
        elif os.path.isdir(file_path): # Deleting folders of PNG files
            shutil.rmtree(file_path)

# Scales live-feed frame to fit in display (captures are not scaled)
def rescale_frame(frame, percent):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv.resize(frame, dim, interpolation =cv.INTER_AREA)

###############################################
############ WIDGET INITIALIZATION ############
###############################################

root = tk.Tk()
root.geometry("800x480")
root.resizable(width=False, height=False)
root.config(bg='black')
root.attributes('-fullscreen',True)
live_feed = tk.Label(root, compound=tk.CENTER, anchor=tk.CENTER, relief=tk.RAISED)


up_arrow = tk.PhotoImage(file=(PNG_PATH + '/up_arrow.png'))
down_arrow = tk.PhotoImage(file=(PNG_PATH + '/down_arrow.png'))
dim_up_arrow = tk.PhotoImage(file=(PNG_PATH + '/dim_up_arrow.png'))
dim_down_arrow = tk.PhotoImage(file=(PNG_PATH + '/dim_down_arrow.png'))
orng_btn_window = tk.PhotoImage(file=(PNG_PATH + '/orng_btn_window.png'))
green_btn_window = tk.PhotoImage(file=(PNG_PATH + '/green_btn_window.png'))
red_btn_window = tk.PhotoImage(file=(PNG_PATH + '/red_btn_window.png'))
orng_btnX = tk.PhotoImage(file=(PNG_PATH + '/orng_btnX.png'))
green_btnX = tk.PhotoImage(file=(PNG_PATH + '/green_btnX.png'))
red_btnX = tk.PhotoImage(file=(PNG_PATH + '/red_btnX.png'))

btn_menu = tk.Frame(root, borderwidth=0, highlightthickness=0)
btnX_menu = tk.Frame(root, borderwidth=0, highlightthickness=0)
btn_window = tk.Label(btn_menu, image=orng_btn_window)
btnX_window = tk.Label(btnX_menu, image=orng_btnX)
top_label = tk.Label(btn_menu, fg=EGGSHELL, bg=EGGPLANT)
bottom_label = tk.Label(btn_menu, fg=EGGSHELL, bg=EGGPLANT)


buttonX = tk.Button(btnX_menu, text="EXIT", font=('Ariel', 13), bg=EGGPLANT, fg=EGGSHELL, command=warningMessage, 
                    borderwidth=0, highlightthickness=0, activebackground=EGGPLANT, activeforeground=EGGSHELL, disabledforeground=BEANS)
button0 = tk.Button(btn_menu, text="CAPTURE", font=('Ariel', 13), bg=EGGPLANT, fg=EGGSHELL, command=capSaveWindow, 
                    borderwidth=0, highlightthickness=0, activebackground=EGGPLANT, activeforeground=EGGSHELL, disabledforeground=BEANS)
button1 = tk.Button(btn_menu, text="MULTI-FRAME", font=('Ariel', 13), bg=EGGPLANT, fg=EGGSHELL, command=multiFrameWindow, 
                    borderwidth=0, highlightthickness=0, activebackground=EGGPLANT, activeforeground=EGGSHELL, disabledforeground=BEANS)
button2 = tk.Button(btn_menu, text="SET TIMER", font=('Ariel', 13), bg=EGGPLANT, fg=EGGSHELL, command=timerWindow, 
                    borderwidth=0, highlightthickness=0, activebackground=EGGPLANT, activeforeground=EGGSHELL, disabledforeground=BEANS)
button3 = tk.Button(btn_menu, text="EXPORT", font=('Ariel', 13), bg=EGGPLANT, fg=EGGSHELL, command=threader, 
                    borderwidth=0, highlightthickness=0, activebackground=EGGPLANT, activeforeground=EGGSHELL, disabledforeground=BEANS)
button4 = tk.Button(btn_menu, bg=EGGPLANT, command="", borderwidth=0, highlightthickness=0, activebackground=EGGPLANT)

live_feed.pack()
btn_menu.place(bordermode=tk.INSIDE, relx=0.88, rely=0.77, anchor=tk.CENTER, width=150, height=164)
btn_window.pack()
btnX_menu.place(bordermode=tk.INSIDE, relx=0.88, rely=0.09, anchor=tk.CENTER, width=150, height=49)
btnX_window.pack()

buttonX.place(bordermode=tk.INSIDE, relx=0.5, rely=0.5, anchor=tk.CENTER, width=120, height=22)
button0.place(bordermode=tk.INSIDE, relx=0.5, rely=0.836, anchor=tk.CENTER, width=120, height=22)
button1.place(bordermode=tk.INSIDE, relx=0.5, rely=0.612, anchor=tk.CENTER, width=120, height=22)
button2.place(bordermode=tk.INSIDE, relx=0.5, rely=0.388, anchor=tk.CENTER, width=120, height=22)
button3.place(bordermode=tk.INSIDE, relx=0.5, rely=0.164, anchor=tk.CENTER, width=120, height=22)

buttonX.lift()
button0.lift()
button1.lift()
button2.lift()
button3.lift()
button4.lift()
top_label.lift()

# Update live feed frame
def show_frame():
    global pause_feed, prevImg

    _, frame = capture.read()
    scaledFrame = rescale_frame(frame, percent=65)
    cvimage = cv.cvtColor(scaledFrame, cv.COLOR_BGR2RGBA)

    prevImg = Image.fromarray(cvimage)
    imgtk = ImageTk.PhotoImage(image=prevImg)
    live_feed.imgtk = imgtk
    live_feed.configure(image=imgtk)

    if not pause_feed:
        live_feed.after(10, show_frame)

show_frame()
root.mainloop()
