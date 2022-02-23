import time
from tkinter import *
from tkinter import messagebox

# creating Tk window


root = Tk()

# setting geometry of tk window
root.geometry("300x250")

# Using title() to display a message in
# the dialogue box of the message in the
# title bar.
root.title("Time Counter")

# Declaration of variables

second = 0

# setting the default value as 0



# Use of Entry class to take input from the user

def add():
    global second
    second += 1
    label.config(text=str(second))
    label.after(100)
    print(second)

def sub():
    global second

    second -= 1
    label.config(text=str(second))
    label.after(100)
    print(second)



def submit():
    try:
        # the input provided by the user is
        # stored in here :temp
        temp = second
    except:
        print("Please input the right value")
    while temp > -1:

        # divmod(firstvalue = temp//60, secondvalue = temp%60)
        mins, secs = divmod(temp, 60)

        # Converting the input entered in mins or secs to hours,
        # mins ,secs(input = 110 min --> 120*60 = 6600 => 1hr :
        # 50min: 0sec)
        hours = 0


        # using format () method to store the value up to
        # two decimal places
        # second.set("{0:2d}".format(secs))

        # updating the GUI window after decrementing the
        # temp value every time
        root.update()
        time.sleep(1)

        # when temp value = 0; then a messagebox pop's up
        # with a message:"Time's up"
        if (temp == 0):
            messagebox.showinfo("Time Countdown", "Time's up ")

        # after every one sec the value of temp will be decremented
        # by one
        temp -= 1


# button widget
btn = Button(root, text='Set Time Countdown', bd='5',
             command=submit)
btn.place(x=90, y=120)

button = Button(text='add 1', command=add)
button.place(x=90, y=150)
button1 = Button(text='sub 1', command=sub)
button1.place(x=90, y=180)

label = Label(root, fg="green")
label.place(x=90, y=80)
label.after(1000)

# infinite loop which is required to
# run tkinter program infinitely
# until an interrupt occurs
root.mainloop()