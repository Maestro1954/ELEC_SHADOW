#import numpy as np
import cv2 as cv
import tkinter as tk
import os
import shutil
import sys
import threading
import time
from tkinter import messagebox
from PIL import Image, ImageTk


# GLOBAL VARIABLES
img_counter = 0
mult_frame_counter = 0
mult_frame_session = 0
export_counter = 0
numFrames = 0
timerCount = 0
mfTimeCount = 0
cancel = False
timerArmed = False
schedule_frame = False
# Colors
orange = '#faa010'
mint = '#46fcb5'
cherry = '#f01148'
papaya = '#fb8f6d'
eggshell = '#f6f3c0'
beans = '#532a07'
eggplant = '#2a082a'
elec_blue = '#041e41'
# Filepaths
btn_png_filepath = 'C:/Users/adrie/Documents/Documents/UNC_Charlotte/Spring 2022/ECGR-4252 Senior Design II/Button PNGs'
screenshot_filepath = "C:/Users/adrie/Documents/Documents/UNC_Charlotte/Spring 2022/ECGR-4252 Senior Design II/Screenshots"
usb_location = "C:/Users/adrie/Documents/Documents/UNC_Charlotte/Spring 2022/ECGR-4252 Senior Design II/USB File"
#btn_png_filepath = '/home/pi/ELEC_SHADOW/Button PNGs'
#screenshot_filepath = "/home/pi/ELEC_SHADOW/Screenshots"
#usb_location = "/media/pi"

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
    global cancel, frame, schedule_frame
    
    if not timerArmed:
        cancel = True
        _, frame = capture.read()
        schedule_frame = True
        button0.place_forget()
        button3.place_forget()
        buttonX.config(fg=beans, command="")
        button1.config(text="SAVE IMAGE", fg=eggshell, command=saveCapture)
        button2.config(text="DISCARD", font=('Ariel', 13), fg=eggshell, command=restoreMenu)
        button2.place_configure(bordermode=tk.INSIDE, relx=0.5, rely=0.388, anchor=tk.CENTER, width=120, height=20)
        
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
    global timerCount, timerArmed, img_counter, cancel, btn_window, top_label

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
                top_label.config(fg=cherry)
            top_label.config(text=timerText)
        else:
            top_label.config(text=timerText)
            time.sleep(1)
            top_label.place_forget()
            timerArmed = False
    
    button1.place_configure(bordermode=tk.INSIDE, relx=0.5, rely=0.612, anchor=tk.CENTER, width=120, height=20)
    capSaveWindow()

###############################################
########### MULTI FRAME CAPTURE ###############
###############################################

def multiFrameWindow(event = 0):
    global cancel, top_label, bottom_label, frameText, numFrames
    cancel = False

    if timerArmed:
        top_label.place_forget()

    frameTimeText = clockString(mfTimeCount)
    numFrames = mfTimeCount * 10
    bottom_label.config(text=frameTimeText, font=('Ariel', 19), fg=eggshell)
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
    button3.place_configure(bordermode=tk.INSIDE, relx=0.5, rely=0.164, anchor=tk.CENTER, width=120, height=20) # CAPTURE/SET FRAMES
    button0.place_configure(bordermode=tk.INSIDE, relx=0.66, rely=0.734, anchor=tk.CENTER, width=25, height=22) # sub sec
    button1.place_configure(bordermode=tk.INSIDE, relx=0.33, rely=0.734, anchor=tk.CENTER, width=25, height=22) # sub min
    bottom_label.place_configure(bordermode=tk.INSIDE, relx=0.5, rely=0.556, anchor=tk.CENTER, width=120, height=30) # frameTimeText
    button2.place_configure(bordermode=tk.INSIDE, relx=0.66, rely=0.377, anchor=tk.CENTER, width=25, height=22) # add sec
    button4.place_configure(bordermode=tk.INSIDE, relx=0.33, rely=0.377, anchor=tk.CENTER, width=25, height=22) # add min

def multiCapTimerWindow(event = 0):
    global button0, button1, button2, button3, button4, cancel, bottom_label, timerCount, frameText
    cancel = False
    
    button0.place_forget()
    button1.place_forget()
    button2.place_forget()
    button3.place_forget()
    button4.place_forget()
    bottom_label.place_forget()

    frameText = str(numFrames)

    if timerArmed:
        top_label.config(text=timeText)
        button0.config(text="START TIMER", image="", command=multiCapThread)
        button2.config(text="SET TIMER", image="", command=timerWindow)

        if timerCount < 11:
            bottom_label.config(text="FRAMES: " + frameText, font=('Ariel', 13), fg=cherry)
        else:
            bottom_label.config(text="FRAMES: " + frameText, font=('Ariel', 13), fg=mint)
        
        top_label.place(bordermode=tk.INSIDE, relx=0.5, rely=0.164, anchor=tk.CENTER, width=120, height=20) # 00:00
        button2.place_configure(bordermode=tk.INSIDE, relx=0.5, rely=0.388, anchor=tk.CENTER, width=120, height=20) # SET TIMER
    else:
        bottom_label.config(text="FRAMES: " + frameText, font=('Ariel', 13), fg=orange)
        button0.config(text="CAPTURE", image="", command=multiCapThread)

    button0.place_configure(bordermode=tk.INSIDE, relx=0.5, rely=0.836, anchor=tk.CENTER, width=120, height=20) # START TIMER/CAPTURE
    bottom_label.place_configure(bordermode=tk.INSIDE, relx=0.5, rely=0.612, anchor=tk.CENTER, width=120, height=20) # Frames: 0000

# When timer is armed: thread allows live feed to work independently from 'while' loop in multiFrameCapture()
def multiCapThread(event = 0):
    t1 = threading.Thread(target=multiFrameCapture)
    t1.start()

def multiFrameCapture(event = 0):
    global frame, numFrames, mult_frame_counter, timerArmed, timerCount, timerText, mult_frame_session

    mult_frame_folderpath, mult_frame_session = createFolder("Multi-Frame Captures ", screenshot_filepath, mult_frame_session)

    if timerArmed:
        button2.config(fg=beans, command="")
    else:
        top_label.config(text="CAPTURE\nIN PROGRESS", font=('Ariel', 10), fg=orange)
        top_label.place(bordermode=tk.INSIDE, relx=0.5, rely=0.164, anchor=tk.CENTER, width=120, height=30) # 00:00

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
                top_label.config(fg=cherry)
                bottom_label.config(fg=cherry)
            top_label.config(text=timerText)
        else:
            top_label.config(text=timerText)
            time.sleep(1)
            timerArmed = False
            top_label.config(text="CAPTURE\nIN PROGRESS", font=('Ariel', 10))
            top_label.place_configure(height=30)
    
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
    global cancel, timeText, top_label, bottom_label
    cancel = False

    if bottom_label.winfo_ismapped():
        bottom_label.place_forget()

    timeText = clockString(timerCount)
    top_label.config(text=timeText, font=('Ariel', 19), fg=eggshell)
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
        button3.place_configure(bordermode=tk.INSIDE, relx=0.5, rely=0.164, anchor=tk.CENTER, width=120, height=20) # SET TIMER

    button0.place_configure(bordermode=tk.INSIDE, relx=0.66, rely=0.734, anchor=tk.CENTER, width=25, height=22) # sub sec
    button1.place_configure(bordermode=tk.INSIDE, relx=0.33, rely=0.734, anchor=tk.CENTER, width=25, height=22) # sub min
    top_label.place_configure(bordermode=tk.INSIDE, relx=0.5, rely=0.556, anchor=tk.CENTER, width=120, height=30) # timeText
    button2.place_configure(bordermode=tk.INSIDE, relx=0.66, rely=0.377, anchor=tk.CENTER, width=25, height=22) # add sec
    button4.place_configure(bordermode=tk.INSIDE, relx=0.33, rely=0.377, anchor=tk.CENTER, width=25, height=22) # add min

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

def export():
    global usb_path, export_counter
    usbDetected = False
    
    # Finding the USB directory
    for _, usb_list, _ in os.walk(usb_location): 
        for usb_name in usb_list:
            usb_path = os.path.join(usb_location, usb_name)
            usb_path, export_counter = createFolder("Export ", usb_path, export_counter)
            usbDetected = True
        usb_list[:] = []

    standByMenu(usbDetected)
    # Moving PNGs and PNG folders to USB
    if usbDetected:
        path = screenshot_filepath
        directory = os.listdir(path)

        for file_name in directory:
            file_path = os.path.join(path, file_name)
            shutil.move(file_path, usb_path)
        
        messagebox.showinfo('EXPORT', 'All stored images have been exported.')
        usbDetected = False
    else:
        messagebox.showinfo('ERROR!', 'No USB storage device detected.')
    restoreMenu()

def exportThread(event = 0):
    t2 = threading.Thread(target=export)
    t2.start()

###############################################
################ WARNING MESSAGE ##############
###############################################

def warningMessage(event = 0):
    global cancel, schedule_frame

    cancel = True
    standByMenu(False)
    reply = messagebox.askyesno('WARNING!', 'All images stored on this device will be deleted upon exiting.\nAre you sure you want to exit?')
    if reply == True:
        eraseStoredImages()
        capture.release()
        root.destroy()
        sys.exit(0) # added function from the old "exitWindow" function
    else: 
        schedule_frame = True
        restoreMenu()

###############################################
############## HELPER FUNCTIONS ###############
###############################################

def restoreMenu(event=0):
    global btn_window, top_label, bottom_label, cancel, timerArmed, schedule_frame, timerCount, numFrames, mfTimeCount, mult_frame_counter
    cancel=False
    
    button0.place_forget()
    button1.place_forget()
    button2.place_forget()
    button3.place_forget()
    button4.place_forget()
    top_label.place_forget()
    bottom_label.place_forget()

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
        button3.config(text="EXPORT", image="", font=('Ariel', 13), fg=eggshell, command=exportThread)
        button3.place_configure(bordermode=tk.INSIDE, relx=0.5, rely=0.164, anchor=tk.CENTER, width=120, height=20)
    else:
        timerArmed = True
        if timerCount < 11:
            btn_window.config(image=red_btn_window)
            btnX_window.config(image=red_btnX)
            top_label.config(text=timeText, font=('Ariel', 19), fg=cherry)
        else:
            btn_window.config(image=green_btn_window)
            btnX_window.config(image=green_btnX)
            top_label.config(text=timeText, font=('Ariel', 19), fg=mint)
        top_label.place_configure(bordermode=tk.INSIDE, relx=0.5, rely=0.164, anchor=tk.CENTER, width=120, height=20)

    button0.place_configure(bordermode=tk.INSIDE, relx=0.5, rely=0.836, anchor=tk.CENTER, width=120, height=20)
    button1.place_configure(bordermode=tk.INSIDE, relx=0.5, rely=0.612, anchor=tk.CENTER, width=120, height=20)
    button2.place_configure(bordermode=tk.INSIDE, relx=0.5, rely=0.388, anchor=tk.CENTER, width=120, height=20)

    if schedule_frame:
        schedule_frame = False
        live_feed.after(10, show_frame)

def standByMenu(exporting):
    buttonX.config(fg=beans, command="")
    button2.config(fg=beans, command="")
    button1.config(fg=beans, command="")
    button0.config(fg=beans, command="")
    
    if not exporting:
        button3.config(fg=beans, command="")
        btnX_window.config(image=red_btnX)
        btn_window.config(image=red_btn_window)
    else:
        button3.place_forget()
        top_label.config(text="EXPORT\nIN PROGRESS", font=('Ariel', 10))
        top_label.place_configure(bordermode=tk.INSIDE, relx=0.5, rely=0.164, anchor=tk.CENTER, width=120, height=30)

def createFolder(folderName, parent_dir, counter):
    # folderName = "name " <= make sure the name includes a space
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
    path = screenshot_filepath
    directory = os.listdir(path)
    for file_name in directory:
        file_path = os.path.join(path, file_name)
        if os.path.isfile(file_path): # Deleting PNG files
            os.remove(file_path)
        elif os.path.isdir(file_path): # Deleting folders of PNG files
            shutil.rmtree(file_path)

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
#root.attributes('-fullscreen',True)
live_feed = tk.Label(root, compound=tk.CENTER, anchor=tk.CENTER, relief=tk.RAISED)


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

btn_menu = tk.Frame(root, borderwidth=0, highlightthickness=0)
btnX_menu = tk.Frame(root, borderwidth=0, highlightthickness=0)
btn_window = tk.Label(btn_menu, image=orng_btn_window)
btnX_window = tk.Label(btnX_menu, image=orng_btnX)
top_label = tk.Label(btn_menu, fg=eggshell, bg=eggplant)
bottom_label = tk.Label(btn_menu, fg=eggshell, bg=eggplant)


buttonX = tk.Button(btnX_menu, text="EXIT", font=('Ariel', 13), bg=eggplant, fg=eggshell, command=warningMessage, 
                    borderwidth=0, highlightthickness=0, activebackground=eggplant, activeforeground=eggshell)
button0 = tk.Button(btn_menu, text="CAPTURE", font=('Ariel', 13), bg=eggplant, fg=eggshell, command=capSaveWindow, 
                    borderwidth=0, highlightthickness=0, activebackground=eggplant, activeforeground=eggshell)
button1 = tk.Button(btn_menu, text="MULTI-FRAME", font=('Ariel', 13), bg=eggplant, fg=eggshell, command=multiFrameWindow, 
                    borderwidth=0, highlightthickness=0, activebackground=eggplant, activeforeground=eggshell)
button2 = tk.Button(btn_menu, text="SET TIMER", font=('Ariel', 13), bg=eggplant, fg=eggshell, command=timerWindow, 
                    borderwidth=0, highlightthickness=0, activebackground=eggplant, activeforeground=eggshell)
button3 = tk.Button(btn_menu, text="EXPORT", font=('Ariel', 13), bg=eggplant, fg=eggshell, command=exportThread, 
                    borderwidth=0, highlightthickness=0, activebackground=eggplant)
button4 = tk.Button(btn_menu, bg=eggplant, command="", borderwidth=0, highlightthickness=0, activebackground=eggplant)

live_feed.pack()
btn_menu.place(bordermode=tk.INSIDE, y=1, relx=0.85, rely=0.8, anchor=tk.CENTER, width=150, height=164)
btn_window.pack()
btnX_menu.place(bordermode=tk.INSIDE, relx=0.85, rely=0.1, anchor=tk.CENTER, width=150, height=49)
btnX_window.pack()

buttonX.place(bordermode=tk.INSIDE, relx=0.5, rely=0.5, anchor=tk.CENTER, width=120, height=20)
button0.place(bordermode=tk.INSIDE, relx=0.5, rely=0.836, anchor=tk.CENTER, width=120, height=20)
button1.place(bordermode=tk.INSIDE, relx=0.5, rely=0.612, anchor=tk.CENTER, width=120, height=20)
button2.place(bordermode=tk.INSIDE, relx=0.5, rely=0.388, anchor=tk.CENTER, width=120, height=20)
button3.place(bordermode=tk.INSIDE, relx=0.5, rely=0.164, anchor=tk.CENTER, width=120, height=20)

buttonX.lift()
button0.lift()
button1.lift()
button2.lift()
button3.lift()
button4.lift()

# Update live feed frame
def show_frame():
    global cancel, prevImg

    _, frame = capture.read()
    scaledFrame = rescale_frame(frame, percent=65)
    cvimage = cv.cvtColor(scaledFrame, cv.COLOR_BGR2RGBA)

    prevImg = Image.fromarray(cvimage)
    imgtk = ImageTk.PhotoImage(image=prevImg)
    live_feed.imgtk = imgtk
    live_feed.configure(image=imgtk)
    #live_feed.configure(bg=elec_blue)
    if not cancel:
        live_feed.after(10, show_frame)

show_frame()
root.mainloop()
